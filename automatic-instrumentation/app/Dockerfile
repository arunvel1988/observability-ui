FROM python:3.12-slim


WORKDIR /app


COPY requirements.txt .


RUN pip install -r requirements.txt


RUN opentelemetry-bootstrap -a install


COPY . .


ENV OTEL_SERVICE_NAME=ecommerce-service

ENV OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317

ENV OTEL_EXPORTER_OTLP_PROTOCOL=grpc


CMD ["opentelemetry-instrument", "python", "app.py"]
