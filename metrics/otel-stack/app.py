from flask import Flask

from opentelemetry import metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
    OTLPMetricExporter
)


app = Flask(__name__)


# OTEL -> Alloy
exporter = OTLPMetricExporter(
    endpoint="http://alloy:4317",
    insecure=True
)


reader = PeriodicExportingMetricReader(
    exporter,
    export_interval_millis=3000
)


provider = MeterProvider(
    resource=Resource.create({
        "service.name": "ecommerce-service"
    }),
    metric_readers=[reader]
)


metrics.set_meter_provider(provider)


meter = metrics.get_meter("ecommerce-meter")


cart_counter = meter.create_counter(
    "cart_count"
)


checkout_counter = meter.create_counter(
    "checkout_count"
)



@app.route("/")
def home():

    return "Flask OTEL Metrics"



@app.route("/cart")
def cart():

    cart_counter.add(
        1,
        {
            "endpoint":"cart"
        }
    )

    return "cart added"



@app.route("/checkout")
def checkout():

    checkout_counter.add(
        1,
        {
            "endpoint":"checkout"
        }
    )

    return "checkout completed"



app.run(
    host="0.0.0.0",
    port=5000
)
