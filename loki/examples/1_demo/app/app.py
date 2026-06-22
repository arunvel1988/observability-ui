from flask import Flask
import logging
import json
import random
import time


app = Flask(__name__)


class JSONFormatter(logging.Formatter):

    def format(self, record):

        data = {

            "timestamp": time.time(),

            "level": record.levelname,

            "service": "payment-service",

            "message": record.getMessage()

        }

        return json.dumps(data)



handler = logging.StreamHandler()

handler.setFormatter(JSONFormatter())


logger = logging.getLogger()

logger.setLevel(logging.INFO)

logger.addHandler(handler)



@app.route("/")

def home():

    logger.info(
        "customer visited home page"
    )

    return "home"



@app.route("/payment")

def payment():

    amount=random.randint(100,5000)

    logger.info(
        f"payment successful amount={amount}"
    )

    return "payment done"



@app.route("/error")

def error():


    logger.error(
        "payment gateway timeout"
    )

    return "error",500



app.run(
    host="0.0.0.0",
    port=5000
)