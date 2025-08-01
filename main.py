import os
from flask import Flask, request
import telegram
from telegram.ext import Dispatcher, CommandHandler
from utils.market import get_market_summary
from utils.signal_generator import get_live_signals

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

# Handlers
def start(update, context): update.message.reply_text("👋 Welcome to Crypto Signal Bot!")
def help_cmd(update, context): update.message.reply_text("/status, /market, /lastsignal")
def status(update, context): update.message.reply_text("✅ Bot is running fine.")
def last_signal(update, context): update.message.reply_text(get_live_signals())
def market(update, context): update.message.reply_text(get_market_summary())

# Bind
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_cmd))
dispatcher.add_handler(CommandHandler("status", status))
dispatcher.add_handler(CommandHandler("lastsignal", last_signal))
dispatcher.add_handler(CommandHandler("market", market))

@app.route(f'/{TOKEN}', methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/", methods=["GET"])
def home(): return "✅ Crypto Signal Bot is Live!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
