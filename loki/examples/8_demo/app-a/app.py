import logging
import time
import random
import json


log=logging.getLogger()

handler=logging.FileHandler("/logs/app.log")

log.addHandler(handler)

log.setLevel(logging.INFO)


users=["arun","john","admin"]


while True:

    data={
      "service":"checkout",
      "event":"payment",
      "user":random.choice(users)
    }


    log.info(json.dumps(data))


    time.sleep(0.5)
