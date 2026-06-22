import time
import logging


logging.basicConfig(
 level=logging.INFO
)


log=logging.getLogger()



while True:

    log.info(
      "debug log"
    )

    log.error(
      "security alert"
    )

    print("logs sent")

    time.sleep(2)