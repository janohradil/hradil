FROM python:3.12.7 AS builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# Create and use virtual environment
RUN python -m venv .venv

# Copy dependencies file and install
COPY requirements.txt .
RUN .venv/bin/pip install --no-cache-dir -r requirements.txt

# Final image
FROM python:3.12.7-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# Copy virtual environment from the builder stage
COPY --from=builder /app/.venv .venv/

# Copy application code
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Run the application
ENTRYPOINT [".venv/bin/uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
