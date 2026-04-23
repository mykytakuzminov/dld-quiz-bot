from dataclasses import dataclass
from datetime import datetime


@dataclass
class Question:
    id: int
    text: str
    options: list[str]
    correct_answer: str
    category: bool
    land: str | None


@dataclass
class User:
    telegram_id: int
    username: str | None
    selected_land: str
    created_at: datetime


@dataclass
class ExamSession:
    id: int
    user_id: int
    total_questions: int
    correct_answers: int
    created_at: datetime
