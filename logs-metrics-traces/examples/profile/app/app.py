from flask import Flask
import time
import random


import pyroscope



from opentelemetry import trace


from opentelemetry.sdk.trace import TracerProvider


from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor
)


from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter
)


from opentelemetry.instrumentation.flask import FlaskInstrumentor





#
# Pyroscope continuous profiling
#

pyroscope.configure(

    application_name="python-profile-app",

    server_address="http://pyroscope:4040",

    tags={
        "env":"demo"
    }

)





#
# OpenTelemetry tracing
#

provider = TracerProvider()


trace.set_tracer_provider(provider)


exporter = OTLPSpanExporter(
    endpoint="http://alloy:4317",
    insecure=True
)


provider.add_span_processor(
    BatchSpanProcessor(exporter)
)



app = Flask(__name__)


FlaskInstrumentor().instrument_app(app)


tracer = trace.get_tracer(__name__)





def cpu_work():


    total = 0


    for i in range(10000000):

        total += i*i


    return total






@app.route("/fast")

def fast():


    return "fast response"







@app.route("/slow")

def slow():


    with tracer.start_as_current_span(
        "expensive-calculation"
    ):


        cpu_work()


        time.sleep(
            random.random()
        )


    return "slow response"





@app.route("/error")

def error():


    with tracer.start_as_current_span(
        "error-operation"
    ):


        raise Exception(
            "demo failure"
        )




app.run(
    host="0.0.0.0",
    port=5000
)
