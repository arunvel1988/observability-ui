#!/bin/bash

echo "Starting profiling load generator..."

while true
do

  echo "FAST endpoint"
  curl -s http://localhost:5000/fast > /dev/null

  echo "CPU HEAVY"
  curl -s http://localhost:5000/cpu-heavy > /dev/null

  echo "MEMORY HEAVY"
  curl -s http://localhost:5000/memory-heavy > /dev/null

  echo "MIXED LOAD"
  curl -s http://localhost:5000/mixed > /dev/null

  echo "DB SIMULATION"
  curl -s http://localhost:5000/db-sim > /dev/null

  echo "ERROR CASE"
  curl -s http://localhost:5000/error > /dev/null

  sleep 1

done
