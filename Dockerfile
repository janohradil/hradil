FROM python:3.12.7 AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /
RUN ls -lh

RUN python -m venv .venv
COPY requirements.txt ./
RUN ls -lh
RUN .venv/bin/pip install -r requirements.txt
FROM python:3.12.7-slim
WORKDIR /
COPY --from=builder /.venv .venv/
RUN ls .venv
COPY . .
RUN ls
# CMD [".venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
ENTRYPOINT [".venv/bin/uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

