#!/bin/bash


echo "Starting load generation..."


while true
do

    echo "Creating Orders"

    curl -s http://localhost:5001/order
    echo ""


    curl -s http://localhost:5001/order
    echo ""



    echo "Making Payments"

    curl -s http://localhost:5002/pay
    echo ""



    echo "-------------------------"

    sleep 2


done
