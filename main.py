import logging
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
from utils import get_signal_message, get_market_summary

TOKEN = '7612808640:AAEm0j8gL-6dswKPHCSqt7eMi4f0L0tbEys'
bot = Bot(token=TOKEN)
app = Flask(__name__)
dispatcher = Dispatcher(bot=bot, update_queue=None, workers=1, use_context=True)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='✅ Bot is Active and Monitoring...')

def help_cmd(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='/status – Bot live status'
/lastsignal - Last alert
/summary - Recent trades
/market - Live coin summary
/help - Command list')

def lastsignal(update, context):
    msg = get_signal_message()
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode='HTML')

def status(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='✅ Bot is Active and Monitoring...')

def market(update, context):
    summary = get_market_summary()
    context.bot.send_message(chat_id=update.effective_chat.id, text=summary, parse_mode='HTML')

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_cmd))
dispatcher.add_handler(CommandHandler("lastsignal", lastsignal))
dispatcher.add_handler(CommandHandler("status", status))
dispatcher.add_handler(CommandHandler("market", market))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/")
def index():
    return "Crypto Signal Bot is running."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
