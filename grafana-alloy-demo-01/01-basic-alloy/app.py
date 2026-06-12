from flask import Flask

from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.metrics import set_meter_provider

from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

from opentelemetry.sdk.metrics.export import (
    PeriodicExportingMetricReader
)


app = Flask(__name__)


exporter = OTLPMetricExporter(
    endpoint="http://alloy:4317",
    insecure=True
)


reader = PeriodicExportingMetricReader(
    exporter,
    export_interval_millis=5000
)


provider = MeterProvider(
    metric_readers=[reader]
)


set_meter_provider(provider)


meter = provider.get_meter(
    "flask-service"
)


counter = meter.create_counter(
    "http_requests_total"
)



@app.route("/")
def hello():


    counter.add(
        1,
        {
        "endpoint":"/"
        }
    )


    return "metrics sent to alloy"



app.run(
    host="0.0.0.0",
    port=5000
)
