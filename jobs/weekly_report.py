"""Weekly mood report job."""
import logging
from datetime import datetime, timedelta

from aiogram import Bot
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import AsyncSessionLocal
from db.models import Transcript, User

logger = logging.getLogger(__name__)


async def send_weekly_reports(bot: Bot) -> None:
    """Send weekly mood summary to all premium users."""
    async with AsyncSessionLocal() as session:
        week_ago = datetime.utcnow() - timedelta(days=7)
        users = await session.scalars(select(User).where(User.is_premium == True))
        for user in users:
            transcripts = await session.scalars(
                select(Transcript)
                .where(Transcript.user_id == user.id, Transcript.created_at >= week_ago)
            )
            texts = [t.text for t in transcripts]
            if not texts:
                continue
            average_mood = await session.scalar(
                select(func.avg(Transcript.mood_score)).where(
                    Transcript.user_id == user.id, Transcript.created_at >= week_ago
                )
            )
            report = (
                "Ваш недельный отчёт. Среднее настроение: {0:.2f}. Сообщений: {1}".format(
                    average_mood or 0.0, len(texts)
                )
            )
            await bot.send_message(user.telegram_id, report)
