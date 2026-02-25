FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH=/app/src
ENV UV_SYSTEM_PYTHON=1

RUN pip install uv

COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --no-install-project

COPY alembic.ini ./
COPY alembic ./alembic
COPY src ./src
RUN uv sync --no-dev

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
