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
    "service.name": "ecommerce-app",
    "environment": "dev"
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



metric_exporter = OTLPMetricExporter(
    endpoint="alloy:4317",
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


meter = metrics.get_meter("shop")


cart_counter = meter.create_counter(
    "cart_count"
)


checkout_counter = meter.create_counter(
    "checkout_count"
)





# =====================
# TRACES
# =====================


from opentelemetry import trace


from opentelemetry.trace import (
    Status,
    StatusCode
)


from opentelemetry.sdk.trace import TracerProvider


from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor
)


from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter
)



trace_provider = TracerProvider(
    resource=resource
)



trace_provider.add_span_processor(

    BatchSpanProcessor(

        OTLPSpanExporter(

            endpoint="alloy:4317",

            insecure=True

        )

    )

)



trace.set_tracer_provider(
    trace_provider
)



tracer = trace.get_tracer(
    "shop-tracer"
)






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



logger_provider = LoggerProvider(
    resource=resource
)



logger_provider.add_log_record_processor(

    BatchLogRecordProcessor(

        OTLPLogExporter(

            endpoint="alloy:4317",

            insecure=True

        )

    )

)



handler = LoggingHandler(
    logger_provider=logger_provider
)



logging.basicConfig(

    level=logging.INFO,

    handlers=[handler]

)



logger = logging.getLogger(
    "shop"
)





# =====================
# FLASK APP
# =====================


app = Flask(__name__)




@app.route("/")
def home():


    return """

    OpenTelemetry Demo

    /cart

    /checkout

    /payment

    /slow

    /error

    """






@app.route("/cart")
def cart():


    with tracer.start_as_current_span(
        "cart-operation"
    ):


        cart_counter.add(1)


        logger.info(
            "Product added to cart"
        )


        time.sleep(
            random.random()
        )


        return "cart added"








@app.route("/checkout")
def checkout():


    with tracer.start_as_current_span(
        "checkout-operation"
    ):


        checkout_counter.add(1)


        logger.info(
            "Checkout completed"
        )


        return "checkout"









@app.route("/payment")
def payment():


    with tracer.start_as_current_span(
        "payment-operation"
    ):


        logger.info(
            "Payment successful"
        )


        return "payment done"








# =====================
# SLOW TRACE TEST
# =====================


@app.route("/slow")
def slow():


    with tracer.start_as_current_span(
        "slow-operation"
    ):


        time.sleep(3)


        logger.info(
            "slow request completed"
        )


        return "slow done"









# =====================
# ERROR TRACE TEST
# =====================


@app.route("/error")
def error():


    with tracer.start_as_current_span(
        "error-operation"
    ) as span:


        try:


            raise Exception(
                "payment failed"
            )


        except Exception as e:


            span.record_exception(e)


            span.set_status(

                Status(

                    StatusCode.ERROR

                )

            )


            logger.error(
                "payment failed"
            )


            return "error generated", 500







app.run(

    host="0.0.0.0",

    port=5000

)
