FROM python:3.11

WORKDIR /app

RUN pip install flask \
    opentelemetry-api \
    opentelemetry-sdk \
    opentelemetry-exporter-otlp

COPY app.py .

CMD ["python", "app.py"]
