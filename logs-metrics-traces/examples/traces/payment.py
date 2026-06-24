
from flask import Flask
import time
import random

from opentelemetry.instrumentation.flask import FlaskInstrumentor


app=Flask(__name__)

FlaskInstrumentor().instrument_app(app)



@app.route("/payment")
def pay():

    if random.randint(1,5)==1:

        time.sleep(5)

    else:

        time.sleep(.2)


    return "payment done"



app.run(host="0.0.0.0",port=5003)
