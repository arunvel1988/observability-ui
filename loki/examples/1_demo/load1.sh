#!/bin/bash

URL="http://localhost:5000"

while true
do
  curl -s $URL/ >/dev/null
  curl -s $URL/payment >/dev/null
  curl -s $URL/error >/dev/null

  # bad logs endpoint
  curl -s $URL/badlog >/dev/null

  # mixed logs
  curl -s $URL/mix >/dev/null

  # simulate traffic spike
  echo "level=info ts=$(date) caller=metrics.go component=frontend status=200 query=test" >> /tmp/app.log

  sleep 1
done
