from flask import Flask
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# -------- SDK CONFIGURATION (startup code) --------
trace.set_tracer_provider(TracerProvider())

otlp_exporter = OTLPSpanExporter(
    endpoint="http://localhost:4318/v1/traces"
)

span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# -------- APPLICATION CODE (API) --------
app = Flask(__name__)
tracer = trace.get_tracer(__name__)

@app.route("/")
def home():
    with tracer.start_as_current_span("home-handler"):
        return "Hello from Flask with OpenTelemetry SDK"

if __name__ == "__main__":
    app.run(port=5000)
