
from flask import Flask
import requests
import random
import time

from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor


app=Flask(__name__)

FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()


@app.route("/checkout")
def checkout():

    requests.get("http://cart:5001/cart")

    requests.get("http://inventory:5002/inventory")

    requests.get("http://payment:5003/payment")

    return "ORDER COMPLETED"


@app.route("/")
def home():
    return "frontend"


app.run(host="0.0.0.0",port=5000)

