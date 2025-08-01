# main.py
import os
import requests
from flask import Flask, request
from signal_generator import get_latest_signal
from market_utils import get_market_summary

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("OWNER_ID")

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Crypto Signal Bot is Live with Webhook!"

@app.route(f"/<token>", methods=["POST"])
def webhook(token):
    if token != TOKEN:
        return "Unauthorized", 403

    data = request.get_json()
    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "")

    if text == "/status":
        reply = "✅ Bot is Active and Monitoring the Market..."
    elif text == "/lastsignal":
        reply = get_latest_signal()
    elif text == "/market":
        reply = get_market_summary()
    elif text == "/help":
        reply = (
            "📘 *Crypto Signal Bot Commands:*\n"
            "/status - Check bot status\n"
            "/lastsignal - Show last trade signal\n"
            "/market - Live prices + deviation\n"
            "/help - Show this help message"
        )
    else:
        reply = "❌ Unknown command. Use /help to see options."

    send_message(chat_id, reply)
    return "", 200

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
