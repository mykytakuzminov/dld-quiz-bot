from dataclasses import dataclass
from datetime import datetime

from dld_quiz_bot.enums import GermanLand, Topic


@dataclass
class Question:
    id: int
    text: str
    options: list[str]
    correct_answer: str
    topic: Topic
    land: GermanLand | None


@dataclass
class User:
    telegram_id: int
    username: str | None
    selected_land: GermanLand
    created_at: datetime


@dataclass
class ExamSession:
    id: int
    user_id: int
    total_questions: int = 33
    correct_answers: int = 0
    created_at: datetime | None = None
