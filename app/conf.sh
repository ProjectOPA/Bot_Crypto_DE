#!/bin/bash
# export PUBLIC_IP=$(curl -s http://ifconfig.me/ip)
# docker-compose up -d

# pid=$!
# wait $pid
# docker-compose up --scale kafka=2 -d
# pid=$!
# wait $pid
# CRON_CMD="* * * * * ./run_extract_history.sh"
python3 ./extract/extract_history.py