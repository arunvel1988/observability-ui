rom flask import Flask
import time
import random
import pyroscope

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor

pyroscope.configure(
    application_name="shop-backend-profile-demo",
    server_address="http://pyroscope:4040",
    tags={"env": "demo", "service": "shop-backend"}
)

provider = TracerProvider()
trace.set_tracer_provider(provider)

exporter = OTLPSpanExporter(
    endpoint="http://alloy:4317",
    insecure=True
)

provider.add_span_processor(BatchSpanProcessor(exporter))

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

tracer = trace.get_tracer(__name__)

def cpu_intensive_task():
    total = 0
    for i in range(20000000):
        total += (i % 10) * (i % 5)
    return total

def memory_intensive_task():
    big_list = []
    for i in range(200000):
        big_list.append({
            "id": i,
            "payload": "x" * 200,
            "meta": {"value": random.random()}
        })
    return len(big_list)

def fake_db_call():
    time.sleep(1.5)
    return {"rows": 1200, "status": "ok"}

@app.route("/fast")
def fast():
    return "FAST OK"

@app.route("/cpu-heavy")
def cpu_heavy():
    with tracer.start_as_current_span("cpu-heavy-span"):
        pyroscope.tag_wrapper({"endpoint": "/cpu-heavy"}, cpu_intensive_task)
    return "CPU DONE"

@app.route("/memory-heavy")
def memory_heavy():
    with tracer.start_as_current_span("memory-heavy-span"):
        pyroscope.tag_wrapper({"endpoint": "/memory-heavy"}, memory_intensive_task)
    return "MEMORY DONE"

@app.route("/mixed")
def mixed():
    with tracer.start_as_current_span("mixed-span"):
        cpu_intensive_task()
        memory_intensive_task()
        time.sleep(0.5)
    return "MIXED DONE"

@app.route("/db-sim")
def db_sim():
    with tracer.start_as_current_span("db-span"):
        fake_db_call()
    return "OK"

@app.route("/error")
def error():
    with tracer.start_as_current_span("error-span"):
        raise Exception("demo failure")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
