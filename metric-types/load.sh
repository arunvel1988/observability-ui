#!/bin/bash


while true

do


curl localhost:5000/cart/add


curl localhost:5000/checkout


sleep 1


done
