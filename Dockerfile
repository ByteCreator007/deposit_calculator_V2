FROM python:3.10-slim

RUN apt-get update \
    && apt-get install -y build-essential libpq-dev \
    && apt-get clean

RUN pip install alembic

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev

COPY . /app

EXPOSE 8000

CMD ["bash", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"]

