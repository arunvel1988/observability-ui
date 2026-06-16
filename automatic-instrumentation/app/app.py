from flask import Flask, jsonify
import random
import time

app = Flask(__name__)


@app.route("/")
def home():
    return {
        "service": "ecommerce",
        "status": "running"
    }


@app.route("/products")
def products():

    time.sleep(random.uniform(0.1,0.5))

    return jsonify([
        {
            "id":1,
            "name":"Laptop",
            "price":1200
        },
        {
            "id":2,
            "name":"Phone",
            "price":800
        }
    ])


@app.route("/checkout")
def checkout():

    time.sleep(random.uniform(0.2,1))

    if random.randint(1,5)==1:
        raise Exception("Payment failed")

    return {
        "status":"order completed"
    }


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
