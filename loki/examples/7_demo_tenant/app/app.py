import logging
import time
import random


audit = logging.getLogger("audit")
error = logging.getLogger("error")


audit_handler = logging.FileHandler("/logs/audit.log")
error_handler = logging.FileHandler("/logs/error.log")


fmt=logging.Formatter(
'{"time":"%(asctime)s","level":"%(levelname)s","msg":"%(message)s"}'
)


audit_handler.setFormatter(fmt)
error_handler.setFormatter(fmt)


audit.addHandler(audit_handler)
error.addHandler(error_handler)


audit.setLevel(logging.INFO)
error.setLevel(logging.ERROR)


users=[
"arun",
"admin",
"john"
]


while True:


    user=random.choice(users)


    audit.info(
      f"LOGIN_SUCCESS user={user}"
    )


    audit.info(
      f"PAYMENT_COMPLETED user={user}"
    )



    try:

        if random.randint(1,2)==1:

            raise Exception(
            "database timeout"
            )


    except Exception as e:


        error.error(
        f"APP_FAILURE reason={e}"
        )


    time.sleep(5)