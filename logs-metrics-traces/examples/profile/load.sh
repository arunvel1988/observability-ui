#!/bin/bash

echo "Starting Python profiling load..."

while true
do

  echo "FAST request"
  curl -s http://localhost:5000/fast
  echo ""

  echo "SLOW CPU request"
  curl -s http://localhost:5000/slow
  echo ""

  echo "ERROR request"
  curl -s http://localhost:5000/error
  echo ""

  sleep 1

done
