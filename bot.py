import os

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text("Bot TikTok Recorder activo.")

def main():
if not TOKEN:
raise Exception("BOT_TOKEN no encontrado")

```
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

print("Bot iniciado...")
app.run_polling()
```

if **name** == "**main**":
main()
