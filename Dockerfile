FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .
COPY . .

RUN apk add --no-cache firefox

ENV UV_LINK_MODE=copy
ENV UV_FROZEN=1
RUN uv sync

ENV PYTHONUNBUFFERED=1

CMD [ "uv", "run", "main.py" ]