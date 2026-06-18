from flask import Flask
from prometheus_client import Counter, generate_latest

app = Flask(__name__)


orders = Counter(
    "orders_created_total",
    "Number of orders created"
)


@app.route("/order")
def create_order():

    orders.inc()

    return "Order Created"



@app.route("/metrics")
def metrics():

    return generate_latest()



app.run(
    host="0.0.0.0",
    port=5000
)
