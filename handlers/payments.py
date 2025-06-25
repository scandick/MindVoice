"""Payment handlers for subscription."""
from datetime import datetime, timedelta

from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_session
from db.models import User
from services.payments import PRICE

router = Router()


@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    """Answer pre-checkout query."""
    await pre_checkout_q.answer(ok=True)


@router.message(types.ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message, session: AsyncSession = None) -> None:
    """Handle successful payment."""
    if session is None:
        async for session in get_session():
            await _success(message, session)
    else:
        await _success(message, session)


async def _success(message: types.Message, session: AsyncSession) -> None:
    user = await session.scalar(
        User.__table__.select().where(User.telegram_id == message.from_user.id)
    )
    if not user:
        user = User(telegram_id=message.from_user.id)
        session.add(user)
        await session.commit()

    user.is_premium = True
    user.subscription_expiry = datetime.utcnow() + timedelta(days=30)
    await session.commit()
    await message.answer("Спасибо за оплату! Подписка активирована на месяц.")
