<div align="center">

# 🚀 DLD Quiz Bot

Telegram preparation bot to "Das Leben in Deutschland" test

[![CI](https://github.com/mykytakuzminov/dld-quiz-bot/actions/workflows/ci.yml/badge.svg)](https://github.com/mykytakuzminov/dld-quiz-bot/actions/workflows/ci.yml)
[![CD](https://github.com/mykytakuzminov/dld-quiz-bot/actions/workflows/cd.yml/badge.svg)](https://github.com/mykytakuzminov/dld-quiz-bot/actions/workflows/cd.yml)
[![Python Version](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=fff)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

[Try the bot](https://t.me/dldquizbot)

</div>

---

## Features

- **Start** - start the bot
- **Learn** - learn by randomly chosen questions until have enough
- **Exam** - practice questions like on test
- **Stats** - check your attempts and results
- **Settings** - change your land to have particular questions
- **Stop** - stop learn or exam modes
- **Info** - get commands for bot usage

## Tech Highlights

- **Layered Architecture** - handlers and repository layers
- **Migrations** - implemented via alembic
- **CI/CD** - automated linting, testing and deploy

## Getting Started

### Prerequisites

- `uv`, `docker` and `docker compose`

### Installation

Add `BOT_TOKEN` given by BotFather, run migrations and seed questions
```bash
git clone https://github.com/mykytakuzminov/dld-quiz-bot.git
cd dld-quiz-bot
cp .env.example .env
docker compose up -d
docker compose exec dld-quiz-bot-app /app/.venv/bin/alembic upgrade head
docker compose exec dld-quiz-bot-app /app/.venv/bin/python -m dld_quiz_bot.db.seed
```

### Development

```bash
uv run tox # run linter, tests
```

## Tech Stack

### Core

- `Python`, `PostgreSQL`, `Docker`, `Docker Compose`, `GitHub Actions`

### Libraries

- `aiogram`, `alembic`, `asyncpg`, `psycopg2-binary`, `python-dotenv`

### Dev Tools
- `pytest`, `ruff`, `mypy`, `tox`
