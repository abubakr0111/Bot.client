import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = '8003016348:AAGlIdYJaNXUdibbJgr5G6CwoSpEnWEsMlE'  # <-- вставь сюда свой токен

# Главное меню с кнопками
main_menu = ReplyKeyboardMarkup(
    [['🤖 О нас', '💱 Курс'], ['✅ AML проверка', '🛠 Связаться']],
    resize_keyboard=True
)

# Приветственное сообщение при /start
start_text = """Добро пожаловать в Mosca!

📍 Москва, Пресненская набережная 12, Башня Федерация. Восток, этаж 11

📅 Мы работаем для вас 24/7. Без обеда и выходных.

💵 Мы работаем только за наличные рубли.

💹 Самый низкий курс на покупку USDT и лучший курс покупки USDT в Москве.

🤑 Отсутствие каких-либо комиссий на покупку и продажу USDT

Для покупки USDT нажмите на кнопку "Обмен"
"""

# Функция получения курса USDT к RUB с CoinGecko
def get_usdt_rub_rate():
url = 'https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies=rub'
response = requests.get(url)
print(response.status_code)
print(response.text)

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(start_text, reply_markup=main_menu)

# Обработчик текстовых сообщений и кнопок
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
Продать 1 USDT = {rate - 1:.2f} RUB  примерно на 1 рубль ниже покупки

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

# Создаем и запускаем приложение
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message_handler))

print("Бот запущен!")
app.run_polling()
