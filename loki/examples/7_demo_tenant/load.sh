#!/bin/bash


while true
do

echo "Generating traffic..."


curl -s http://localhost:5000/login > /dev/null


curl -s http://localhost:5000/payment > /dev/null


curl -s http://localhost:5000/hack > /dev/null



R=$(( RANDOM % 3 ))


if [ $R -eq 1 ]
then

 curl -s http://localhost:5000/error > /dev/null

fi



sleep 1


done