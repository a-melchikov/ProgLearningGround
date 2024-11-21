FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry

RUN apt-get update && apt-get install -y docker.io && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-dev

ENV PYTHONPATH=/app/app

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app.main_app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
