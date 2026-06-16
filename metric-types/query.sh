#!/bin/bash


PROM="http://localhost:9090/api/v1/query"


run_query () {

echo
echo "========================================"
echo "$1"
echo "PromQL: $2"
echo "========================================"

curl -sG $PROM \
--data-urlencode "query=$2"

echo
}



#########################################
# COUNTER EXAMPLES
# Metric:
# orders_total
#########################################


run_query \
"1. Raw counter value" \
"orders_total"



run_query \
"2. Orders per second (RATE)" \
"rate(orders_total[1m])"



run_query \
"3. Orders in last 5 minutes (INCREASE)" \
"increase(orders_total[5m])"



run_query \
"4. Total orders by status label" \
"sum(orders_total) by (status)"



run_query \
"5. Order rate by status" \
"sum(rate(orders_total[1m])) by (status)"



run_query \
"6. Total orders all services" \
"sum(orders_total)"



run_query \
"7. Top order producers" \
"topk(5, orders_total)"





#########################################
# GAUGE EXAMPLES
# Metric:
# active_carts
#########################################



run_query \
"8. Current active carts" \
"active_carts"



run_query \
"9. Average carts last 5 min" \
"avg_over_time(active_carts[5m])"



run_query \
"10. Max carts last 5 min" \
"max_over_time(active_carts[5m])"



run_query \
"11. Min carts last 5 min" \
"min_over_time(active_carts[5m])"



run_query \
"12. Cart changes" \
"changes(active_carts[5m])"



run_query \
"13. Predict carts in future" \
"predict_linear(active_carts[10m],300)"






#########################################
# HISTOGRAM
# Metric:
# checkout_duration_seconds
#########################################



run_query \
"14. Histogram buckets" \
"checkout_duration_seconds_bucket"



run_query \
"15. Request count from histogram" \
"checkout_duration_seconds_count"



run_query \
"16. Total latency sum" \
"checkout_duration_seconds_sum"




run_query \
"17. Average checkout latency" \
"rate(checkout_duration_seconds_sum[5m]) / rate(checkout_duration_seconds_count[5m])"




run_query \
"18. P50 latency" \
"histogram_quantile(0.50, rate(checkout_duration_seconds_bucket[5m]))"




run_query \
"19. P90 latency" \
"histogram_quantile(0.90, rate(checkout_duration_seconds_bucket[5m]))"




run_query \
"20. P95 latency" \
"histogram_quantile(0.95, rate(checkout_duration_seconds_bucket[5m]))"




run_query \
"21. P99 latency" \
"histogram_quantile(0.99, rate(checkout_duration_seconds_bucket[5m]))"





#########################################
# LABEL FILTERING
#########################################



run_query \
"22. Successful orders only" \
"orders_total{status=\"success\"}"



run_query \
"23. Regex label filter" \
"orders_total{status=~\"success|failed\"}"




#########################################
# AGGREGATION
#########################################



run_query \
"24. Count series" \
"count(orders_total)"



run_query \
"25. Average value" \
"avg(orders_total)"



run_query \
"26. Maximum value" \
"max(orders_total)"



run_query \
"27. Minimum value" \
"min(orders_total)"





#########################################
# TIME OPERATORS
#########################################



run_query \
"28. Value 5 minutes ago" \
"orders_total offset 5m"



run_query \
"29. Rate comparison old data" \
"rate(orders_total[1m] offset 5m)"





#########################################
# ALERT STYLE QUERIES
#########################################


run_query \
"30. High latency alert example" \
"histogram_quantile(0.95, rate(checkout_duration_seconds_bucket[5m])) > 0.5"




run_query \
"31. Too many carts alert" \
"active_carts > 20"




run_query \
"32. Missing metric check" \
"absent(orders_total)"





#########################################
# SERVICE LABEL EXAMPLES
#########################################



run_query \
"33. Metrics from ecommerce service" \
'{service_name="ecommerce-custom"}'



run_query \
"34. Count metrics per service" \
"count by(service_name)({service_name!=\"\"})"
