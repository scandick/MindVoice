import os
from datetime import datetime
from pathlib import Path

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Получаем токен бота из переменной окружения
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Папка для сохранения записей
RECORDINGS_DIR = Path("recordings")
RECORDINGS_DIR.mkdir(exist_ok=True)

SUPPORTIVE_MESSAGE = (
    "Вы молодец, что делитесь своими чувствами. "
    "Проговаривание помогает облегчить мысли."
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Ответ на команду /start."""
    await update.message.reply_text(
        "Привет! Этот бот поможет вам проговаривать эмоции. "
        "Просто отправьте голосовое сообщение в любой момент."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Ответ на команду /help."""
    await update.message.reply_text(
        "Отправьте голосовое сообщение, чтобы сохранить его. "
        "Команда /myrecordings покажет список ваших записей."
    )

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Сохраняем голосовое сообщение и отправляем поддерживающий ответ."""
    user_id = update.effective_user.id
    voice = update.message.voice
    if not voice:
        return

    file = await context.bot.get_file(voice.file_id)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    user_dir = RECORDINGS_DIR / str(user_id)
    user_dir.mkdir(exist_ok=True)
    file_path = user_dir / f"{timestamp}.ogg"
    await file.download_to_drive(str(file_path))

    await update.message.reply_text(SUPPORTIVE_MESSAGE)

async def list_recordings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показываем список сохранённых записей пользователя."""
    user_id = update.effective_user.id
    user_dir = RECORDINGS_DIR / str(user_id)
    if not user_dir.exists():
        await update.message.reply_text("У вас пока нет записей.")
        return

    files = sorted(user_dir.iterdir())
    if not files:
        await update.message.reply_text("У вас пока нет записей.")
        return

    lines = [f.name for f in files]
    message = "Ваши записи:\n" + "\n".join(lines)
    await update.message.reply_text(message)

async def main() -> None:
    """Запуск бота."""
    if not TOKEN:
        print("Необходимо указать токен бота в переменной TELEGRAM_BOT_TOKEN")
        return

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("myrecordings", list_recordings))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))

    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
