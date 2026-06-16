!/bin/bash

URL="http://localhost:5000"

echo "Starting OpenTelemetry load test"


echo "Generating normal traffic..."

for i in {1..500}
do

 curl -s $URL/cart > /dev/null &
 curl -s $URL/checkout > /dev/null &
 curl -s $URL/payment > /dev/null &

 if (( $i % 50 == 0 ))
 then
   echo "sent $i batches"
 fi

 sleep 0.05

done


wait


echo "Generating errors..."

for i in {1..50}
do

 curl -s $URL/error > /dev/null

done



echo "Generating more random traffic..."

for i in {1..300}
do
