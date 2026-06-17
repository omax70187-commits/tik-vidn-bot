import os

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

print("=== INICIO ===")
print("BOT_TOKEN =", os.getenv("BOT_TOKEN"))

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot TikTok Recorder activo.")

def main():
    if not TOKEN:
        raise Exception("BOT_TOKEN no fue encontrado en Railway")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot iniciado...")
    app.run_polling()

if __name__ == "__main__":
    main()
