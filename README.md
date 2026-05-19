# DLD Quiz Bot

![Python](https://img.shields.io/badge/Python-376996?logo=python&logoColor=fff)
![Aiogram](https://img.shields.io/badge/Aiogram-376996?logo=telegram&logoColor=fff)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-376996?logo=postgresql&logoColor=fff)
![Alembic](https://img.shields.io/badge/Alembic-376996?logo=postgresql&logoColor=fff)
![Docker](https://img.shields.io/badge/Docker-376996?logo=docker&logoColor=fff)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-376996?logo=github-actions&logoColor=fff)
![Uv](https://img.shields.io/badge/Uv-376996?logo=uv&logoColor=fff)
![Ruff](https://img.shields.io/badge/Ruff-376996?logo=ruff&logoColor=fff)
![Mypy](https://img.shields.io/badge/Mypy-376996?logo=python&logoColor=fff)
![Pytest](https://img.shields.io/badge/Pytest-376996?logo=pytest&logoColor=fff)

> A Telegram quiz bot for preparing to the **Das Leben in Deutschland** citizenship test — practice all 460 questions and take full mock exams.

🤖 **[@dldquizbot](https://t.me/dldquizbot)** — available 24/7

## 🗺️ Features

| Feature | Description |
|---|---|
| Land selection | Questions tailored to your specific German federal state |
| Practice mode | Random questions one by one with instant feedback |
| Exam mode | Full 33-question mock test (30 general + 3 land-specific) |
| Statistics | Track your exam history and average score |
| Settings | Change your federal state at any time |

## ⚙️ Commands

| Command | Description |
|---|---|
| `/start` | Start or restart the bot |
| `/learn` | Practice individual questions |
| `/exam` | Take a full mock test |
| `/stats` | View your test results |
| `/settings` | Change your federal state |
| `/stop` | Stop current session |
| `/info` | Show available commands |

## 🛠️ Tech Stack

- **[python](https://www.python.org/)** — core language, 3.14
- **[aiogram](https://aiogram.dev/)** — async Telegram bot framework
- **[postgresql](https://www.postgresql.org/)** — relational database
- **[alembic](https://alembic.sqlalchemy.org/)** — database schema migrations
- **[docker](https://www.docker.com/)** — containerized deployment
- **[github actions](https://github.com/features/actions)** — CI + CD on every push
- **[uv](https://github.com/astral-sh/uv)** — fast package and environment management
- **[mypy](http://mypy-lang.org/)** — strict static type checking
- **[ruff](https://github.com/astral-sh/ruff)** — linting and formatting
- **[pytest](https://docs.pytest.org/)** — async tests with real PostgreSQL

## 🚀 Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) and Docker Compose
- A Telegram bot token from [@BotFather](https://t.me/BotFather)

### Setup

```bash
git clone https://github.com/mykytakuzminov/dld-quiz-bot.git
cd dld-quiz-bot
cp .env.example .env
```

Fill in your values in `.env`, then run:

```bash
docker compose up --build -d
docker compose exec bot uv run alembic upgrade head
docker compose exec bot uv run python -m dld_quiz_bot.db.seed
```

## 🔧 Development

```bash
uv sync
uv run tox
```
