#!/bin/bash

echo "Starting load test for observability stack..."

URL="http://localhost:5000"

for i in {1..200}
do
  curl -s $URL/ > /dev/null
  curl -s $URL/buy > /dev/null

  # generate errors randomly
  if [ $((RANDOM % 10)) -eq 0 ]; then
    curl -s $URL/error > /dev/null
  fi

  echo "request batch $i sent"
  sleep 0.1
done

echo "Load generation completed"
