FROM python:latest AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

RUN python -m venv .venv
COPY requirements.txt ./
RUN .venv/bin/pip install -r requirements.txt
FROM python:latest
COPY --from=builder /.venv .venv/
COPY . .
ENTRYPOINT ["python", "app:app", "--host", "0.0.0.0", "--port", "8000"]
