import os
from flask import Flask, request
import telegram
from telegram.ext import Dispatcher, CommandHandler
from utils import get_market_summary, get_live_signals

TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = os.getenv("OWNER_ID")  # use consistent env var
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

# Telegram command handlers
def start(update, context):
    update.message.reply_text("👋 Welcome to Crypto Signal Bot!")

def help_cmd(update, context):
    update.message.reply_text("/status, /market, /lastsignal")

def status(update, context):
    update.message.reply_text("✅ Bot is running")

def last_signal(update, context):
    signal = get_live_signals()
    update.message.reply_text(signal or "No signal right now")

def market(update, context):
    summary = get_market_summary()
    update.message.reply_text(summary or "Error fetching market data")

# Setup dispatcher
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_cmd))
dispatcher.add_handler(CommandHandler("status", status))
dispatcher.add_handler(CommandHandler("lastsignal", last_signal))
dispatcher.add_handler(CommandHandler("market", market))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/", methods=["GET"])
def root():
    return "✅ Crypto Signal Bot is Live"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))


