FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create a user for running tests (helps with permissions)
RUN useradd -m -u 1000 testuser && chown -R testuser:testuser /app
USER testuser

COPY ./server/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./server .

# Create directories with proper permissions
RUN mkdir -p /tmp/coverage /tmp/pytest_cache && \
    chmod 777 /tmp/coverage /tmp/pytest_cache

EXPOSE 5000

CMD ["python", "main.py"]