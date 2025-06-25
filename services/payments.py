"""Telegram Payments integration helpers."""
from datetime import datetime, timedelta

from aiogram import types

from config import settings

PRICE = types.LabeledPrice(label="Подписка на месяц", amount=50000)  # 500 RUB


async def create_invoice(user_id: int) -> types.Invoice:
    """Create invoice for subscription payment."""
    return types.Invoice(
        title="Подписка",
        description="Доступ к эмоциональному дневнику на месяц",
        payload="subscription",
        provider_token=settings.PAYMENT_PROVIDER_TOKEN,
        currency="RUB",
        prices=[PRICE],
        start_parameter="subscribe",
    )


def is_trial_active(trial_start: datetime) -> bool:
    """Check if free trial is still active."""
    return datetime.utcnow() - trial_start < timedelta(days=settings.FREE_TRIAL_DAYS)
