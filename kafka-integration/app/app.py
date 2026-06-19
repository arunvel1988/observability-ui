from prometheus_client import Counter,start_http_server
import random
import time


orders = Counter(
    "orders_total",
    "orders created",
    ["status"]
)


start_http_server(8000)


while True:

    status=random.choice(
        [
            "success",
            "failed"
        ]
    )


    orders.labels(
        status=status
    ).inc()


    time.sleep(1)
