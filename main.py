import os, hashlib, hmac, json
from fastapi import FastAPI, Request, HTTPException
import httpx

# --- Env ---
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
CHAT_ID   = os.getenv("OWNER_CHAT_ID", "")   # optional: apna Telegram user id
SECRET    = os.getenv("WEBHOOK_SECRET", "supersecret")  # webhook path secret
API_URL   = f"https://api.telegram.org/bot{BOT_TOKEN}"

if not BOT_TOKEN:
    raise RuntimeError("Set BOT_TOKEN env var")

app = FastAPI()

@app.get("/")
async def health():
    return {"ok": True, "service": "telegram-bot", "webhook": f"/webhook/{SECRET}"}

async def tg_send(chat_id: str, text: str):
    async with httpx.AsyncClient(timeout=10) as client:
        await client.post(f"{API_URL}/sendMessage", json={"chat_id": chat_id, "text": text})

@app.post(f"/webhook/{{secret:path}}")
async def webhook(secret: str, request: Request):
    # 405/404 problems usually due to wrong path — this ensures secret must match
    if secret != SECRET:
        raise HTTPException(status_code=404, detail="Not found")

    update = await request.json()

    # Basic message handler
    msg = update.get("message") or update.get("edited_message")
    if msg:
        chat_id = msg["chat"]["id"]
        text = (msg.get("text") or "").strip()

        if text.lower().startswith("/start"):
            await tg_send(chat_id, "Bot is live ✅\nCommands: /status, /help")
        elif text.lower().startswith("/status"):
            await tg_send(chat_id, "Status: ✅ Running on Render (webhook).")
        elif text.lower().startswith("/help"):
            await tg_send(chat_id, "Use /status to check bot. This is a minimal FastAPI webhook.")
        else:
            await tg_send(chat_id, f"You said: {text}")

    # Optional: handle callback_query etc.
    cq = update.get("callback_query")
    if cq:
        chat_id = cq["message"]["chat"]["id"]
        await tg_send(chat_id, "Callback received.")

    return {"ok": True}
