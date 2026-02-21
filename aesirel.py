import telebot
from telebot import types
import html
import json
import os
import schedule
import threading
import time
from datetime import datetime, timedelta

# === НАСТРОЙКИ ===
BOT_TOKEN = '8571682294:AAHfLqvLSadmm1qaGn94LSZV4sNm11RV2cE'
CHANNEL_ID = -1003768671164
OWNER_IDS = [5127944821, 6066649640]
OWNER_USERNAME = '@arzaramanager'
ADMIN_FILE = 'admins_aesirel.json'
CHECK_TIME = "23:59"

# === ЛОГ-БОТ НАСТРОЙКИ ===
LOG_BOT_TOKEN = '7973441371:AAELiQCvqAdB8jFqmYxQT0ib7oBWHxpU3oo'  # ⚠️ Замените на токен вашего лог-бота
OWNER_CHAT_ID = 5127944821  # ⚠️ Замените на ваш ID

# Основной бот
bot = telebot.TeleBot(BOT_TOKEN)
# Бот для логов
log_bot = telebot.TeleBot(LOG_BOT_TOKEN, parse_mode='HTML')


# === ФУНКЦИЯ ЛОГИРОВАНИЯ ===
def log(message: str):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] {message}"

    # Вывод в консоль
    print(log_message)

    # Отправка в Telegram
    try:
        log_bot.send_message(
            OWNER_CHAT_ID,
            f"{html.escape(log_message)}",
            parse_mode='HTML'
        )
    except Exception as e:
        print(f"[LOG FAILED] Не удалось отправить сообщение в лог-бот: {e}")


# --- ЗАГРУЗКА АДМИНОВ ИЗ JSON ---
def load_admins():
    if not os.path.exists(ADMIN_FILE):
        return {}
    try:
        with open(ADMIN_FILE, 'r', encoding='utf-8') as f:
            data = f.read().strip()
            return json.loads(data) if data else {}
    except Exception as e:
        log(f"Ошибка при загрузке админов: {e}")
        return {}


def save_admins(admins):
    try:
        with open(ADMIN_FILE, 'w', encoding='utf-8') as f:
            json.dump(admins, f, ensure_ascii=False, indent=4)
    except Exception as e:
        log(f"Ошибка при сохранении админов: {e}")


# --- ПРОВЕРКА ПРАВ ---
def is_owner(user):
    return user and (user.id in OWNER_IDS)


# ... существующий код ...

def is_admin(user):
    if not user:
        return False

    if is_owner(user):
        return True

    admins = load_admins()
    username = user.username.lstrip('@') if user.username else None
    user_id = user.id

    admin_entry = None
    matched_username = None

    # Поиск по username
    if username and username in admins:
        admin_entry = admins[username]
        matched_username = username

    # Поиск по user_id, если не нашли по username
    if not admin_entry:
        for uname, data in admins.items():
            if data.get('user_id') == user_id:
                admin_entry = data
                matched_username = uname
                break

    if not admin_entry:
        return False

    try:
        expiry_date = datetime.fromisoformat(admin_entry["expiry"]).date()
        check_time_obj = datetime.strptime(CHECK_TIME, "%H:%M").time()
        expiry_datetime = datetime.combine(expiry_date, check_time_obj)
        now = datetime.now()

        # Админ активен, если сейчас <= времени окончания (включительно до указанного времени)
        is_active = now <= expiry_datetime  # Изменено: <= вместо <

        # Обновляем user_id, если нужно
        if admin_entry.get('user_id') != user_id:
            admins[matched_username]['user_id'] = user_id
            save_admins(admins)
            log(f"🔄 Обновлён user_id для @{matched_username}: {user_id}")

        return is_active or is_owner(user)

    except Exception as e:
        log(f"❌ Ошибка при проверке срока админа (возможно @{matched_username}): {e}")
        return False


def get_username(user):
    return user.username if user and user.username else f"id_{user.id}"


# --- СОСТОЯНИЯ ДЛЯ ПУБЛИКАЦИИ ЗАДАНИЙ ---
active_sets = {}
user_states = {}


def check_for_start(message):
    """Проверяет, не ввёл ли пользователь /start, и перезапускает бота"""
    if message.text == '/start':
        username = get_username(message.from_user)
        if username in user_states:
            del user_states[username]
        if "pending_admin" in user_states:
            del user_states["pending_admin"]
        start(message)
        return True
    return False


# === ОСНОВНОЕ МЕНЮ ===
def main_menu(chat_id, user=None):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📂 Открыть набор", callback_data="open_set"))
    markup.add(types.InlineKeyboardButton("❌ Закрыть набор", callback_data="close_set"))
    if is_owner(user):
        markup.add(types.InlineKeyboardButton("⚙️ Управление админами", callback_data="admin_menu"))
    bot.send_message(chat_id, "Главное меню:", reply_markup=markup)


# === КОМАНДА /start ===
@bot.message_handler(commands=['start'])
def start(message):
    # Сбрасываем все возможные состояния
    username = get_username(message.from_user)
    if username in user_states:
        del user_states[username]
    if "pending_admin" in user_states:
        del user_states["pending_admin"]

    if not is_admin(message.from_user):
        bot.send_message(message.chat.id, f"🔐Упс, у вас нет доступа к боту!\nМожете приобрести доступ у {OWNER_USERNAME}", parse_mode='HTML')
        return
    main_menu(message.chat.id, message.from_user)


# === КНОПКА: ПЕРЕХОД В МЕНЮ УПРАВЛЕНИЯ АДМИНАМИ ===
@bot.callback_query_handler(func=lambda call: call.data == "admin_menu")
def go_to_admin_menu(call):
    if not is_owner(call.from_user):
        bot.answer_callback_query(call.id, "⛔ Доступ запрещён.", show_alert=True)
        return
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    bot.send_message(call.message.chat.id, "🔧 <b>Меню управления админами:</b>", parse_mode='HTML',
                     reply_markup=admin_main_menu())
    bot.answer_callback_query(call.id)


# === МЕНЮ УПРАВЛЕНИЯ АДМИНАМИ ===
def admin_main_menu():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("➕ Назначить админа", callback_data="add_admin"))
    markup.add(types.InlineKeyboardButton("❌ Снять админа", callback_data="remove_admin"))
    markup.add(types.InlineKeyboardButton("📋 Посмотреть админов", callback_data="list_admins"))
    markup.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main"))
    return markup


# === НАЗНАЧЕНИЕ АДМИНА ===
@bot.callback_query_handler(func=lambda call: call.data == "add_admin")
def ask_admin_username(call):
    if not is_owner(call.from_user):
        bot.answer_callback_query(call.id, "⛔ Доступ запрещён.", show_alert=True)
        return
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    msg = bot.send_message(call.message.chat.id, "Введите юзернейм админа:")
    bot.register_next_step_handler(msg, process_username_step)


def process_username_step(message):
    if check_for_start(message):
        return

    username = message.text.strip().lstrip('@')
    if not username:
        bot.send_message(message.chat.id, "❌ Юзернейм не может быть пустым.")
        return

    user_states["pending_admin"] = {"username": username}

    msg = bot.send_message(message.chat.id, "Введите дату окончания админки в формате ДД.ММ.ГГГГ:")
    bot.register_next_step_handler(msg, process_expiry_step)


def process_expiry_step(message):
    if check_for_start(message):
        return

    date_str = message.text.strip()
    try:
        expiry_date = datetime.strptime(date_str, "%d.%m.%Y").date()
        username = user_states["pending_admin"]["username"]
        del user_states["pending_admin"]

        admins = load_admins()
        admins[username] = {"expiry": expiry_date.isoformat()}
        save_admins(admins)

        bot.send_message(message.chat.id, f"✅ Админ <b>@{username}</b> назначен до <b>{expiry_date}</b>.",
                         parse_mode='HTML')
        bot.send_message(message.chat.id, "Меню управления:", reply_markup=admin_main_menu())
        log(f"Админ @{username} назначен до {expiry_date}")
    except ValueError:
        bot.send_message(message.chat.id, "❌ Неверный формат даты. Попробуйте снова.")
        msg = bot.send_message(message.chat.id, "Введите дату окончания админки в формате ДД.ММ.ГГГГ:")
        bot.register_next_step_handler(msg, process_expiry_step)
    except Exception as e:
        log(f"Ошибка при назначении админа: {e}")


# === СНЯТИЕ АДМИНА ===
@bot.callback_query_handler(func=lambda call: call.data == "remove_admin")
def ask_remove_username(call):
    if not is_owner(call.from_user):
        bot.answer_callback_query(call.id, "⛔ Доступ запрещён.", show_alert=True)
        return
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    msg = bot.send_message(call.message.chat.id, "Введите юзернейм админа:")
    bot.register_next_step_handler(msg, remove_admin_manually)


def remove_admin_manually(message):
    if check_for_start(message):
        return

    username = message.text.strip().lstrip('@')
    if not username:
        bot.send_message(message.chat.id, "❌ Юзернейм не может быть пустым.", parse_mode='HTML')
        bot.send_message(message.chat.id, "Меню управления:", reply_markup=admin_main_menu())
        return

    admins = load_admins()
    if username not in admins:
        bot.send_message(message.chat.id, "❌ Такого админа нет.", parse_mode='HTML')
        bot.send_message(message.chat.id, "Меню управления:", reply_markup=admin_main_menu())
        return

    user_id = admins[username].get('user_id')
    del admins[username]
    save_admins(admins)

    bot.send_message(message.chat.id, f"✅ Админ <b>@{username}</b> снят.", parse_mode='HTML')
    bot.send_message(message.chat.id, "Меню управления:", reply_markup=admin_main_menu())

    if user_id:
        try:
            bot.send_message(user_id, f"🔐 {OWNER_USERNAME} снял вас с админки", parse_mode='HTML')
        except Exception as e:
            log(f"Не удалось уведомить @{username}: {e}")

    log(f"Админ @{username} снят владельцем")


# === ПРОСМОТР АДМИНОВ ===
@bot.callback_query_handler(func=lambda call: call.data == "list_admins")
def list_admins(call):
    if not is_owner(call.from_user):
        bot.answer_callback_query(call.id, "⛔ Доступ запрещён.", show_alert=True)
        return
    admins = load_admins()
    if not admins:
        bot.send_message(call.message.chat.id, "📋 Список админов пуст.", parse_mode='HTML')
        bot.send_message(call.message.chat.id, "Меню управления:", reply_markup=admin_main_menu())
        return

    text = "<b>Список админов:</b>\n\n"
    for uname, data in admins.items():
        try:
            expiry = datetime.fromisoformat(data["expiry"]).date()
            # Убираем пометки "Активен" и "Просрочен" - оставляем только дату
            text += f"• @{uname} — до <code>{expiry}</code>\n"
        except Exception as e:
            log(f"Ошибка при отображении @{uname}: {e}")
            text += f"• @{uname} — ❌ Ошибка даты\n"

    bot.send_message(call.message.chat.id, text, parse_mode='HTML')
    bot.send_message(call.message.chat.id, "Меню управления:", reply_markup=admin_main_menu())


# === ВЕРНУТЬСЯ В ГЛАВНОЕ МЕНЮ ===
@bot.callback_query_handler(func=lambda call: call.data == "back_to_main")
def back_to_main(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    main_menu(call.message.chat.id, call.from_user)
    bot.answer_callback_query(call.id)


# === ОБРАБОТКА ГЛАВНОГО МЕНЮ (открыть/закрыть набор) ===
@bot.callback_query_handler(func=lambda call: call.data in ["open_set", "close_set"])
def menu_handler(call):
    if not is_admin(call.from_user):
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        bot.send_message(call.message.chat.id, f"🔐Упс, у вас нет доступа к боту!\nМожете приобрести доступ у {OWNER_USERNAME}", parse_mode='HTML')
        return

    username = get_username(call.from_user)

    # --- ОТКРЫТЬ НАБОР ---
    if call.data == "open_set":
        if username in active_sets:
            bot.answer_callback_query(call.id, "У вас уже есть открытый набор. Сначала закройте его.", show_alert=True)
            return

        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        platforms = ["Авито", "Яндекс Карты", "Яндекс браузер", "2GIS", "Гугл Карты", "Другое"]
        markup = types.InlineKeyboardMarkup()
        for p in platforms:
            markup.add(types.InlineKeyboardButton(p, callback_data=f"platform_{p}"))
        bot.send_message(call.message.chat.id, "Выберите платформу:", reply_markup=markup)
        user_states[username] = {"step": "platform", "data": {}}
        bot.answer_callback_query(call.id)

    # --- ЗАКРЫТЬ НАБОР ---
    elif call.data == "close_set":
        if username not in active_sets:
            bot.answer_callback_query(call.id, "У вас нет открытого набора.", show_alert=True)
            return

        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        msg_id = active_sets[username]["msg_id"]

        try:
            bot.edit_message_text(
                "🔒 Набор закрыт, ожидайте следующие задания",
                chat_id=CHANNEL_ID, message_id=msg_id, parse_mode='HTML')
        except Exception as e:
            log(f"Ошибка при редактировании сообщения: {e}")

        del active_sets[username]
        bot.send_message(call.message.chat.id, "Ваш набор был закрыт.")
        main_menu(call.message.chat.id, call.from_user)
        bot.answer_callback_query(call.id)


# --- ОБРАБОТКА ПЛАТФОРМЫ ---
@bot.callback_query_handler(func=lambda call: call.data.startswith("platform_"))
def platform_handler(call):
    if not is_admin(call.from_user):
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        bot.send_message(call.message.chat.id,
                         f"🔐Упс, у вас нет доступа к боту!\nМожете приобрести доступ у {OWNER_USERNAME}",
                         parse_mode='HTML')
        return

    username = get_username(call.from_user)
    if username not in user_states or user_states[username]["step"] != "platform":
        return

    platform = call.data.split("platform_", 1)[1]
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

    if platform.lower() == "другое":
        bot.send_message(call.message.chat.id, "Введите название платформы:")
        user_states[username]["step"] = "platform_custom"
    else:
        user_states[username]["data"]["platform"] = platform
        bot.send_message(call.message.chat.id, "Введите оплату:")
        user_states[username]["step"] = "payment"

    bot.answer_callback_query(call.id)


# --- ВВОД ТЕКСТА — С ФИЛЬТРАЦИЕЙ КОМАНД ===
@bot.message_handler(func=lambda m: True)
def text_handler(message):
    if message.text == '/start':
        user_states.pop(get_username(message.from_user), None)
        start(message)
        return

    if message.text.startswith('/'):
        bot.send_message(message.chat.id, "Используйте /start, чтобы начать заново.")
        return

    username = get_username(message.from_user)

    if not is_admin(message.from_user):
        bot.send_message(message.chat.id,
                         f"🔐Упс, у вас нет доступа к боту!\nМожете приобрести доступ у {OWNER_USERNAME}",
                         parse_mode='HTML')
        return

    if username not in user_states:
        bot.send_message(message.chat.id, "⚠️ Кажется, бот не ожидал этого от вас. Если что, вот меню:")
        main_menu(message.chat.id, message.from_user)
        return

    step = user_states[username]["step"]

    if step == "platform_custom":
        user_states[username]["data"]["platform"] = message.text
        bot.send_message(message.chat.id, "Введите оплату:")
        user_states[username]["step"] = "payment"
        return

    if step == "payment":
        user_states[username]["data"]["payment"] = message.text
        bot.send_message(message.chat.id, "Введите описание:")
        user_states[username]["step"] = "description"
        return

    if step == "description":
        user_states[username]["data"]["description"] = message.text
        data = user_states[username]["data"]

        text_preview = (
            f"<b>• Платформа:</b> {html.escape(data['platform'])}\n"
            f"<b>• Оплата:</b> {html.escape(data['payment'])}\n"
            f"<b>• Описание:</b> {html.escape(data['description'])}\n"
            f"<b>• Выдаст:</b> @{username}"
        )

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ Да", callback_data="confirm_yes"))
        markup.add(types.InlineKeyboardButton("❌ Нет", callback_data="confirm_no"))

        bot.send_message(message.chat.id, text_preview, reply_markup=markup, parse_mode="HTML")
        user_states[username]["step"] = "confirm"
        return

    # Сброс при неизвестном шаге
    bot.send_message(message.chat.id, "❌ Ошибка состояния. Начните сначала.")
    user_states.pop(username, None)


# --- ПОДТВЕРЖДЕНИЕ ---
@bot.callback_query_handler(func=lambda call: call.data in ["confirm_yes", "confirm_no"])
def confirm_handler(call):
    username = get_username(call.from_user)
    if not is_admin(call.from_user):
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        bot.send_message(call.message.chat.id,
                         f"🔐Упс, у вас нет доступа к боту!\nМожете приобрести доступ у {OWNER_USERNAME}",
                         parse_mode='HTML')
        return

    if username not in user_states or user_states[username]["step"] != "confirm":
        return

    data = user_states[username]["data"]

    if call.data == "confirm_yes":
        markup = types.InlineKeyboardMarkup()
        markup.row(types.InlineKeyboardButton("Взять задание", url=f"https://t.me/{username}"))
        markup.row(types.InlineKeyboardButton("Как начать?", url="https://t.me/instructionsream"), types.InlineKeyboardButton("Выплаты", url="https://t.me/bulwjf"))

        text_publish = (
            f"<b>• Платформа:</b> {html.escape(data['platform'])}\n"
            f"<b>• Оплата:</b> {html.escape(data['payment'])}\n"
            f"<b>• Описание:</b> {html.escape(data['description'])}\n"
            f"<b>• Выдаст:</b> @{username}"
        )
        msg = bot.send_message(CHANNEL_ID, text_publish, parse_mode="HTML", disable_web_page_preview=True,
                               reply_markup=markup)

        active_sets[username] = {
            "platform": data['platform'],
            "payment": data['payment'],
            "description": data['description'],
            "msg_id": msg.message_id
        }

        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        bot.send_message(call.message.chat.id, "Набор опубликован в канал.")

    else:
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        bot.send_message(call.message.chat.id, "Открытие набора отменено.")

    user_states.pop(username, None)
    main_menu(call.message.chat.id, call.from_user)
    bot.answer_callback_query(call.id)


# === АВТОМАТИЧЕСКОЕ УДАЛЕНИЕ ПО ИСТЕЧЕНИИ СРОКА И НАПОМИНАНИЕ ЗА 1 ДЕНЬ ===
def check_expired_admins():
    now = datetime.now()
    check_time_obj = datetime.strptime(CHECK_TIME, "%H:%M").time()
    current_datetime = now
    current_date = now.date()
    log(f"Проверка истёкших админов и напоминаний...")
    try:
        admins = load_admins()
        removed = []
        notified_expired = []
        notified_soon = []

        for username, data in list(admins.items()):
            try:
                expiry_date = datetime.fromisoformat(data["expiry"]).date()
                expiry_datetime = datetime.combine(expiry_date, check_time_obj)
                user_id = data.get('user_id')

                # Проверяем, истек ли срок с учетом времени CHECK_TIME
                if current_datetime >= expiry_datetime:
                    # Срок истёк в CHECK_TIME в дату снятия — удаляем
                    del admins[username]
                    removed.append(f"@{username}")
                    if user_id:
                        try:
                            bot.send_message(
                                user_id,
                                f"<b><u>Твоя админка закончилась⛔️</u></b>\nЧтобы продлить её, спроси есть ли места у {OWNER_USERNAME}",
                                parse_mode='HTML'
                            )
                            notified_expired.append(f"@{username}")
                        except Exception as e:
                            log(f"Не удалось уведомить @{username}: {e}")
                else:
                    # Проверяем, нужно ли отправить напоминание за 1 день
                    reminder_date = expiry_date - timedelta(days=1)
                    if current_date == reminder_date:
                        # Отправляем напоминание за день до окончания
                        if user_id:
                            try:
                                bot.send_message(
                                    user_id,
                                    f"<b>Привет 👋</b>\nЗавтра в {CHECK_TIME} по МСК у тебя  заканчивается админка. Чтобы не потерять свое место, не забудь продлить ее.\n> {OWNER_USERNAME}",
                                    parse_mode='HTML'
                                )
                                notified_soon.append(f"@{username}")
                            except Exception as e:
                                log(f"Не удалось отправить напоминание @{username}: {e}")

            except Exception as e:
                log(f"Ошибка при обработке @{username}: {e}")

        # Сохраняем изменения (если кто-то удалён)
        if removed:
            save_admins(admins)

        # Отправляем отчёты владельцам
        for owner_id in OWNER_IDS:
            try:
                msg_parts = []
                if removed:
                    msg_parts.append("⛔ <b>Админы сняты (срок истёк):</b>\n" + "\n".join(removed))
                if notified_soon:
                    msg_parts.append(
                        "🔔 <b>Напоминание отправлено (заканчивается завтра):</b>\n" + "\n".join(notified_soon))
                if notified_expired:
                    msg_parts.append("📩 <b>Уведомлены о снятии:</b> " + ", ".join(notified_expired))

                if msg_parts:
                    bot.send_message(owner_id, "\n\n".join(msg_parts), parse_mode='HTML')
                else:
                    log("Нет активных событий для владельцев")

            except Exception as e:
                log(f"Не удалось уведомить владельца {owner_id}: {e}")

        if removed:
            log(f"Сняты: {', '.join(removed)}")
        if notified_soon:
            log(f"Напоминания отправлены: {', '.join(notified_soon)}")
        if not removed and not notified_soon:
            log("Нет админов с истёкшим или завершающимся сроком")

    except Exception as e:
        log(f"Критическая ошибка в check_expired_admins: {e}")


# === ЗАПУСК ПЛАНИРОВЩИКА ===
def scheduler():
    schedule.every().day.at(CHECK_TIME).do(check_expired_admins)
    log(f"Запланирована проверка в {CHECK_TIME}")
    while True:
        schedule.run_pending()
        time.sleep(1)


# === ЗАПУСК БОТА ===
if __name__ == '__main__':
    if not os.path.exists(ADMIN_FILE):
        save_admins({})
        log(f"Создан файл {ADMIN_FILE}")

    threading.Thread(target=scheduler, daemon=True).start()
    log(f"Бот запущен. Проверка в {CHECK_TIME} по МСК.")

    bot.infinity_polling(timeout=10, long_polling_timeout=5)


