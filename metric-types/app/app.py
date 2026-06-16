from flask import Flask
import random
import time


from opentelemetry import metrics

from opentelemetry.sdk.metrics import MeterProvider

from opentelemetry.sdk.metrics.export import (
    PeriodicExportingMetricReader
)

from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
    OTLPMetricExporter
)

from opentelemetry.sdk.resources import Resource



app = Flask(__name__)



resource = Resource.create(
    {
        "service.name":
        "ecommerce-custom"
    }
)



exporter = OTLPMetricExporter(
    endpoint="http://alloy:4317",
    insecure=True
)



reader = PeriodicExportingMetricReader(
    exporter,
    export_interval_millis=5000
)



provider = MeterProvider(
    resource=resource,
    metric_readers=[reader]
)


metrics.set_meter_provider(provider)



meter = metrics.get_meter(
    "ecommerce-meter"
)



#
# COUNTER
#

orders_counter = meter.create_counter(

    name="orders_total",

    description="total ecommerce orders"

)



#
# HISTOGRAM
#

checkout_histogram = meter.create_histogram(

    name="checkout_duration_seconds",

    description="checkout duration"

)




#
# GAUGE
#

active_cart_count = 0



def cart_callback(options):

    return [

        metrics.Observation(
            active_cart_count
        )

    ]



cart_gauge = meter.create_observable_gauge(

    name="active_carts",

    callbacks=[
        cart_callback
    ]

)




@app.route("/")
def home():

    return {

        "app":"custom metrics alloy demo"

    }




@app.route("/cart/add")
def cart():

    global active_cart_count


    active_cart_count += random.randint(
        1,
        5
    )


    return {

        "active_carts":
        active_cart_count

    }





@app.route("/checkout")
def checkout():

    global active_cart_count


    start=time.time()


    time.sleep(
        random.uniform(
            0.1,
            1
        )
    )


    orders_counter.add(

        1,

        {
            "status":"success"
        }

    )


    checkout_histogram.record(

        time.time()-start

    )


    active_cart_count=0



    return {

        "checkout":"complete"

    }




if __name__=="__main__":

    app.run(

        host="0.0.0.0",

        port=5000

    )
