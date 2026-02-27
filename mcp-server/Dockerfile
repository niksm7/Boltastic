# Use official Python image
FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install project
COPY . /app
WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN uv sync
RUN uv run playwright install chromium
RUN uv run playwright install-deps || true

EXPOSE 8080

ENV PORT=8080
CMD ["uv", "run", "mcp_server.py"]
