FROM python:3.14-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project --no-python-downloads
COPY src/ ./src/
RUN uv sync --locked

FROM python:3.14-slim
WORKDIR /app
COPY --from=builder /app/.venv/ /app/.venv/
COPY --from=builder /app/src/ /app/src/
COPY pyproject.toml ./
COPY alembic/ ./alembic/
COPY alembic.ini ./
CMD ["/app/.venv/bin/python", "-m", "dld_quiz_bot.main"]
