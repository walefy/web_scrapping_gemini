FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .
COPY . .

RUN apk add --no-cache firefox

RUN addgroup -g 1000 appuser && \
  adduser -D -u 1000 -G appuser appuser && \
  chown -R appuser:appuser /app

USER appuser

ENV UV_LINK_MODE=copy
ENV UV_FROZEN=1
ENV PYTHONUNBUFFERED=1

RUN uv sync

CMD [ "uv", "run", "main.py" ]
