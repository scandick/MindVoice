"""Service to analyze emotion and generate empathetic reply via GPT-4."""
import openai

from config import settings

# TODO: Insert your OpenAI API key in .env
openai.api_key = settings.OPENAI_API_KEY

SYSTEM_PROMPT = (
    "Ты — заботливый собеседник. Определи эмоциональный тон сообщения на шкале от -1 до 1 "
    "(где -1 — очень негативно, 1 — очень позитивно) и кратко поддержи пользователя."
)


async def analyze_text(text: str) -> tuple[str, float]:
    """Analyze emotion in text and return reply with mood score."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": text},
    ]
    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
    )
    content = response.choices[0].message.content
    # Simple extraction of mood score and reply
    # Expected format: "<score>; <reply>"
    try:
        score_str, reply = content.split(";", 1)
        mood_score = float(score_str.strip())
    except Exception:
        mood_score = 0.0
        reply = content

    return reply.strip(), mood_score
