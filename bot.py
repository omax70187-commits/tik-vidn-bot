import os
import asyncio

from TikTokLive import TikTokLiveClient

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

print("=== INICIO ===")
print("BOT_TOKEN cargado correctamente")

watched_users = []
monitor_running = False
recording_users = set()

TOKEN = os.getenv("BOT_TOKEN")

async def start_recording(username):
    if username in recording_users:
        return

    recording_users.add(username)

    print(f"INICIANDO GRABACION: {username}")

    try:
        import subprocess
        
        video_file = f"videos/{username}.mp4"
        
        print(f"Archivo destino: {video_file}")
        
        live_url = f"https://www.tiktok.com/@{username}/live"
        
        subprocess.Popen(
            [
                "yt-dlp",
                "-o",
                video_file,
                live_url
            ]
        )
        
        print(f"Grabacion lanzada para: {username}")

    except Exception as e:
        print(f"Error grabando {username}: {e}")

    finally:
        recording_users.discard(username)

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

async def tiktokinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        client = TikTokLiveClient(unique_id="tiktok")

        text = ""

        text += f"room_info: {client.room_info}\n\n"
        text += f"is_live: {client.is_live}\n\n"
        text += f"room_id: {client.room_id}\n\n"

        await update.message.reply_text(text[:4000])

    except Exception as e:
        await update.message.reply_text(
            f"Error: {e}"
        )

async def ytdltest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import subprocess

    try:
        result = subprocess.run(
            ["yt-dlp", "--version"],
            capture_output=True,
            text=True
        )

        await update.message.reply_text(
            f"yt-dlp OK\n{result.stdout}"
        )

    except Exception as e:
        await update.message.reply_text(
            f"Error yt-dlp: {e}"
        )

async def versiontest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import subprocess

    try:
        result = subprocess.run(
            ["pip", "show", "TikTokLive"],
            capture_output=True,
            text=True
        )

        await update.message.reply_text(result.stdout[:4000])

    except Exception as e:
        await update.message.reply_text(
            f"Error: {e}"
        )

async def grabtest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import subprocess

    try:
        result = subprocess.run(
            [
                "yt-dlp",
                "-F",
                "https://www.tiktok.com/@chimbotebaltayespinar5/live"
            ],
            capture_output=True,
            text=True
        )

        output = result.stdout + "\n" + result.stderr

        await update.message.reply_text(output[:4000])

    except Exception as e:
        await update.message.reply_text(
            f"Error: {e}"
        )

async def monitor_loop():
    global monitor_running

    monitor_running = True

    if not os.path.exists("videos"):
        os.makedirs("videos")
        print("Carpeta videos creada")

    while True:
        print("Revisando usuarios...")

        for user in watched_users:
            print(f"Usuario vigilado: {user}")

            try:
                client = TikTokLiveClient(unique_id=user)

                print(f"Cliente TikTok creado: {user}")

                if client.is_live:

                    print(f"LIVE DETECTADO: {user}")

                    if user not in recording_users:
                        await start_recording(user)

                else:
                    print(f"Offline: {user}")

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
    app.add_handler(CommandHandler("tiktokinfo", tiktokinfo))
    app.add_handler(CommandHandler("ytdltest", ytdltest))
    app.add_handler(CommandHandler("versiontest", versiontest))
    app.add_handler(CommandHandler("grabtest", grabtest))

    print("Bot iniciado...")

    app.job_queue.run_once(
        lambda context: asyncio.create_task(monitor_loop()),
        when=5
    )

    app.run_polling()


if __name__ == "__main__":
    main()
