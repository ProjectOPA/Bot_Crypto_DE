#!/bin/bash
python3 extract_history.py
python3 transform_history.py
crontab -l | { cat; echo "0 0 * * * python3 /application/extract_history.py && python3 /application/transform_history.py"; } | crontab -
service cron restart
echo "Historical data have correctly been collected and processed"
tail -f /dev/null