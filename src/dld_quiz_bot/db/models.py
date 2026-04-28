import json
from dataclasses import dataclass
from datetime import datetime

from asyncpg import Record

from dld_quiz_bot.enums import GermanLand, Topic


@dataclass
class Question:
    id: int
    text: str
    options: list[str]
    correct_answer: str
    topic: Topic
    land: GermanLand | None

    @classmethod
    def from_record(cls, record: Record) -> Question:
        return cls(
            id=record["id"],
            text=record["text"],
            options=json.loads(record["options"]),
            correct_answer=record["correct_answer"],
            topic=Topic(record["topic"]),
            land=GermanLand(record["land"]) if record["land"] is not None else None,
        )


@dataclass
class User:
    telegram_id: int
    username: str | None
    selected_land: GermanLand
    created_at: datetime

    @classmethod
    def from_record(cls, record: Record) -> User:
        return cls(
            telegram_id=record["telegram_id"],
            username=record["username"],
            selected_land=GermanLand(record["selected_land"]),
            created_at=record["created_at"],
        )


@dataclass
class ExamSession:
    id: int
    user_id: int
    total_questions: int = 33
    correct_answers: int = 0
    created_at: datetime | None = None
