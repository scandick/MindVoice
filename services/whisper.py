"""Service to handle audio transcription using OpenAI Whisper API."""
import openai
from aiogram import Bot
from aiohttp import ClientSession

from config import settings

# TODO: Insert your OpenAI API key in .env
openai.api_key = settings.OPENAI_API_KEY


async def transcribe_voice(bot: Bot, file_id: str) -> str:
    """Download the voice file from Telegram and transcribe it."""
    file = await bot.get_file(file_id)
    file_path = file.file_path

    async with ClientSession() as session:
        voice_data = await bot.download_file(file_path)

    # Save to temp file
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".ogg") as temp_file:
        temp_file.write(voice_data.getvalue())
        temp_file.flush()
        with open(temp_file.name, "rb") as f:
            transcript = openai.Audio.transcribe("whisper-1", f, language="ru")

    return transcript["text"]
