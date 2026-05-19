FROM ghcr.io/astral-sh/uv:0.11.15-python3.11-trixie-slim

WORKDIR /app

# Install additional system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libavif-dev pkg-config \
    libjpeg-dev \
    gcc unzip zip \
    python3-dev \
    libxml2-dev \
    libxslt1-dev \
    libffi-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY src/requirements.txt .

RUN uv pip install -r requirements.txt --system

COPY src/ .

RUN mkdir -p  models/db_schemas/minirag

COPY docker/minirag/alembic.ini /app/models/db_schemas/minirag/alembic.ini

COPY docker/minirag/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" , "--workers", "4" ]
