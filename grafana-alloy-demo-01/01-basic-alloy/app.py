from flask import Flask
import logging

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor


app = Flask(__name__)


trace.set_tracer_provider(
    TracerProvider()
)

tracer = trace.get_tracer(__name__)


exporter = OTLPSpanExporter(
    endpoint="http://alloy:4317",
    insecure=True
)


trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(exporter)
)


@app.route("/")
def home():

    with tracer.start_as_current_span(
        "homepage-request"
    ):

        logging.warning(
            "request received"
        )

        return {
            "message":
            "Hello Alloy"
        }


app.run(
    host="0.0.0.0",
    port=5000
)
