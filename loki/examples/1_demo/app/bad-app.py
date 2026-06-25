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
    logger.info("customer visited home page")
    return "home"


@app.route("/payment")
def payment():
    amount = random.randint(100, 5000)
    logger.info(f"payment successful amount={amount}")
    return "payment done"


@app.route("/error")
def error():
    logger.error("payment gateway timeout")
    return "error", 500


@app.route("/badlog")
def badlog():

    print('{"timestamp": 12345, level: INFO, service: payment-service, message: broken json}')

    print("ERROR payment-service timeout user=123 action=pay")

    print('{"timestamp": 12345, "level": "INFO", "service": "payment-service", "message": "cut off log')

    print('{"timestamp": 12345, "level": "INFO", "service": "payment-service", message: missing quotes}')

    return "bad logs generated"


@app.route("/mix")
def mix():

    logger.info("valid structured log 1")

    print("BROKEN LOG: user login failed user=123 ip=10.0.0.1")

    logger.info(f"valid structured log 2 payment={random.randint(100,999)}")

    return "mixed logs generated"


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
