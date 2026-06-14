from flask import Flask
import logging


# ==================
# METRICS
# ==================

from opentelemetry import metrics

from opentelemetry.sdk.metrics import MeterProvider

from opentelemetry.sdk.metrics.export import (
    PeriodicExportingMetricReader
)

from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
    OTLPMetricExporter
)


# ==================
# LOGS
# ==================

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


from opentelemetry.sdk.resources import Resource



app = Flask(__name__)



resource = Resource.create({

    "service.name":"shopping-service"

})



# ======================
# Metrics OTEL
# ======================


metric_exporter = OTLPMetricExporter(

    endpoint="http://alloy:4317",

    insecure=True

)


reader = PeriodicExportingMetricReader(
    metric_exporter,
    export_interval_millis=5000
)


metrics.set_meter_provider(

    MeterProvider(

        resource=resource,

        metric_readers=[reader]

    )

)


meter = metrics.get_meter("shop-meter")


cart_counter = meter.create_counter(

    "cart_count"

)


checkout_counter = meter.create_counter(

    "checkout_count"

)



# ======================
# Logs OTEL
# ======================


logger_provider = LoggerProvider(

    resource=resource

)


log_exporter = OTLPLogExporter(

    endpoint="http://alloy:4317",

    insecure=True

)


logger_provider.add_log_record_processor(

    BatchLogRecordProcessor(

        log_exporter

    )

)


handler = LoggingHandler(

    logger_provider=logger_provider

)


logging.basicConfig(

    level=logging.INFO,

    handlers=[handler]

)


logger=logging.getLogger(__name__)



@app.route("/cart")

def cart():

    cart_counter.add(
        1,
        {
            "api":"cart"
        }
    )


    logger.info(

        "User added product to cart"

    )


    return "cart"



@app.route("/checkout")

def checkout():


    checkout_counter.add(
        1,
        {
            "api":"checkout"
        }
    )


    logger.info(

        "User completed checkout"

    )


    return "checkout"



app.run(

    host="0.0.0.0",

    port=5000

)
