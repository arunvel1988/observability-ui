from flask import Flask
from prometheus_client import Counter, generate_latest
import random


app = Flask(__name__)


orders = Counter(
    "orders_total",
    "Total orders",
    ["status"]
)


@app.route("/")
def order():

    status=random.choice(
        ["success","failed"]
    )

    orders.labels(
        status=status
    ).inc()

    return status


@app.route("/metrics")
def metrics():

    return generate_latest()



app.run(
    host="0.0.0.0",
    port=8000
)
