from prometheus_client import Counter, start_http_server
import random
import time


orders = Counter(
    "orders_total",
    "Total orders",
    [
        "user_id",
        "session_id",
        "product_id"
    ]
)


start_http_server(8000)


while True:

    orders.labels(
        user_id=str(random.randint(1,1000000)),
        session_id=str(random.randint(1,1000000)),
        product_id=str(random.randint(1,10000))
    ).inc()


    time.sleep(0.01)
