from flask import Flask
import random
import time

# OpenTelemetry Imports
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter

# Automatic Flask instrumentation
from opentelemetry.instrumentation.flask import FlaskInstrumentor

app = Flask(__name__)

# -----------------------------
# OTel Setup
# -----------------------------

resource = Resource.create({
    "service.name": "flask-otel-demo"
})

exporter = OTLPMetricExporter(
    endpoint="http://alloy:4318/v1/metrics"
)

reader = PeriodicExportingMetricReader(exporter)

provider = MeterProvider(
    resource=resource,
    metric_readers=[reader]
)

metrics.set_meter_provider(provider)

meter = metrics.get_meter("flask-demo")

# -----------------------------
# Custom Metrics
# -----------------------------

cart_counter = meter.create_counter(
    name="cart_count",
    description="Number of carts created"
)

checkout_counter = meter.create_counter(
    name="checkout_success",
    description="Successful checkouts"
)

# -----------------------------
# Automatic Metrics
# -----------------------------

FlaskInstrumentor().instrument_app(app)

# -----------------------------
# Routes
# -----------------------------

@app.route("/")
def home():
    return "Flask OTel Demo Running"

@app.route("/cart")
def cart():
    cart_counter.add(1)

    time.sleep(random.uniform(0.1, 0.5))

    return "Cart Added"

@app.route("/checkout")
def checkout():
    checkout_counter.add(1)

    time.sleep(random.uniform(0.2, 1.0))

    return "Checkout Success"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
