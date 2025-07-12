import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TELEGRAM_TOKEN = "8086289161:AAGKtcTq5as5McAIpyH4ySoNlNnLfoqSNEc"
JINA_API_KEY = "jina_44965e7977484c169bb41699c973e74e3vh_2p8yF-z1q66GSiReMZ5UHmye"

logging.basicConfig(level=logging.INFO)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if not url.startswith("http"):
        await update.message.reply_text("שלח לי קישור למאמר 😊")
        return

    await update.message.reply_text("🔍 קורא את המאמר...")

    try:
        response = requests.post(
            "https://api.jina.ai/v1/reader/task",
            headers={
                "Authorization": f"Bearer {JINA_API_KEY}",
                "Content-Type": "application/json"
            },
            json={"input": url}
        )
        content = response.json().get("output", "")
        if not content:
            raise Exception("לא נמצא תוכן.")

        await update.message.reply_text(f"📄 סיכום:

{content[:4000]}")
    except Exception as e:
        logging.error(e)
        await update.message.reply_text("❌ שגיאה בקריאת המאמר.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
