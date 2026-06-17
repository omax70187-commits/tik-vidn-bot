import os

from telegram import Update
from telegram.ext import (
Application,
CommandHandler,
ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")

watched_users = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text(
"Bot TikTok Recorder activo."
)

async def monitor(update: Update, context: ContextTypes.DEFAULT_TYPE):
if not context.args:
await update.message.reply_text(
"Uso: /monitor usuario"
)
return

```
username = context.args[0]

if username not in watched_users:
    watched_users.append(username)

await update.message.reply_text(
    f"Ahora vigilando: {username}"
)
```

async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
if not watched_users:
await update.message.reply_text(
"No hay usuarios vigilados."
)
return

```
text = "Usuarios vigilados:\n\n"

for user in watched_users:
    text += f"- {user}\n"

await update.message.reply_text(text)
```

async def record(update: Update, context: ContextTypes.DEFAULT_TYPE):
if not context.args:
await update.message.reply_text(
"Uso: /record usuario"
)
return

```
username = context.args[0]

await update.message.reply_text(
    f"Grabación manual solicitada para: {username}"
)
```

def main():
if not TOKEN:
raise Exception("BOT_TOKEN no encontrado")

```
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("monitor", monitor))
app.add_handler(CommandHandler("record", record))
app.add_handler(CommandHandler("list", list_users))

print("Bot iniciado...")
app.run_polling()
```

if **name** == "**main**":
main()
