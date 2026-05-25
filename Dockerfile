FROM python:3.13-slim

WORKDIR /app

COPY novel_platform_backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY novel_platform_backend/ .

EXPOSE 8001

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8001", "--workers", "2", "--timeout", "120"]
