import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
genai.configure(api_key=os.environ["GEMINI_KEY"])
TOKEN = os.environ["BOT_TOKEN"]
SYSTEM = "Du bist ein hilfreicher KI-Assistent. Du antwortest auf Deutsch, bist freundlich und direkt."
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hallo! Ich bin dein KI-Assistent. Schreib mir einfach!")
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash", system_instruction=SYSTEM)
        antwort = model.generate_content(update.message.text)
        await update.message.reply_text(antwort.text)
    except Exception as e:
        await update.message.reply_text(f"❌ Fehler: {str(e)}")
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot läuft...")
    app.run_polling()
if __name__ == "__main__":
    main()
