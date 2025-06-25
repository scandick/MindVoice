"""Main entry point for Emotional Voice Diary bot."""
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from config import settings
from db.database import Base, engine
from handlers import start, voice, payments
from jobs.weekly_report import send_weekly_reports

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def on_startup(bot: Bot) -> None:
    """Create database tables on startup."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Bot started")


async def main() -> None:
    """Initialize bot, dispatcher and scheduler."""
    bot = Bot(token=settings.TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(start.router, voice.router, payments.router)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_weekly_reports, CronTrigger(day_of_week="mon", hour=9), args=[bot])
    scheduler.start()

    await on_startup(bot)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
