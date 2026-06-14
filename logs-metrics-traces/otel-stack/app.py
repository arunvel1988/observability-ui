from flask import Flask
import logging
import random
import time


# =====================
# OTEL COMMON
# =====================

from opentelemetry.sdk.resources import Resource


resource = Resource.create(
{
"service.name":"ecommerce-app",
"environment":"dev"
}
)



# =====================
# METRICS
# =====================

from opentelemetry import metrics

from opentelemetry.sdk.metrics import MeterProvider

from opentelemetry.sdk.metrics.export import (
PeriodicExportingMetricReader
)

from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
OTLPMetricExporter
)


metric_exporter=OTLPMetricExporter(
endpoint="http://alloy:4317",
insecure=True
)


metrics.set_meter_provider(

MeterProvider(

resource=resource,

metric_readers=[

PeriodicExportingMetricReader(
metric_exporter,
export_interval_millis=5000
)

]

)

)


meter=metrics.get_meter("shop")


cart_counter=meter.create_counter(
"cart_count"
)


checkout_counter=meter.create_counter(
"checkout_count"
)



# =====================
# TRACES
# =====================


from opentelemetry import trace

from opentelemetry.sdk.trace import TracerProvider

from opentelemetry.sdk.trace.export import (
BatchSpanProcessor
)

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
OTLPSpanExporter
)


trace_provider=TracerProvider(
resource=resource
)


trace_provider.add_span_processor(

BatchSpanProcessor(

OTLPSpanExporter(

endpoint="http://alloy:4317",

insecure=True

)

)

)


trace.set_tracer_provider(trace_provider)


tracer=trace.get_tracer("shop-tracer")



# =====================
# LOGS
# =====================


from opentelemetry.sdk._logs import (
LoggerProvider,
LoggingHandler
)


from opentelemetry.sdk._logs.export import (
BatchLogRecordProcessor
)


from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
OTLPLogExporter
)



logger_provider=LoggerProvider(
resource=resource
)


logger_provider.add_log_record_processor(

BatchLogRecordProcessor(

OTLPLogExporter(

endpoint="http://alloy:4317",

insecure=True

)

)

)


handler=LoggingHandler(
logger_provider=logger_provider
)


logging.basicConfig(
level=logging.INFO,
handlers=[handler]
)


logger=logging.getLogger("shop")



app=Flask(__name__)



@app.route("/")
def home():

 return """

 <h1>OpenTelemetry Ecommerce Demo</h1>

 <h3>Generate Traffic</h3>

 <a href="/cart">Add Cart</a><br><br>

 <a href="/checkout">Checkout</a><br><br>

 <a href="/payment">Payment</a><br><br>

 <a href="/error">Generate Error</a>


 <hr>

 <h3>Curl Traffic</h3>

 <pre>

for i in {1..20}; do

 curl localhost:5000/cart

 curl localhost:5000/checkout

 curl localhost:5000/payment

done

 </pre>


 """




@app.route("/cart")
def cart():

 with tracer.start_as_current_span("cart-operation"):


  cart_counter.add(1)


  logger.info("Product added to cart")


  time.sleep(
  random.random()
  )


  return "cart added"





@app.route("/checkout")
def checkout():


 with tracer.start_as_current_span("checkout-operation"):


  checkout_counter.add(1)


  logger.info("Checkout completed")


  return "checkout"





@app.route("/payment")
def payment():


 with tracer.start_as_current_span("payment-operation"):


  logger.info("Payment successful")


  return "payment done"





@app.route("/error")
def error():


 with tracer.start_as_current_span("error-operation"):


  logger.error("payment failed")


  return "error generated"




app.run(
host="0.0.0.0",
port=5000
)
