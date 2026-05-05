# DLD Quiz Bot

![Python](https://img.shields.io/badge/Python-3B6D11?logo=python&logoColor=fff)
![Aiogram](https://img.shields.io/badge/Aiogram-1A7FA6?logo=telegram&logoColor=fff)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-5B3A8E?logo=postgresql&logoColor=fff)
![Docker](https://img.shields.io/badge/Docker-1D6A72?logo=docker&logoColor=fff)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2D6A2D?logo=github-actions&logoColor=fff)
![Uv](https://img.shields.io/badge/Uv-D85A30?logo=uv&logoColor=fff)
![Ruff](https://img.shields.io/badge/Ruff-A32D2D?logo=ruff&logoColor=fff)
![Mypy](https://img.shields.io/badge/Mypy-0C447C?logo=python&logoColor=fff)
![Pytest](https://img.shields.io/badge/Pytest-085041?logo=pytest&logoColor=fff)

> A Telegram quiz bot for preparing to the **Das Leben in Deutschland** citizenship test — practice all 310 questions and take full mock exams.

🤖 **[@dldquizbot](https://t.me/dldquizbot)** — available 24/7

## Features

- 🗺️ **Land selection** — questions tailored to your specific German federal state
- 📚 **Practice mode** — random questions one by one with instant feedback
- 📋 **Exam mode** — full 33-question mock test (23 general + 10 land-specific)
- 📊 **Statistics** — track your exam history and average score
- ⚙️ **Settings** — change your federal state at any time

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) and Docker Compose
- A Telegram bot token from [@BotFather](https://t.me/BotFather)

### Setup

```bash
git clone https://github.com/mykytakuzminov/dld-quiz-bot.git
cd dld-quiz-bot
```

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Fill in your values in `.env`, then run:

```bash
docker compose up --build -d
docker compose exec bot uv run alembic upgrade head
docker compose exec bot uv run python -m dld_quiz_bot.db.seed
```

## Commands

| Command | Description |
|---|---|
| `/start` | Start or restart the bot |
| `/learn` | Practice individual questions |
| `/exam` | Take a full mock test |
| `/stats` | View your test results |
| `/settings` | Change your federal state |
| `/stop` | Stop current session |
| `/info` | Show available commands |

## Development

```bash
uv sync
uv run tox
```
