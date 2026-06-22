from flask import Flask
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


@app.route("/")
def home():

    logging.info("home page called")

    return "hello loki"


@app.route("/error")
def error():

    logging.error("payment failed")

    return "error created"


app.run(
 host="0.0.0.0",
 port=5000
)