#!/bin/bash

echo "Generating Loki test traffic..."

while true
do

  echo "DEBUG request"
  curl -s http://localhost:5000/debug
  echo


  echo "SECURITY request"
  curl -s http://localhost:5000/security
  echo


  sleep 1

done