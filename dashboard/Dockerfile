FROM python:3.11-slim

WORKDIR /app

COPY dashboard/requirements.txt /app/dashboard/requirements.txt
RUN pip install --no-cache-dir -r /app/dashboard/requirements.txt

COPY dashboard /app/dashboard
COPY models /app/models
COPY outputs /app/outputs

ENV PYTHONIOENCODING=utf-8
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

WORKDIR /app/dashboard
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
