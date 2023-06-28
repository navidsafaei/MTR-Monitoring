#!/bin/bash

INTERVAL=60
INFLUXDB_HOST="your-influxdb-host"
INFLUXDB_PORT=8086

function monitor_mtr() {
  while read -r MTR_HOST; do
    IP_ADDRESS=$(nslookup "$MTR_HOST" | awk '/Address/ { print $2  }' | tail -n 1)
    if [[ -n $IP_ADDRESS ]]; then
      ( /usr/bin/mtr --json $IP_ADDRESS | /usr/bin/python3 /opt/mtr-exporter-influx/saving_data.py --host $INFLUXDB_HOST --port $INFLUXDB_PORT ) &
    else
      echo "Failed to resolve hostname: $MTR_HOST"
    fi
  done < /opt/mtr-exporter-influx/list-ip-dest
}

which mtr &>/dev/null
if [ $? -eq 1 ]; then
  echo "mtr not found, please install mtr"
  exit 1
else
  echo "collecting data..."
fi

while true; do
  monitor_mtr
  sleep $INTERVAL
done
