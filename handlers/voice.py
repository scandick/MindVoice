"""Voice message handler."""
import logging
from datetime import datetime

from aiogram import Router, types
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_session
from db.models import Transcript, User
from services.whisper import transcribe_voice
from services.gpt import analyze_text
from services.payments import create_invoice, is_trial_active

router = Router()
logger = logging.getLogger(__name__)


@router.message(lambda m: m.voice)
async def voice_handler(message: types.Message, bot, session: AsyncSession = None) -> None:
    """Handle incoming voice messages."""
    if session is None:
        async for session in get_session():
            await _process(message, bot, session)
    else:
        await _process(message, bot, session)


async def _process(message: types.Message, bot, session: AsyncSession) -> None:
    user = await session.scalar(
        User.__table__.select().where(User.telegram_id == message.from_user.id)
    )
    if not user:
        user = User(telegram_id=message.from_user.id)
        session.add(user)
        await session.commit()

    if not user.is_premium and not is_trial_active(user.trial_start):
        invoice = await create_invoice(message.from_user.id)
        await message.answer("Ваш пробный период истёк. Пожалуйста, оформите подписку.")
        await bot.send_invoice(message.chat.id, **invoice.model_dump())
        return

    try:
        text = await transcribe_voice(bot, message.voice.file_id)
    except Exception as e:
        logger.exception("Whisper failed")
        await message.answer("Не удалось распознать голосовое сообщение.")
        return

    try:
        reply, mood_score = await analyze_text(text)
    except Exception as e:
        logger.exception("GPT failed")
        reply = "Извините, произошла ошибка при анализе."
        mood_score = 0.0

    transcript = Transcript(user_id=user.id, text=text, mood_score=mood_score)
    session.add(transcript)
    await session.commit()

    await message.answer(reply)
