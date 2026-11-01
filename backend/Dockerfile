# Development image for the FastAPI backend (production image comes in Phase 7).
FROM python:3.12-slim

# Install uv from PyPI. Long timeout + retries help on slow/unstable networks.
RUN pip install --no-cache-dir --default-timeout=120 --retries 10 uv

WORKDIR /app

# Put the virtualenv outside /app so the source bind-mount doesn't hide it.
ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    UV_HTTP_TIMEOUT=120 \
    PYTHONPATH=/app

# Install dependencies first (cached layer: only re-runs when deps change).
COPY pyproject.toml uv.lock* ./
RUN uv sync --no-install-project

# Copy the source (in dev it is overridden by the volume mount).
COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

