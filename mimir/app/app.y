from flask import Flask
from prometheus_client import Counter, Gauge, Histogram
from prometheus_client import generate_latest
from prometheus_client import CONTENT_TYPE_LATEST

import random
import time


app = Flask(__name__)


orders = Counter(
    "orders_total",
    "Total Orders",
    ["status","customer"]
)


cart = Gauge(
    "cart_items",
    "Items currently in cart"
)


checkout_latency = Histogram(
    "checkout_latency_seconds",
    "Checkout latency"
)



@app.route("/")
def home():

    status=random.choice(["success","failed"])

    customer=str(random.randint(1,10000))


    orders.labels(
        status=status,
        customer=customer
    ).inc()


    cart.set(
        random.randint(1,100)
    )


    checkout_latency.observe(
        random.random()
    )


    return "order generated"



@app.route("/metrics")
def metrics():

    return generate_latest(),200,{"Content-Type":CONTENT_TYPE_LATEST}



if __name__=="__main__":

    app.run(
        host="0.0.0.0",
        port=8000
    )
