from flask import Flask, jsonify, request, render_template_string
from flask import Flask, jsonify, request
from confluent_kafka import Consumer
from opentelemetry.proto.collector.logs.v1.logs_service_pb2 import (
    ExportLogsServiceRequest
)
import threading
from collections import defaultdict, deque
from datetime import datetime

app = Flask(__name__)

# =========================
# In-memory state
# =========================
LOG_BUFFER = deque(maxlen=300)

STATS = {
    "total_logs": 0,
    "error_logs": 0,
    "http_5xx": 0,
    "per_service_errors": defaultdict(int),
    "last_error_ts": None,
}

# =========================
# Helpers
# =========================
def ns_to_iso(ns):
    if not ns:
        return None
    return datetime.utcfromtimestamp(ns / 1_000_000_000).isoformat() + "Z"


def get_attr(log, key):
    for kv in log.attributes:
        if kv.key == key:
            return kv.value.string_value
    return None


# =========================
# Kafka Consumer Thread
# =========================
def consume_kafka():
    conf = {
        "bootstrap.servers": "arunvel1988-kafka-arunvel1988.e.aivencloud.com:14253",
        "security.protocol": "SSL",
        "ssl.ca.location": "ca.pem",
        "ssl.certificate.location": "service.cert",
        "ssl.key.location": "service.key",
        "group.id": "otel-observability",
        "auto.offset.reset": "latest",
    }

    consumer = Consumer(conf)
    consumer.subscribe(["otel-logs"])

    print("Kafka consumer started...")

    while True:
        msg = consumer.poll(1.0)
        if msg is None or msg.error():
            continue

        request_proto = ExportLogsServiceRequest()
        request_proto.ParseFromString(msg.value())

        for resource_log in request_proto.resource_logs:
            service = "unknown"
            for kv in resource_log.resource.attributes:
                if kv.key == "service.name":
                    service = kv.value.string_value

            for scope_log in resource_log.scope_logs:
                for log in scope_log.log_records:
                    STATS["total_logs"] += 1

                    severity = log.severity_text or "UNSPECIFIED"
                    body = log.body.string_value

                    http_status = get_attr(log, "http.status_code")
                    http_status = int(http_status) if http_status and http_status.isdigit() else None

                    is_error = severity == "ERROR" or (http_status and http_status >= 500)

                    record = {
                        "timestamp": ns_to_iso(log.time_unix_nano),
                        "service": service,
                        "severity": severity,
                        "body": body,
                        "http_status": http_status,
                        "is_error": is_error,
                    }

                    LOG_BUFFER.append(record)

                    if is_error:
                        STATS["error_logs"] += 1
                        STATS["per_service_errors"][service] += 1
                        STATS["last_error_ts"] = record["timestamp"]

                        if http_status and http_status >= 500:
                            STATS["http_5xx"] += 1


# =========================
# Flask Endpoints
# =========================
@app.route("/")
def index():
    template = """
    <html>
    <head>
        <title>OTEL Kafka Observability Demo</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; color: #333; padding: 30px; }
            h1 { color: #007BFF; }
            .container { background: #fff; padding: 20px 30px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
            .endpoint { margin: 10px 0; font-size: 18px; }
            a { color: #007BFF; text-decoration: none; font-weight: bold; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>OTEL  AIVEN Kafka Observability Demo OTEL</h1>
            <p>Welcome to the observability dashboard for your Aiven OTEL Kafka project.</p>
            <div class="endpoint"><a href="/logs">/logs</a> - View recent decoded logs</div>
            <div class="endpoint"><a href="/analytics">/analytics</a> - View log-derived analytics</div>
        </div>
    </body>
    </html>
    """
    return render_template_string(template)



@app.route("/logs")
def logs():
    severity = request.args.get("severity")
    service = request.args.get("service")

    logs = list(LOG_BUFFER)

    if severity:
        logs = [l for l in logs if l["severity"] == severity.upper()]

    if service:
        logs = [l for l in logs if l["service"] == service]

    return jsonify(logs)


@app.route("/analytics")
def analytics():
    total = STATS["total_logs"]
    error_rate = round((STATS["error_logs"] / total) * 100, 2) if total else 0

    recent_errors = [l for l in LOG_BUFFER if l["is_error"]][-5:]

    return jsonify({
        "total_logs": total,
        "error_logs": STATS["error_logs"],
        "http_5xx_errors": STATS["http_5xx"],
        "error_rate_percent": error_rate,
        "per_service_errors": dict(STATS["per_service_errors"]),
        "last_error_timestamp": STATS["last_error_ts"],
        "recent_error_samples": recent_errors,
    })


# =========================
# Main
# =========================
if __name__ == "__main__":
    t = threading.Thread(target=consume_kafka, daemon=True)
    t.start()

    app.run(host="0.0.0.0", port=5000)
