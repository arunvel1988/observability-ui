FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN opentelemetry-bootstrap -a install

COPY . .

ENV OTEL_SERVICE_NAME=ecommerce-service

ENV OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
ENV OTEL_EXPORTER_OTLP_PROTOCOL=grpc

ENV OTEL_TRACES_EXPORTER=otlp
ENV OTEL_METRICS_EXPORTER=otlp

ENV OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true

ENV OTEL_PYTHON_DISABLED_INSTRUMENTATIONS=""

ENV OTEL_METRIC_EXPORT_INTERVAL=5000


CMD ["opentelemetry-instrument", "python", "app.py"]
