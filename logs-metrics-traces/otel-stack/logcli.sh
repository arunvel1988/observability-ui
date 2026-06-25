#!/bin/bash

set -e

LOKI_ADDR="http://localhost:3100"
DEFAULT_QUERY='{service_name="ecommerce-app"}'

while true; do

echo ""
echo "=================================================="
echo "          LOGCLI MANAGEMENT CONSOLE"
echo "=================================================="
echo "LOKI: $LOKI_ADDR"
echo "DEFAULT QUERY: $DEFAULT_QUERY"
echo ""
echo "1) Version Check"
echo "2) Run Default Query (ecommerce-app)"
echo "3) Run Custom Query"
echo "4) Instant Query"
echo "5) Show Labels"
echo "6) Show Series"
echo "7) Stats"
echo "8) Volume"
echo "9) Detect Fields"
echo "10) Format LogQL"
echo "11) Exit"
echo ""
read -p "Select option: " opt


case $opt in

1)
echo ">>> LOGCLI VERSION"
logcli --version
;;

2)
echo ">>> DEFAULT QUERY (ECOMMERCE APP)"

logcli query --addr=$LOKI_ADDR "$DEFAULT_QUERY"
;;

3)
echo ">>> CUSTOM QUERY"
read -p "Enter LogQL (press enter for default): " q

if [ -z "$q" ]; then
    q=$DEFAULT_QUERY
fi

logcli query --addr=$LOKI_ADDR "$q"
;;

4)
echo ">>> INSTANT QUERY"
read -p "Enter query: " q

if [ -z "$q" ]; then
    q=$DEFAULT_QUERY
fi

logcli instant-query --addr=$LOKI_ADDR "$q"
;;

5)
echo ">>> LABELS"
logcli labels --addr=$LOKI_ADDR
;;

6)
echo ">>> SERIES"
read -p "Enter matcher (default ecommerce-app): " m

if [ -z "$m" ]; then
    m="$DEFAULT_QUERY"
fi

logcli series --addr=$LOKI_ADDR "$m"
;;

7)
echo ">>> STATS"
read -p "Enter query (default ecommerce-app): " q

if [ -z "$q" ]; then
    q="$DEFAULT_QUERY"
fi

logcli stats --addr=$LOKI_ADDR "$q"
;;

8)
echo ">>> VOLUME"
read -p "Enter query (default ecommerce-app): " q

if [ -z "$q" ]; then
    q="$DEFAULT_QUERY"
fi

logcli volume --addr=$LOKI_ADDR "$q"
;;

9)
echo ">>> DETECTED FIELDS"
read -p "Enter query (default ecommerce-app): " q

if [ -z "$q" ]; then
    q="$DEFAULT_QUERY"
fi

logcli detected-fields --addr=$LOKI_ADDR "$q"
;;

10)
echo ">>> FORMAT LOGQL"
read -p "Enter LogQL: " q
logcli fmt "$q"
;;

11)
echo "EXITING..."
exit 0
;;

*)
echo "INVALID OPTION"
;;

esac

done
