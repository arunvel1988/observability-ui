from flask import Flask
from prometheus_client import Counter, generate_latest


app = Flask(__name__)


payments = Counter(
    "payments_done_total",
    "Number of payments"
)



@app.route("/pay")
def pay():

    payments.inc()

    return "Payment Done"



@app.route("/metrics")
def metrics():

    return generate_latest()



app.run(
    host="0.0.0.0",
    port=5000
)
