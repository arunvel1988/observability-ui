import logging
import random
import time

logging.basicConfig(
    level=logging.INFO
)

while True:

    logging.info(
        f"user={random.randint(1,1000000)} checkout completed"
    )

    if random.randint(1,50000) == 1:

        logging.error(
            "SUPER_SECRET_SECURITY_BREACH"
        )

    time.sleep(0.001)