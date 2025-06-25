"""Start and help commands."""
from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from db.database import get_session

router = Router()


@router.message(Command("start"))
async def start(message: types.Message, session: AsyncSession = None) -> None:
    """Handle /start command."""
    if session is None:
        async for session in get_session():
            await _start(message, session)
    else:
        await _start(message, session)


async def _start(message: types.Message, session: AsyncSession) -> None:
    user = await session.execute(
        User.__table__.select().where(User.telegram_id == message.from_user.id)
    )
    result = user.fetchone()
    if not result:
        user_obj = User(telegram_id=message.from_user.id)
        session.add(user_obj)
        await session.commit()
    text = (
        "Добро пожаловать в ваш эмоциональный дневник! "
        "Отправьте голосовое сообщение, чтобы начать."
    )
    await message.answer(text)


@router.message(Command("help"))
async def help_handler(message: types.Message) -> None:
    """Handle /help command."""
    await message.answer(
        "Просто отправьте голосовое сообщение. "
        "Бот распознает текст, определит настроение и ответит."
    )


@router.message(Command("privacy"))
async def privacy_handler(message: types.Message) -> None:
    """Handle /privacy command."""
    await message.answer(
        "Ваши данные хранятся конфиденциально и не передаются третьим лицам."
    )
