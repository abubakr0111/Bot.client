from flask import Flask
import asyncio
import threading
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update

# Flask-приложение
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Бот работает!"

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я работаю 💥")

# Функция для запуска Telegram-бота
def run_telegram_bot():
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()

    # Создаём Telegram приложение
    application = Application.builder().token("YOUR_BOT_TOKEN").build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))

    # Запускаем polling внутри event loop
    loop.run_until_complete(application.run_polling())

# Главная точка входа
if __name__ == "__main__":
    # Запускаем Telegram бота в отдельном потоке
    threading.Thread(target=run_telegram_bot).start()

    # Запускаем Flask-сервер
    flask_app.run(host="0.0.0.0", port=10000)
