FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.in-project true

RUN apt-get update && apt-get install -y docker.io curl && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./

RUN poetry install --only=main --no-interaction --no-ansi --no-root

ENV PYTHONPATH=/app/app

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "python", "-m", "app.main"]
