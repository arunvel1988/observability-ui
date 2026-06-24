from flask import Flask
import random,time

from opentelemetry.instrumentation.flask import FlaskInstrumentor


app=Flask(__name__)

FlaskInstrumentor().instrument_app(app)


@app.route("/inventory")
def inventory():

    time.sleep(random.random())

    return "inventory ok"


app.run(host="0.0.0.0",port=5002)

