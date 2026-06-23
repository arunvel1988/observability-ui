import logging
import uuid
import time
import json


log=logging.getLogger()

handler=logging.FileHandler("/logs/app.log")

log.addHandler(handler)

log.setLevel(logging.INFO)



while True:


    data={

      "service":"checkout",

      "event":"login",

      "user_id":str(uuid.uuid4())

    }


    log.info(json.dumps(data))


    time.sleep(0.01)
