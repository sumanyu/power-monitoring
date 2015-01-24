#!/bin/bash

set -e
echo "Setting up VM..."

echo "Installing system tools..."
sudo apt-get update
wget http://s3.amazonaws.com/influxdb/influxdb_latest_amd64.deb
sudo dpkg -i influxdb_latest_amd64.deb
sudo service influxdb start

sudo apt-get install python-pip
sudo pip install Flask

cd /opt

curl http://grafanarel.s3.amazonaws.com/grafana-1.9.1.tar.gz
find . -type f -name "grafana*" -exec tar -zxvf {} \;
cd $(find . -type d -name "grafana*")
mv /opt/grafana_settings/config.js config.js
rm config.sample.js
python -m SimpleHTTPServer 8095 &