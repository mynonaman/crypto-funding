FROM python:3.11-slim
WORKDIR /app

# Install system deps for matplotlib if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libfreetype6-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Entrypoint: run the one-off job (cron or external scheduler should run this)
CMD ["python", "run_daily.py"]
