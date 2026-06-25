#!/bin/bash

set -e

MIMIR="http://localhost:9009"
TENANT="demo"

while true; do

echo ""
echo "=================================================="
echo "         MIMIRTOOL MANAGEMENT CONSOLE"
echo "=================================================="
echo ""
echo "TENANT: $TENANT"
echo "MIMIR: $MIMIR"
echo ""
echo "1) Version Check"
echo "2) Health Check"
echo "3) Create Rule File"
echo "4) Check Rules"
echo "5) Load Rules"
echo "6) List Rules"
echo "7) Print Rules"
echo "8) Diff Rules"
echo "9) Sync Rules"
echo "10) Analyze Rule File"
echo "11) Analyze Ruler"
echo "12) Analyze Grafana"
echo "13) Analyze Prometheus"
echo "14) PromQL Format"
echo "15) Validate Alerts"
echo "16) Bucket Validation"
echo "17) Runtime Config Validate"
echo "18) Exit"
echo ""
read -p "Select option: " opt


case $opt in

1)
echo ">>> VERSION"
mimirtool version
;;

2)
echo ">>> HEALTH CHECK"
curl -s $MIMIR/ready || echo "NOT READY"
;;

3)
echo ">>> CREATING RULE FILE"
cat > rules.yml <<EOF
groups:
- name: demo
  interval: 30s
  rules:
  - record: job:cpu:avg5m
    expr: avg(cpu_usage)
  - record: job:mem:avg5m
    expr: avg(memory_usage)
  - alert: HighCPU
    expr: job:cpu:avg5m > 0.8
EOF
echo "rules.yml created"
;;

4)
echo ">>> RULE CHECK"
mimirtool rules check rules.yml
;;

5)
echo ">>> RULE LOAD"
mimirtool rules load --address=$MIMIR --id=$TENANT rules.yml
;;

6)
echo ">>> RULE LIST"
mimirtool rules list --address=$MIMIR --id=$TENANT
;;

7)
echo ">>> RULE PRINT"
mimirtool rules print --address=$MIMIR --id=$TENANT
;;

8)
echo ">>> RULE DIFF"
mimirtool rules diff --address=$MIMIR --id=$TENANT rules.yml || true
;;

9)
echo ">>> RULE SYNC"
mimirtool rules sync --address=$MIMIR --id=$TENANT rules.yml || true
;;

10)
echo ">>> ANALYZE RULE FILE"
mimirtool analyze rule-file rules.yml || true
;;

11)
echo ">>> ANALYZE RULER"
mimirtool analyze ruler --address=$MIMIR --id=$TENANT || true
;;

12)
echo ">>> ANALYZE GRAFANA"
mimirtool analyze grafana --address=$MIMIR --id=$TENANT || true
;;

13)
echo ">>> ANALYZE PROMETHEUS"
mimirtool analyze prometheus --address=$MIMIR --id=$TENANT || true
;;

14)
echo ">>> PROMQL FORMAT"
read -p "Enter query: " q
mimirtool promql format "$q"
;;

15)
echo ">>> ALERT VALIDATION"
mimirtool validate alerts-file alerts.yml || true
;;

16)
echo ">>> BUCKET VALIDATION"
mimirtool bucket-validation || true
;;

17)
echo ">>> RUNTIME CONFIG VALIDATE"
mimirtool runtime-config validate runtime.yaml || true
;;

18)
echo "EXITING..."
exit 0
;;

*)
echo "INVALID OPTION"
;;

esac

done
