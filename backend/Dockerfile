FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.in-project true

RUN apt-get update && apt-get install -y docker.io curl && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-dev --no-interaction --no-ansi

ENV PYTHONPATH=/app/app

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "python", "-m", "app.main"]
