#!/bin/bash
# export PUBLIC_IP=$(curl -s http://ifconfig.me/ip)
#export PUBLIC_IP=$(ipconfig getifaddr en0)
#docker-compose up --scale kafka=2 -d
#pid=$!
#wait $pid

python3 ./extract/extract_history.py