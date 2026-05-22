import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from openai import OpenAI
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPENROUTER_KEY"])
TOKEN = os.environ["BOT_TOKEN"]
SYSTEM = "Du bist ein hilfreicher KI-Assistent. Du antwortest auf Deutsch, bist freundlich und direkt."
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hallo! Ich bin dein KI-Assistent. Schreib mir einfach!")
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        antwort = client.chat.completions.create(
            model="google/gemma-2-9b-it:free",
            messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": update.message.text}]
        )
        await update.message.reply_text(antwort.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text(f"❌ Fehler: {str(e)}")
def run_bot():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot läuft...")
    app.run_polling()
def run_http():
    server = HTTPServer(("0.0.0.0", int(os.environ.get("PORT", 10000))), HealthHandler)
    server.serve_forever()
threading.Thread(target=run_http, daemon=True).start()
run_bot()
