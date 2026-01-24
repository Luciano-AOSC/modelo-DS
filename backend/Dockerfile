FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

COPY backend /app/backend
COPY src /app/src
COPY models /app/models
COPY outputs /app/outputs

ENV PYTHONIOENCODING=utf-8

WORKDIR /app/backend
EXPOSE 8000

CMD ["python", "main.py"]
