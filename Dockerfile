FROM python:3.12-alpine

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.1.3 \
    POETRY_HOME="/opt/poetry" \
    PATH="/opt/poetry/bin:$PATH"

RUN apk add --no-cache --virtual .build-deps curl git build-base
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.create false

WORKDIR /app
COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-interaction --no-ansi --only main \
    && apk del .build-deps
RUN pip install wafw00f

COPY . .
CMD ["python", "bot/discbot.py"]

# Create a .env file with the following content:
# DISCORD_TOKEN=your-discord-token
# VT_API_KEY=your-virustotal-api-key
# Then start the container with the following flag: --env-file .env