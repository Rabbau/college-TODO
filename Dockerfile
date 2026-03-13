FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY pyproject.toml poetry.lock requirements.txt /app/

RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends libpq-dev build-essential ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN update-ca-certificates

RUN pip install --no-cache-dir -r requirements.txt
    
COPY . /app

RUN mkdir -p /app/notes

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"]
