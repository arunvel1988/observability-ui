import time
import logging


from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs import LoggingHandler


from opentelemetry.sdk._logs.export import (
    BatchLogRecordProcessor
)

from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
    OTLPLogExporter
)

from opentelemetry import _logs



provider = LoggerProvider()

_logs.set_logger_provider(provider)


exporter = OTLPLogExporter(
    endpoint="http://alloy:4317",
    insecure=True
)


provider.add_log_record_processor(
    BatchLogRecordProcessor(exporter)
)


handler = LoggingHandler(
    level=logging.INFO,
    logger_provider=provider
)


logging.basicConfig(
    level=logging.INFO,
    handlers=[handler]
)


log=logging.getLogger("checkout-service")



while True:


    log.info(
        "debug log checkout success"
    )


    log.error(
        "SECURITY invalid login detected"
    )


    print("sent logs")


    time.sleep(2)