import logging
import json
import time
import random


logger=logging.getLogger()

handler=logging.FileHandler("/logs/app.log")

logger.addHandler(handler)

logger.setLevel(logging.INFO)



while True:


    log={

      "service":"payment",

      "event":"checkout",

      "status":"success",

      "amount":random.randint(10,100)

    }


    logger.info(
        json.dumps(log)
    )


    time.sleep(1)

