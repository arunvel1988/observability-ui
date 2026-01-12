from flask import Flask
from opentelemetry import trace

app = Flask(__name__)

tracer = trace.get_tracer(__name__)

@app.route("/")
def home():
    with tracer.start_as_current_span("home-handler"):
        return "Hello from Flask with OpenTelemetry API"

if __name__ == "__main__":
    app.run(port=5000)
