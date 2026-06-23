import logging
import time


logger=logging.getLogger()

handler=logging.FileHandler("/logs/app.log")

logger.addHandler(handler)

logger.setLevel(logging.INFO)



while True:


    logger.info(
    "{ service payment event checkout"
    )


    time.sleep(1)

