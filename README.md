# Das Leben in Deutschland Quiz Bot

![Python](https://img.shields.io/badge/Python-24292e?logo=python&logoColor=fff)
![Aiogram](https://img.shields.io/badge/Aiogram-24292e?logo=telegram&logoColor=fff)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-24292e?logo=postgresql&logoColor=fff)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-24292e?logo=sqlalchemy&logoColor=fff)
![Alembic](https://img.shields.io/badge/Alembic-24292e?logo=sqlalchemy&logoColor=fff)
![Docker](https://img.shields.io/badge/Docker-24292e?logo=docker&logoColor=fff)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-24292e?logo=github-actions&logoColor=fff)

> An asynchronous Telegram bot designed to help users prepare for the official German integration exam *"Das Leben in Deutschland" (LiD)*. Features state-dependent quiz modes, region-specific questions, and user statistics tracking.
>
> 🚀 **Live Demo:** Try the bot directly on Telegram: [@dldquizbot](https://t.me/dldquizbot) (Running 24/7 on a VPS)

## 🗺️ Features

| Feature | Description |
|---|---|
| **Exam Simulation** | Simulates the real test environment with 33 randomized questions within the time limit. |
| **State-Specific Content** | Filters and includes specialized questions based on the selected German federal state (Bundesland). |
| **Progressive Learning** | Allows users to browse questions, choose answering options, and receive instant feedback. |
| **Statistics Tracking** | Persists user performance data to track passing rates and exam history. |
| **State Machine (FSM)** | Leverages strict finite state management to handle multi-step user interactions smoothly. |

## 🛠️ Tech Stack

- **[Python](https://www.python.org/)** — Core language utilizing async/await paradigms.
- **[Aiogram](https://docs.aiogram.dev/)** — Modern and fully asynchronous framework for Telegram Bots API.
- **[PostgreSQL](https://www.postgresql.org/)** — Relational database system for user states, progress, and historical stats.
- **[SQLAlchemy](https://www.sqlalchemy.org/)** — Async ORM layer for robust database communication via `asyncpg`.
- **[Alembic](https://alembic.sqlalchemy.org/)** — Database schema migration management.
- **[Docker](https://www.docker.com/)** — Containerized multi-service architecture (Bot application + PostgreSQL instance).
- **[GitHub Actions](https://github.com/features/actions)** — Automated CI/CD workflow running tests, style formatting, and type-checking on every push.

## 🏗️ Project Architecture & Design Patterns

The project follows a modular, scalable architecture specifically tailored for event-driven Telegram bot development. It decouples message handling from data persistence layers to maintain low coupling.

### 📁 Directory Structure
- `src/dld_quiz_bot/` — Root package of the application.
  - `db/` — Database architecture containing connection pooling (`database.py`), SQLAlchemy declarations (`models.py`), automated seeders for the question bank (`seed.py`), and data access objects (`repository.py`).
  - `handlers/` — Domain-specific message routing and interaction handlers divided by feature layers (`exam.py`, `learn.py`, `stats`, `settings.py`).
  - `data/` — Static assets including the parsed exam questions dataset (`questions.json`) and illustration vectors.
  - `main.py` — Bot initialization, polling manager orchestration, and middleware registration.

### 🧬 Architectural Highlights

1. **Repository Pattern (`repository.py`)** — Data transactions are completely isolated from the Telegram event loop. Handlers never write raw SQL or interact directly with database sessions, ensuring clean testing boundaries.
2. **Finite State Machine (FSM)** — User contexts (e.g., currently running an exam vs. changing settings) are explicitly locked inside states managed asynchronously, preventing collision in concurrent chats.
3. **Automated Seeding System** — On container initialization, the bot parses structured `questions.json` data and automatically synchronizes the PostgreSQL instance with complete multilingual content and question-to-image mappings.

## 🚀 Getting Started

### Prerequisites
- [Docker](https://www.docker.com/) and Docker Compose installed.
- A Telegram Bot Token obtained from [@BotFather](https://t.me/BotFather).

### Quick Start

1. Clone the repository and navigate into it:
```bash
git clone https://github.com/mykytakuzminov/dld-quiz-bot.git
cd dld-quiz-bot
```

2. Configure environment variables:
```bash
cp .env.example .env
```

(Open `.env` and fill in your `BOT_TOKEN` along with database credentials).

3. Run the ecosystem via Docker Compose:
```bash
docker compose up -d --build
```

4. Apply database schemas:
```bash
docker compose exec bot uv run alembic upgrade head
```

5. Run seed script to fill questions table
```bash
docker compose exec bot uv run python -m dld_quiz_bot.db.seed
```

## 🔧 Development & Code Quality

This project enforces strict code styling and testing principles via `Tox`.

### Local Installation

Sync dependencies using the ultra-fast `uv` toolchain
```bash
uv sync
```

### Running Automated Testing & Linting

You can invoke the entire validation suite locally just as it runs inside GitHub Actions:

* **Run Everything (Tox):** Enforces tests, linters, and checkers in isolated environments.
```bash
uv run tox
```

* **Unit & Integration Tests:** Driven by `pytest` with async database isolation.
```bash
uv run pytest
```

* **Linter & Code Formatting:** Managed by `ruff`.
```bash
uv run ruff check
```

* **Strict Type Auditing:** Evaluated via mypy.
```bash
uv run mypy src/
```

