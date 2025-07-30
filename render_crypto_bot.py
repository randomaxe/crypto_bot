
import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from flask import Flask

# Flask-сервер для поддержания активности Render.com
web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "Bot is running!"

def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        return float(data["price"])
    except Exception as e:
        print(f"Ошибка получения цены: {e}")
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот, показывающий курсы криптовалют с Binance.\n"
        "Команды:\n"
        "/btc — курс Bitcoin (BTC/USDT)\n"
        "/eth — курс Ethereum (ETH/USDT)\n"
        "/usdt — курс USDT к тенге (USDT/KZT)"
    )

async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = get_price("BTCUSDT")
    if price:
        await update.message.reply_text(f"Курс Bitcoin: ${price}")
    else:
        await update.message.reply_text("Не удалось получить курс BTC.")

async def eth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = get_price("ETHUSDT")
    if price:
        await update.message.reply_text(f"Курс Ethereum: ${price}")
    else:
        await update.message.reply_text("Не удалось получить курс ETH.")

async def usdt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = get_price("USDTKZT")
    if price:
        await update.message.reply_text(f"Курс USDT к KZT: {round(price, 2)} ₸")
    else:
        await update.message.reply_text("Не удалось получить курс USDT к KZT.")

# Токен бота
TOKEN = os.getenv("BOT_TOKEN", "7987485172:AAGsujvykcRJMvNNjH3QGFLCYqtouwuE6CE")

# Telegram-бот
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("btc", btc))
app.add_handler(CommandHandler("eth", eth))
app.add_handler(CommandHandler("usdt", usdt))

# Запуск Telegram-бота в фоне
import threading
threading.Thread(target=app.run_polling, daemon=True).start()

# Запуск Flask-сервера
if __name__ == "__main__":
    web_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
