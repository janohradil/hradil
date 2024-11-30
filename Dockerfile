FROM python:latest AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

RUN python -m venv .venv
COPY requirements.txt ./
RUN .venv/bin/pip install -r requirements.txt
FROM python:latest-slim
COPY --from=builder /.venv .venv/
COPY . .
# CMD [".venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
<<<<<<< HEAD
# ENTRYPOINT [".venv/bin/uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
ENTRYPOINT ["python", "app:app", "--host", "0.0.0.0", "--port", "8000"]
=======
<<<<<<< HEAD
# ENTRYPOINT [".venv/bin/uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
ENTRYPOINT ["python", "app:app", "--host", "0.0.0.0", "--port", "8000"]
=======
ENTRYPOINT [".venv/bin/uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
# ENTRYPOINT [".venv/bin/python", "main"]
>>>>>>> 95650fa034a1417f608f25afb38325ae5910a605
>>>>>>> 3a956162ba5ebd49169a193206c10759159d1105

