from flask import Flask
import logging
import random
import time

from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

app = Flask(__name__)

# ---------------- METRICS ----------------
exporter = OTLPMetricExporter(
    endpoint="http://alloy:4317",
    insecure=True
)

reader = PeriodicExportingMetricReader(exporter)
provider = MeterProvider(metric_readers=[reader])
metrics.set_meter_provider(provider)

meter = metrics.get_meter("shop")
counter = meter.create_counter("requests_total")

# ---------------- LOGGING ----------------
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("shop")

@app.route("/")
def home():
    counter.add(1)
    log.info("home hit")
    return "home"

@app.route("/buy")
def buy():
    counter.add(5)
    log.debug("debug payment step")  # will be dropped
    log.info("buy success")
    time.sleep(random.random())
    return "buy"

@app.route("/error")
def error():
    log.error("payment failed")
    return "error"

app.run(host="0.0.0.0", port=5000)
