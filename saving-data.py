#!/usr/bin/env python5
import argparse
import json
import sys
import datetime as dt
import logging

from influxdb import InfluxDBClient, SeriesHelper

logging.basicConfig(level=logging.INFO)
db_name = 'mtr'
user = 'user'
password = '12345'

class HubEntry(SeriesHelper):
    class Meta:
        series_name = '{destination}'
        fields = ['time', 'loss', 'snt', 'last', 'avg', 'best', 'wrst', 'stdev']
        tags = ['destination', 'step', 'hostname']

def get_cmd_arguments():
    parser = argparse.ArgumentParser(description='JSON parser')
    parser.add_argument('--host', default='your-influxdb-host', help='influxdb host')
    parser.add_argument('--port', default=8086, help='influxdb port')
    return parser.parse_args()

def main():
    args = get_cmd_arguments()

    # Connect to InfluxDB
    client = InfluxDBClient(host=args.host, port=args.port, username=user, password=password, database=db_name)
    mtr_result = json.load(sys.stdin)
    # ping destination
    destination = mtr_result['report']['mtr']['dst']
    report_time = dt.datetime.utcnow()
    existing_entries = set()  # Keep track of existing entries
    for hub in mtr_result['report']['hubs']:
        hub_name = hub['host']

        # Exclude private hubs with name "???"
        if hub_name == '???':
            continue

        # Check if the entry already exists
        if (destination, hub['host']) in existing_entries:
            continue  # Skip if the entry already exists

        # Modifying the data if needed so that it can be easily sorted in the event of more than 9 hops.
        if len(str(hub['count'])) < 2:
            hop = "0" + str(hub['count']) + "---" + hub['host']
            step = hop.split("---")[0]
            hostname = hop.split("---")[1]
        else:
            hop = str(hub['count']) + "---" + hub['host']
            step = hop.split("---")[0]
            hostname = hop.split("---")[1]

        HubEntry(
            time=report_time,
            destination=destination,
            step=step,
            hostname=hostname,
            loss=hub['Loss%'],
            snt=hub['Snt'],
            last=hub['Last'],
            avg=hub['Avg'],
            best=hub['Best'],
            wrst=hub['Wrst'],
            stdev=hub['StDev']
        )

        # Add the entry to the set of existing entries
        existing_entries.add((destination, hub['host']))
    HubEntry.commit(client=client)  # Pass the InfluxDBClient instance to the commit() method

if __name__ == '__main__':
    main()
