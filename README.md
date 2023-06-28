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

