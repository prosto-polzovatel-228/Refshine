import telebot
from telebot import types
import html
import json
import os
import threading

# ================== БОТ 1: [Arzara] ==================
BOT1_CONFIG = {
    "API_TOKEN": "8465314986:AAFKMeiEZJjCFCVRWouq3i7bgTSMlQb9bT8",
    "CHANNEL_ID": -1001918784178,
    "ADMINS_FILE": "admins_arzara.json",
    "OWNERS": ["necalculator", "amiwwni", "amiwwnii", "arzaramanager"],
    "ADMINS_DEFAULT": ["Matvey_Gribochek"],
    "BOT_PREFIX": "arzara",
    "TEXTS": {
        "start_denied": "⛔ Чтобы публиковать задания в канал, напишите @amiwwni",
        "set_closed": (
            "<b>✅ Данное задание завершено, набор закрыт.</b> \n\n"
            "<b>🔔 Не упустите возможности получить новое! Рекомендуем включить уведомления.</b>"
        ),
        "set_opened": (
            "<b>📝 НОВОЕ ЗАДАНИЕ</b>\n\n"
            "🌐 Платформа: {platform}\n"
            "📋 Описание: {description}\n"
            "💰 Вознаграждение: {payment}\n"
            "🤝 Задание выдаст: @{username}\n\n"
            "••• ━───── • • ─────━ •••\n"
            "჻︎ Наши выплаты – @arzarapayments\n"
            "჻︎ Обучение – @arzaratutorial"
        ),
    },
    "BUTTONS": {
        "channel_opened": [
            [
            {"text": "Взять задание", "url": "https://t.me/{username}"}
            ],
            [
            {"text": "Обучение", "url": "https://t.me/Arzaratutorial/27"},
            {"text": "Выплаты", "url": "https://t.me/arzarapayments"}
            ]
        ],
        "channel_closed": [
            {"text": "Обучение", "url": "https://t.me/Arzaratutorial"},
            {"text": "Выплаты", "url": "https://t.me/arzarapayments"}
        ]
    }
}

# ================== БОТ 2: [Stream] ==================
BOT2_CONFIG = {
    "API_TOKEN": "8474324716:AAHASDeYq74HOpwAOMGwznZC5wIvK61DZfw",
    "CHANNEL_ID": -1001527165475,
    "ADMINS_FILE": "admins_stream.json",
    "OWNERS": ["necalculator", "elenesing"],
    "ADMINS_DEFAULT": ["username"],
    "BOT_PREFIX": "stream",
    "TEXTS": {
        "start_denied": "⛔ Чтобы публиковать задания в канал, напишите @elenesing",
        "set_closed": (
            "🔒 Набор закрыт, ожидайте следующие задания ❗️"
        ),
        "set_opened": (
            "<b>• Платформа:</b> {platform}\n"
            "<b>• Оплата:</b> {payment}\n"
            "<b>• Описание:</b> {description}\n"
        ),
    },
    "BUTTONS": {
        "channel_opened": [
            [
                {"text": "Взять задание", "url": "https://t.me/{username}"}
            ],
            [
            {"text": "Обучение", "url": "https://t.me/moneyjdjdj"},
            {"text": "Выплаты", "url": "https://t.me/Sweramd"}
            ]
        ],
        "channel_closed": [
            [
            {"text": "Обучение", "url": "https://t.me/moneyjdjdj"},
            {"text": "Выплаты", "url": "https://t.me/Sweramd"}
            ]
        ]
    }
}

# ================== БОТ 3: [Moony] ==================
BOT3_CONFIG = {
    "API_TOKEN": "8583249222:AAE-ucOn4-Lj8m23xEJOfbY1O2qfgTykNYk",
    "CHANNEL_ID": -1002241094762,
    "ADMINS_FILE": "admins_moony.json",
    "OWNERS": ["necalculator", "hikka149"],
    "ADMINS_DEFAULT": ["username"],
    "BOT_PREFIX": "moony",
    "TEXTS": {
        "start_denied": "⛔ Чтобы публиковать задания в канал, напишите @hikka149",
        "set_closed": (
            "<b>🌕Набор окончен! Задание завершено</b>\n"
            "<blockquote>Если не успеваешь брать задания, включи <b>уведомления</b>\n"
            "<a href='https://t.me/livpon'><b>🌼Как приступить к заданию</b></a></blockquote>"
        ),
        "set_opened": (
            "<b>🌎НОВОЕ ЗАДАНИЕ</b>\n\n"
            "📲Платформа:\n{platform}\n"
            "👒Оплата: {payment}\n"
            "📝Описание: {description}\n"
        ),
    },
    "BUTTONS": {
        "channel_opened": [
            [
                {"text": "Взять задание", "url": "https://t.me/{username}"}
            ],
            [
            {"text": "Обучение", "url": "https://t.me/livpon/26"},
            {"text": "Выплаты", "url": "https://t.me/viplota_lox"}
            ]
        ],
        "channel_closed": [
            [
            {"text": "Обучение", "url": "https://t.me/livpon/26"},
            {"text": "Выплаты", "url": "https://t.me/viplota_lox"}
            ]
        ]
    }
}

# ================== БОТ 4: [Guru] ==================
# BOT4_CONFIG = {
#     "API_TOKEN": "8474324716:AAHASDeYq74HOpwAOMGwznZC5wIvK61DZfw",
#     "CHANNEL_ID": -1002032117087,
#     "ADMINS_FILE": "admins_guru.json",
#     "OWNERS": ["necalculator", "Hype_hab"],
#     "ADMINS_DEFAULT": ["username"],
#     "BOT_PREFIX": "guru",
#     "TEXTS": {
#         "start_denied": "⛔ Чтобы публиковать задания в канал, напишите @Hype_hab",
#         "set_closed": (
#             "🔒 Набор закрыт, ожидайте следующие задания ❗️"
#         ),
#         "set_opened": (
#             "<b>• Платформа:</b> {platform}\n"
#             "<b>• Оплата:</b> {payment}\n"
#             "<b>• Описание:</b> {description}\n"
#         ),
#     },
#     "BUTTONS": {
#         "channel_opened": [
#             [
#                 {"text": "Взять задание", "url": "https://t.me/{username}"}
#             ],
#             [
#             {"text": "Обучение", "url": "https://t.me/Hamer_goto"},
#             {"text": "Выплаты", "url": "https://t.me/Sweramd"}
#             ]
#         ],
#         "channel_closed": [
#             [
#             {"text": "Обучение", "url": "https://t.me/Hamer_goto"},
#             {"text": "Выплаты", "url": "https://t.me/Sweramd"}
#             ]
#         ]
#     }
# }

# ------------------ Класс для управления ботом ------------------
class TaskBot:
    def __init__(self, config):
        self.config = config
        self.bot = telebot.TeleBot(config["API_TOKEN"])

        # Переменные состояния
        self.active_sets = {}
        self.user_states = {}

        # Загрузка админов
        self.ADMINS = self.load_admins()
        self.OWNERS = config["OWNERS"]

        # Регистрация обработчиков
        self.register_handlers()

    def load_admins(self):
        filename = self.config["ADMINS_FILE"]
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            default_admins = self.config["ADMINS_DEFAULT"]
            self.save_admins(default_admins)
            return default_admins

    def save_admins(self, admins_list):
        with open(self.config["ADMINS_FILE"], "w", encoding="utf-8") as f:
            json.dump(admins_list, f, ensure_ascii=False, indent=4)

    def is_admin(self, user):
        return (user and user.username) and (user.username in self.ADMINS or user.username in self.OWNERS)

    def is_owner(self, user):
        return (user and user.username) and (user.username in self.OWNERS)

    def get_username(self, user):
        return user.username if user and user.username else f"id_{user.id}"

    def main_menu(self, chat_id, user=None):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📂 Открыть набор", callback_data="open_set"))
        markup.add(types.InlineKeyboardButton("❌ Закрыть набор", callback_data="close_set"))
        if user and self.is_owner(user):
            markup.add(types.InlineKeyboardButton("⚙️ Управление админами", callback_data="edit_admins"))

        # Добавляем дополнительные кнопки из конфига
        for btn in self.config["BUTTONS"].get("main_menu", []):
            markup.add(types.InlineKeyboardButton(btn["text"], url=btn["url"]))

        self.bot.send_message(chat_id, "Главное меню:", reply_markup=markup)

    def register_handlers(self):
        # --- START ---
        @self.bot.message_handler(commands=["start"])
        def start_cmd(message):
            if not self.is_admin(message.from_user):
                self.bot.send_message(message.chat.id, self.config["TEXTS"]["start_denied"], parse_mode="HTML")
                return
            self.main_menu(message.chat.id, message.from_user)

        # --- КНОПКИ: открыть/закрыть набор ---
        @self.bot.callback_query_handler(func=lambda call: call.data in ["open_set", "close_set"])
        def menu_handler(call):
            if not self.is_admin(call.from_user):
                self.bot.answer_callback_query(call.id, "⛔ Доступ запрещён.", show_alert=True)
                return

            username = self.get_username(call.from_user)

            if call.data == "open_set":
                if username in self.active_sets:
                    self.bot.answer_callback_query(call.id, "У вас уже есть открытый набор. Сначала закройте его.", show_alert=True)
                    return

                self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
                platforms = ["Авито", "Яндекс Карты", "Яндекс браузер", "2GIS", "Гугл Карты", "Другое"]
                markup = types.InlineKeyboardMarkup()
                for p in platforms:
                    markup.add(types.InlineKeyboardButton(p, callback_data=f"platform_{p}"))
                self.bot.send_message(call.message.chat.id, "Выберите платформу:", reply_markup=markup)
                self.user_states[username] = {"step": "platform", "data": {}}
                self.bot.answer_callback_query(call.id)


            elif call.data == "close_set":

                if username not in self.active_sets:
                    self.bot.answer_callback_query(call.id, "У вас нет открытого набора.", show_alert=True)

                    return

                self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

                msg_id = self.active_sets[username]["msg_id"]

                try:

                    extra_buttons = self.config["BUTTONS"].get("channel_closed", [])

                    markup = None

                    if extra_buttons:

                        markup = types.InlineKeyboardMarkup()

                        for row in extra_buttons:  # row — список кнопок

                            buttons_in_row = []

                            for btn in row:
                                # Форматируем URL, если нужно

                                url = btn["url"].format(username=username)

                                buttons_in_row.append(

                                    types.InlineKeyboardButton(btn["text"], url=url)

                                )

                            markup.row(*buttons_in_row)

                    # Редактируем сообщение

                    self.bot.edit_message_text(

                        self.config["TEXTS"]["set_closed"],

                        chat_id=self.config["CHANNEL_ID"],

                        message_id=msg_id,

                        reply_markup=markup,

                        parse_mode="HTML",

                        disable_web_page_preview=True

                    )


                except Exception as e:

                    print(f"[{self.config['BOT_PREFIX']}] Ошибка при редактировании сообщения: {e}")

                    self.bot.send_message(call.message.chat.id, f"❌ Не удалось обновить сообщение: {e}")

                del self.active_sets[username]

                self.bot.send_message(call.message.chat.id, "✅ Ваш набор был закрыт")

                self.main_menu(call.message.chat.id, call.from_user)

                self.bot.answer_callback_query(call.id)

        # --- Выбор платформы ---
        @self.bot.callback_query_handler(func=lambda call: call.data.startswith("platform_"))
        def platform_handler(call):
            if not self.is_admin(call.from_user):
                self.bot.answer_callback_query(call.id, "⛔ Доступ запрещён.", show_alert=True)
                return

            username = self.get_username(call.from_user)
            if username not in self.user_states or self.user_states[username]["step"] != "platform":
                self.bot.answer_callback_query(call.id)
                return

            platform = call.data.split("platform_", 1)[1]
            self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

            if platform.lower() == "другое":
                self.bot.send_message(call.message.chat.id, "Введите название платформы:")
                self.user_states[username]["step"] = "platform_custom"
            else:
                self.user_states[username]["data"]["platform"] = platform
                self.bot.send_message(call.message.chat.id, "Введите оплату:")
                self.user_states[username]["step"] = "payment"

            self.bot.answer_callback_query(call.id)

        # --- Ввод текста ---
        @self.bot.message_handler(func=lambda m: True)
        def text_handler(message):
            username = self.get_username(message.from_user)

            # Обновление админов
            if username in self.user_states and self.user_states[username]["step"] == "update_admins":
                new_admins = [u.strip().lstrip("@") for u in message.text.split(",") if u.strip()]
                if new_admins:
                    self.ADMINS = new_admins
                    self.save_admins(new_admins)
                    self.bot.send_message(message.chat.id, f"Список админов обновлён: {', '.join('@' + a for a in new_admins)}")
                else:
                    self.bot.send_message(message.chat.id, "Что-то не так. Между юзернеймами должны быть запятые.")
                self.user_states.pop(username, None)
                return

            if not self.is_admin(message.from_user):
                return

            if username not in self.user_states:
                return

            step = self.user_states[username]["step"]

            if step == "platform_custom":
                self.user_states[username]["data"]["platform"] = message.text
                self.bot.send_message(message.chat.id, "Введите оплату:")
                self.user_states[username]["step"] = "payment"

            elif step == "payment":
                self.user_states[username]["data"]["payment"] = message.text
                self.bot.send_message(message.chat.id, "Введите описание:")
                self.user_states[username]["step"] = "description"

            elif step == "description":
                self.user_states[username]["data"]["description"] = message.text
                data = self.user_states[username]["data"]

                # Формируем текст предпросмотра
                text_preview = self.config["TEXTS"]["set_opened"].format(
                    platform=html.escape(data['platform']),
                    description=html.escape(data['description']),
                    payment=html.escape(data['payment']),
                    username=username
                )

                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("✅ Да", callback_data="confirm_yes"))
                markup.add(types.InlineKeyboardButton("❌ Нет", callback_data="confirm_no"))
                self.bot.send_message(message.chat.id, text_preview, reply_markup=markup, parse_mode="HTML")
                self.user_states[username]["step"] = "confirm"

        # --- Подтверждение ---
        @self.bot.callback_query_handler(func=lambda call: call.data in ["confirm_yes", "confirm_no"])
        def confirm_handler(call):
            username = self.get_username(call.from_user)
            if not self.is_admin(call.from_user):
                self.bot.answer_callback_query(call.id, "⛔ Доступ запрещён.", show_alert=True)
                return

            if username not in self.user_states or self.user_states[username]["step"] != "confirm":
                self.bot.answer_callback_query(call.id)
                return

            data = self.user_states[username]["data"]

            if call.data == "confirm_yes":
                # Формируем текст публикации
                text_publish = self.config["TEXTS"]["set_opened"].format(
                    platform=html.escape(data['platform']),
                    description=html.escape(data['description']),
                    payment=html.escape(data['payment']),
                    username=username
                )

                # Создаём кнопки
                markup = types.InlineKeyboardMarkup()
                for row in self.config["BUTTONS"]["channel_opened"]:
                    buttons_in_row = []
                    for btn in row:
                        buttons_in_row.append(
                            types.InlineKeyboardButton(
                                btn["text"],
                                url=btn["url"].format(username=username)
                            )
                        )
                    markup.row(*buttons_in_row)  # каждая строка — отдельный ряд кнопок

                try:
                    msg = self.bot.send_message(
                        self.config["CHANNEL_ID"],
                        text_publish,
                        parse_mode="HTML",
                        disable_web_page_preview=True,
                        reply_markup=markup
                    )
                    self.active_sets[username] = {
                        "platform": data['platform'],
                        "payment": data['payment'],
                        "description": data['description'],
                        "msg_id": msg.message_id
                    }
                    self.bot.send_message(call.message.chat.id, "✅ Набор опубликован в канал.")
                except Exception as e:
                    self.bot.send_message(call.message.chat.id, f"Ошибка публикации: {e}")
            else:
                self.bot.send_message(call.message.chat.id, "Открытие набора отменено.")

            # Очищаем состояние
            self.user_states.pop(username, None)
            self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
            self.main_menu(call.message.chat.id, call.from_user)
            self.bot.answer_callback_query(call.id)

        # --- Управление админами (для владельцев) ---
        @self.bot.callback_query_handler(func=lambda call: call.data == "edit_admins")
        def edit_admins_handler(call):
            username = self.get_username(call.from_user)
            if not self.is_owner(call.from_user):
                self.bot.answer_callback_query(call.id, "⛔ Это только для владельца. Как ты вообще сюда попал(-а)? 🧐", show_alert=True)
                return

            self.bot.send_message(call.message.chat.id, "Текущие админы:")
            self.bot.send_message(call.message.chat.id, f"{', '.join('@' + a for a in self.ADMINS)}")
            self.bot.send_message(call.message.chat.id, "Введите новый список админов через запятую:")
            self.user_states[username] = {"step": "update_admins"}
            self.bot.answer_callback_query(call.id)


# ================== ЗАПУСК ДВУХ БОТОВ ПАРАЛЛЕЛЬНО ==================
def run_bot(bot_instance, name):
    print(f"[{name}] Бот запущен...")
    bot_instance.bot.infinity_polling()


# Создаём ботов
bot1 = TaskBot(BOT1_CONFIG)
bot2 = TaskBot(BOT2_CONFIG)
bot3 = TaskBot(BOT3_CONFIG)
# bot4 = TaskBot(BOT4_CONFIG)

# Запускаем в потоках
thread1 = threading.Thread(target=run_bot, args=(bot1, "arzara"))
thread2 = threading.Thread(target=run_bot, args=(bot2, "stream"))
thread3 = threading.Thread(target=run_bot, args=(bot3, "moony"))
# thread4 = threading.Thread(target=run_bot, args=(bot4, "guru"))

thread1.start()
thread2.start()
thread3.start()
# thread4.start()

# Держим основной поток живым
try:
    thread1.join()
    thread2.join()
    thread3.join()
    # thread4.join()
except KeyboardInterrupt:
    print("Боты остановлены.")