FROM python:3.12-alpine

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.1.3 \
    POETRY_HOME="/opt/poetry" \
    PATH="/opt/poetry/bin:$PATH"

RUN apk add --no-cache --virtual .build-deps curl git nmap build-base 

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi \
    && apk del .build-deps

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . .

CMD ["python", "bot/discbot.py"]

# Create a .env file with the following content:

# DISCORD_TOKEN=your-discord-token
# VT_API_KEY=your-virustotal-api-key

# Then start the container with the following flag: --env-file .env