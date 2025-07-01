import requests
import time
import threading
from flask import Flask
import os

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# --- Telegram Bot Setup ---
TOKEN = '8003016348:AAGlIdYJaNXUdibbJgr5G6CwoSpEnWEsMlE'

cached_rate = None
last_fetched = 0

main_menu = ReplyKeyboardMarkup(
    [['🤖 О нас', '💱 Курс'], ['✅ AML проверка', '🛠 Связаться']],
    resize_keyboard=True
)

start_text = """Добро пожаловать в Mosca!

📍 Москва, Пресненская набережная 12, Башня Федерация. Восток, этаж 11
📅 Мы работаем для вас 24/7. Без обеда и выходных.
💵 Мы работаем только за наличные рубли.
💹 Самый низкий курс на покупку USDT и лучший курс покупки USDT в Москве.
🤑 Отсутствие каких-либо комиссий на покупку и продажу USDT

Для покупки USDT нажмите на кнопку "Обмен"
"""

def get_usdt_rub_rate():
    global cached_rate, last_fetched
    now = time.time()
    if cached_rate is not None and (now - last_fetched) < 60:
        return cached_rate
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies=rub')
        if response.status_code != 200:
            print(f"[HTTP Error]: {response.status_code}")
            return cached_rate
        data = response.json()
        rate = data.get('tether', {}).get('rub')
        if rate is not None:
            cached_rate = rate
            last_fetched = now
        return rate
    except Exception as e:
        print(f"[Ошибка парсинга курса]: {e}")
        return cached_rate

# --- Telegram Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(start_text, reply_markup=main_menu)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text

    if msg == '🤖 О нас':
        await update.message.reply_text("""Добро пожаловать в наш бот для обмена криптовалюты!
💰 Мы занимаемся обменом криптовалют более 3х лет.
📅 Мы работаем для вас 24/7.
💵 Мы работаем только за наличные рубли.
💹 У нас вы можете купить USDT без комиссии по самому лучшему курсу в Москве.  
Комиссия 3$ за вывод USDT в сети Tron.

Наш адрес: Москва, Пресненская набережная 12, Башня Федерация. Восток, этаж 11

Для получения пропуска к нам в офис и покупки USDT, вам нужно создать заявку через приложение""")

    elif msg == '💱 Курс':
        rate = get_usdt_rub_rate()
        if rate:
            await update.message.reply_text(f"""Курс USDT к RUB сейчас примерно:

Купить 1 USDT = {rate:.2f} RUB  
Продать 1 USDT = {rate - 1:.2f} RUB  (примерно на 1 рубль ниже покупки)

*данный курс является биржевым и меняется каждую минуту.

Комиссия 3$ за вывод USDT в сети Tron.

Для получения пропуска к нам в офис и покупки USDT, нажмите на кнопку "Обмен" """)
        else:
            await update.message.reply_text("Не удалось получить текущий курс. Попробуйте позже.")

    elif msg == '✅ AML проверка':
        await update.message.reply_text("🔎 Функция в разработке...")

    elif msg == '🛠 Связаться':
        await update.message.reply_text("""Наши операторы на связи 24/7 и готовы ответить на любые ваши вопросы.

Для связи с нами напишите — @Dolar_exchange_bot

Для получения пропуска к нам в офис и покупки USDT, нажмите на кнопку "Обмен"
""")
    else:
        await update.message.reply_text("Пожалуйста, выберите действие с помощью кнопок ниже.", reply_markup=main_menu)

# --- Telegram Bot Runner ---
def run_telegram_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message_handler))
    print("🤖 Бот запущен!")
    app.run_polling()

# --- Flask Stub for Render Web Service ---
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return '🟢 Бот работает. Render доволен.'

if __name__ == '__main__':
    # Запуск Telegram-бота в отдельном потоке
    bot_thread = threading.Thread(target=run_telegram_bot)
    bot_thread.start()

    # Запуск Flask-сервера (Render требует открытый порт!)
    port = int(os.environ.get('PORT', 10000))
    flask_app.run(host='0.0.0.0', port=port)
