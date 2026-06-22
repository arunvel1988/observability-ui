import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

while True:

    logging.info(
        "checkout completed"
    )

    logging.error(
        "SECURITY invalid login attempt"
    )

    time.sleep(2)