#!/bin/bash

set -e

TEMPO_ADDR="http://localhost:3200"

DEFAULT_QUERY='{resource.service.name="ecommerce-app"}'

while true; do

echo ""
echo "=================================================="
echo "           TEMPO CLI MANAGEMENT CONSOLE"
echo "=================================================="
echo "TEMPO ENDPOINT: $TEMPO_ADDR"
echo "NETWORK MODE: host (required for working DNS)"
echo ""
echo "1) Help / Version"
echo "2) Query Trace by TraceID"
echo "3) Search Traces (default ecommerce-app)"
echo "4) Search Traces (custom TraceQL)"
echo "5) Search Tags"
echo "6) Search Tag Values"
echo "7) List Blocks"
echo "8) Analyse Block"
echo "9) Analyse Blocks"
echo "10) View Parquet Schema"
echo "11) Metrics Query"
echo "12) Trace Summary"
echo "13) Cache Summary"
echo "14) Compaction Summary"
echo "15) Column List"
echo "16) Migrate Config"
echo "17) Migrate Tenant"
echo "18) Redact Trace"
echo "19) Exit"
echo ""
read -p "Select option: " opt

case $opt in

1)
echo ">>> TEMPO CLI HELP"
docker run --rm grafana/tempo-cli:latest --help
;;

2)
echo ">>> TRACE BY TRACE ID"
read -p "Enter Trace ID: " id

docker run --rm --network=host grafana/tempo-cli:latest \
query api trace-id "$TEMPO_ADDR" "$id"
;;

3)
echo ">>> DEFAULT TRACE SEARCH (ecommerce-app)"

docker run --rm --network=host grafana/tempo-cli:latest \
query api search "$DEFAULT_QUERY"
;;

4)
echo ">>> CUSTOM TRACEQL SEARCH"
read -p "Enter TraceQL (press ENTER for default): " q

if [ -z "$q" ]; then
  q=$DEFAULT_QUERY
fi

docker run --rm --network=host grafana/tempo-cli:latest \
query api search "$q"
;;

5)
echo ">>> SEARCH TAGS"

docker run --rm --network=host grafana/tempo-cli:latest \
query api search-tags http://localhost:3200 now-1h now
;;

6)
echo ">>> SEARCH TAG VALUES"
read -p "Enter tag name: " tag

docker run --rm --network=host grafana/tempo-cli:latest \
query api search-tag-values "$tag"
;;

7)
echo ">>> LIST BLOCKS"

docker run --rm --network=host grafana/tempo-cli:latest \
list blocks
;;

8)
echo ">>> ANALYSE BLOCK"
read -p "Enter block name: " b

docker run --rm --network=host grafana/tempo-cli:latest \
analyse block "$b"
;;

9)
echo ">>> ANALYSE BLOCKS"

docker run --rm --network=host grafana/tempo-cli:latest \
analyse blocks
;;

10)
echo ">>> PARQUET SCHEMA"

docker run --rm --network=host grafana/tempo-cli:latest \
view schema
;;

11)
echo ">>> METRICS QUERY"
read -p "Enter query: " mq

docker run --rm --network=host grafana/tempo-cli:latest \
query api metrics "$mq"
;;

12)
echo ">>> TRACE SUMMARY"
read -p "Enter Trace ID: " tid

docker run --rm --network=host grafana/tempo-cli:latest \
query trace-summary "$tid"
;;

13)
echo ">>> CACHE SUMMARY"

docker run --rm --network=host grafana/tempo-cli:latest \
list cache-summary
;;

14)
echo ">>> COMPACTION SUMMARY"

docker run --rm --network=host grafana/tempo-cli:latest \
list compaction-summary
;;

15)
echo ">>> COLUMN LIST"
read -p "Enter column: " col

docker run --rm --network=host grafana/tempo-cli:latest \
list column "$col"
;;

16)
echo ">>> MIGRATE CONFIG"
read -p "Config file: " f

docker run --rm --network=host grafana/tempo-cli:latest \
migrate config "$f"
;;

17)
echo ">>> MIGRATE TENANT"
read -p "Source tenant: " s
read -p "Target tenant: " t

docker run --rm --network=host grafana/tempo-cli:latest \
migrate tenant "$s" "$t"
;;

18)
echo ">>> REDACT TRACE"
read -p "Trace IDs: " ids

docker run --rm --network=host grafana/tempo-cli:latest \
redact "$ids"
;;

19)
echo "EXITING..."
exit 0
;;

*)
echo "INVALID OPTION"
;;

esac

done
