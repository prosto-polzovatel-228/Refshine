import telebot
from telebot import types
import html
import pickle

# --- НАСТРОЙКИ ---
API_TOKEN = "8206130111:AAEHJrj59Q2ze1NeFeP0uKtPwp5FP1m9K9Q"
CHANNEL_ID = -1002720938276
GROUP_ID = -1003064412522

bot = telebot.TeleBot(API_TOKEN)

# Загружаем активные наборы
def load_active_sets():
    try:
        with open("sets_klin.pkl", "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return {}

active_sets = load_active_sets()

# Сохраняем активные наборы
def save_active_sets():
    with open("sets_klin.pkl", "wb") as f:
        pickle.dump(active_sets, f)

# Проверка: сообщение из нужной группы?
def is_target_group(message):
    return message.chat.id == GROUP_ID

# --- ОБРАБОТКА СООБЩЕНИЯ В ГРУППЕ ---
@bot.message_handler(content_types=['text'], func=lambda m: not m.text.startswith('/') and is_target_group(m))
def handle_set(message):
    username = message.from_user.username or f"id_{message.from_user.id}"

    # 🔒 Проверка: есть ли у пользователя уже открытый набор?
    if username in active_sets:
        bot.reply_to(message, "❌ У вас уже есть открытый набор. Сначала закройте его командой /close")
        return

    text = message.text.strip()
    lines = text.splitlines()

    if len(lines) < 3:
        bot.reply_to(message,
                     "Так не пойдёт. Мне нужно 3 строки:\n•Платформа\n•Оплата\n•Описание\n\n(Инструкция в закрепе)")
        return
    elif len(lines) > 3:
        bot.reply_to(message,
                     "Так не пойдёт. Мне нужно 3 строки:\n•Платформа\n•Оплата\n•Описание\n\n(Инструкция в закрепе)")
        return

    platform, payment, description = lines[:3]

    text_publish = (
        f"📊Площадка - {html.escape(platform)}\n"
        f"💵Оплата - {html.escape(payment)}\n"
        f"📩Описание - {html.escape(description)}\n"
        f"👨‍💻Писать: @{username}"
    )

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Обучение⚖", url="https://t.me/klin_faq")
    btn2 = types.InlineKeyboardButton(text="Выплаты💸", url="https://t.me/klin_oplata")
    btn3 = types.InlineKeyboardButton(text="Взять задание🙋", url=f"t.me/{username}")
    markup.row(btn1, btn2)
    markup.row(btn3)

    try:
        msg = bot.send_message(
            CHANNEL_ID,
            text_publish,
            parse_mode="HTML",
            disable_web_page_preview=True,
            reply_markup=markup
        )
        active_sets[username] = {"msg_id": msg.message_id}
        save_active_sets()
        bot.reply_to(message, "✅ Опубликовал")
    except Exception as e:
        bot.reply_to(message, f"😢 Что-то сломалось при попытке открыть набор. Отправьте это @necalculator, он починит. Ошибка: {e}")

# --- КОМАНДА /close (доступна везде, но логика — только свой набор) ---
@bot.message_handler(commands=['close'])
def handle_close(message):
    username = message.from_user.username or f"id_{message.from_user.id}"

    if username not in active_sets:
        bot.reply_to(message, "❌ У вас нет активного набора.")
        return

    msg_id = active_sets[username]["msg_id"]
    try:
        bot.edit_message_text(
            "🔒 Набор закрыт, ожидайте следующие задания",
            chat_id=CHANNEL_ID,
            message_id=msg_id
        )
        del active_sets[username]
        save_active_sets()
        bot.reply_to(message, "✅ Набор закрыт.")
    except Exception as e:
        bot.reply_to(message, f"😢 Что-то сломалось при попытке закрыть набор. Отправьте это @necalculator, он починит. Ошибка: {e}")

# --- ЗАПУСК ---
print("Бот запущен...")
bot.infinity_polling()