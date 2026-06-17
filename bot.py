import os
import asyncio

from TikTokLive import TikTokLiveClient

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

print("=== INICIO ===")
print("BOT_TOKEN cargado correctamente")

watched_users = []
monitor_running = False

TOKEN = os.getenv("BOT_TOKEN")


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

    username = context.args[0]

    if username not in watched_users:
        watched_users.append(username)

    await update.message.reply_text(
        f"Ahora vigilando: {username}"
    )


async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not watched_users:
        await update.message.reply_text(
            "No hay usuarios vigilados."
        )
        return

    text = "Usuarios vigilados:\n\n"

    for user in watched_users:
        text += f"- {user}\n"

    await update.message.reply_text(text)


async def record(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Uso: /record usuario"
        )
        return

    username = context.args[0]

    if username not in watched_users:
        watched_users.append(username)

        await update.message.reply_text(
            f"Usuario {username} añadido a vigilancia.\n"
            f"Intentaré grabarlo cuando esté en vivo."
        )
    else:
        await update.message.reply_text(
            f"{username} ya está en vigilancia."
        )


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Uso: /stop usuario"
        )
        return

    username = context.args[0]

    if username in watched_users:
        watched_users.remove(username)

        await update.message.reply_text(
            f"{username} eliminado de vigilancia."
        )
    else:
        await update.message.reply_text(
            f"{username} no estaba en vigilancia."
        )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Monitor activo\nUsuarios vigilados: {len(watched_users)}"
    )


async def tiktoktest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        client = TikTokLiveClient(unique_id="tiktok")

        await update.message.reply_text(
            "TikTokLive funciona correctamente."
        )

    except Exception as e:
        await update.message.reply_text(
            f"Error: {e}"
        )


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Uso: /check usuario"
        )
        return

    username = context.args[0]

    try:
        client = TikTokLiveClient(unique_id=username)

        await update.message.reply_text(
            f"Usuario TikTok encontrado: {username}"
        )

    except Exception as e:
        await update.message.reply_text(
            f"Error comprobando {username}: {e}"
        )


async def monitor_loop():
    global monitor_running

    monitor_running = True

    while True:
        print("Revisando usuarios...")

        for user in watched_users:
            print(f"Usuario vigilado: {user}")

            try:
                client = TikTokLiveClient(unique_id=user)

                print(f"Cliente TikTok creado: {user}")
                print(f"Preparando comprobación: {user}")

            except Exception as e:
                print(f"Error TikTok {user}: {e}")

        await asyncio.sleep(60)


def main():
    if not TOKEN:
        raise Exception("BOT_TOKEN no fue encontrado en Railway")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("monitor", monitor))
    app.add_handler(CommandHandler("list", list_users))
    app.add_handler(CommandHandler("record", record))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("tiktoktest", tiktoktest))
    app.add_handler(CommandHandler("check", check))

    print("Bot iniciado...")

    app.job_queue.run_once(
        lambda context: asyncio.create_task(monitor_loop()),
        when=5
    )

    app.run_polling()


if __name__ == "__main__":
    main()
