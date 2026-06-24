
#!/bin/bash


URL="http://localhost:5000/checkout"


echo "Starting ecommerce user journey load"


while true
do

echo "-----------------------------"
echo "New customer batch"
echo "-----------------------------"


for i in {1..20}
do

(
CUSTOMER=$(( RANDOM % 10000 ))

echo "customer-$CUSTOMER buying product"


curl -s \
-H "x-customer-id: customer-$CUSTOMER" \
-H "x-cart-id: cart-$RANDOM" \
-H "x-order-id: order-$RANDOM" \
$URL >/dev/null


)&


done


wait


sleep 2


done
