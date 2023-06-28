# MTR-Monitoring

Monitoring MTR of destitations with Influxdb and Grafana

Ensure that you have InfluxDB , python installed and running. InfluxDB is a high-performance time-series database used for storing monitoring data. You can download InfluxDB from the official website and follow the installation instructions specific to your operating system.The project uses Python and some additional libraries. Make sure you have Python 3.x installed on your system. You'll also need the following Python libraries:
influxdb: This library provides the necessary functionality to connect to and interact with InfluxDB. Install it using the command: 

``` 
pip install influxdb
```

1) Login to your InfluxDB and write these commands:

```
>CREATE DATABASE mtr
>USE mtr
>CREATE USER user with PASSWORD ‘12345’ WITH ALL PRIVILEGES
>GRANT ALL ON mtr TO user
```
2) Create a bash script for collect data mtr, for example the name of file is mtr-exporter.sh in folder /opt/mtr-project and put these script into those file have you created. in this scenario all files will put in folder /opt/mtr-project

``` 
# mkdir -p /opt/mtr-project
```
```
# vi /opt/mtr-project/mtr-exporter.sh
```

Put the scrip str-exporter.sh and save.

``` 
# chmod +x /opt/mtr-project/mtr_exporter.sh
```

3) Create List of IP Destination that you will monitor. For example, www.example1.com
```
# vi /opt/mtr-project/list-ip
```
5) Create a python script for export data mtr into Influxdb database, for example the name of file saving-data.py and put these script into your have you created.

6) Create a linux service mtr-exporter, the example service name is mtr-exporter, create a file mtr-exporter.service in folder /lib/systemd/system

```
[Unit]
Description=mtr exporter
After=multi-user.target

[Service]
Type=idle
ExecStart=/bin/bash /opt/mtr-project/mtr-export.sh

[Install]
WantedBy=multi-user.target
```
``` 
systemctl daemon-reload
```
``` 
systemctl start mtr-exporter.service
```

6) Add DataSource in Grafana
7) Make Grafana Dashboards.


=========================================================================================

Explain Codes:
your-influxdb-host: Replace this with the IP address or hostname of your InfluxDB server.
www.example1.com, www.example2.com, www.example3.com: Replace these with the desired hostnames or IP addresses you want to monitor.

Certainly! Let's go through the codes and provide explanations for each section.

list-ip:
This file contains a list of destination IP addresses or hostnames that you want to monitor with MTR (My Traceroute). Each destination should be on a separate line. In this example, three destinations are listed: www.example1.com, www.example2.com, and www.example3.com. You can modify this file to include your desired destinations.

mtr-exporter.sh:

This shell script is responsible for executing the MTR command and exporting the results to InfluxDB for monitoring. Here's a breakdown of its functionalities:

**INTERVAL**: This variable represents the interval (in seconds) at which MTR will be executed to monitor the destinations. In this example, the interval is set to 60 seconds.
**INFLUXDB_HOST**: This variable holds the IP address or hostname of the InfluxDB server where the monitoring data will be stored.
**INFLUXDB_PORT**: This variable specifies the port number for the InfluxDB server.
The **monitor_mtr** function is responsible for executing MTR for each destination listed in list-ip. It reads each line from the file, resolves the hostname to an IP address, and then runs MTR using the IP address. The MTR results are piped to the saving-data.py script, which exports the data to InfluxDB.

The script checks if the mtr command is installed. If not found, it displays an error message and exits. Otherwise, it enters a continuous loop where MTR is executed for each destination at the specified interval.

saving-data.py:

This Python script is responsible for parsing the MTR JSON output and saving the relevant data to InfluxDB. Let's understand the different sections of the script:

**get_cmd_arguments**: This function uses the argparse module to parse command-line arguments. It retrieves the InfluxDB host and port values provided when executing the script.
The main function is the entry point of the script. It establishes a connection to the InfluxDB server using the provided host, port, username, and password.

The MTR JSON data is read from the standard input using json.load(sys.stdin).
The destination and current time are extracted from the MTR data.
The **HubEntry** class is defined as a subclass of SeriesHelper from the influxdb module. It represents the data to be stored in InfluxDB and defines the series name, fields, and tags.
The script iterates through the hubs in the MTR data and extracts relevant information such as loss percentage, sent packets, last latency, average latency, best latency, worst latency, and standard deviation.
If the hub name is "???", it is skipped as it represents private hubs.
The data is modified if needed to ensure proper sorting when there are more than nine hops.
An instance of HubEntry is created for each hub, and the data is added to InfluxDB.
The script keeps track of existing entries to avoid duplicates.
Finally, the changes are committed to InfluxDB using HubEntry.commit(client=client).
You need to ensure that the InfluxDB host, port, username, and password are correctly provided in the script to establish a connection and store the MTR data.

That's a high-level overview of the code. It allows you to monitor multiple destinations using MTR and store the results in InfluxDB for further analysis and visualization.
