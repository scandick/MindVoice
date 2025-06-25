"""Database models."""
from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, Float, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    """User model storing subscription info."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    is_premium = Column(Boolean, default=False)
    trial_start = Column(DateTime, default=datetime.utcnow)
    subscription_expiry = Column(DateTime, nullable=True)

    transcripts = relationship("Transcript", back_populates="user")


class Transcript(Base):
    """Transcribed voice messages with mood score."""

    __tablename__ = "transcripts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    text = Column(String, nullable=False)
    mood_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="transcripts")
