
from flask import Flask
import time
import random

from opentelemetry.instrumentation.flask import FlaskInstrumentor


app=Flask(__name__)

FlaskInstrumentor().instrument_app(app)


@app.route("/cart")
def cart():

    time.sleep(random.random())

    return "cart ok"


app.run(host="0.0.0.0",port=5001)

EOF
