from flask import Flask
import logging
import uuid
import json

app = Flask(__name__)

logging.basicConfig(
    filename="/logs/app.log",
    level=logging.INFO,
    format="%(message)s"
)

@app.route("/")
def home():

    log = {
        "service": "checkout",
        "user_id": str(uuid.uuid4()),
        "session_id": str(uuid.uuid4()),
        "order_id": str(uuid.uuid4()),
        "status": "success"
    }

    logging.info(json.dumps(log))

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)