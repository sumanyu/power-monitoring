#!/bin/bash

set -e
echo "Setting up VM..."

echo "Installing system tools..."
sudo apt-get update

cd /opt

sudo chown -R vagrant .

wget http://grafanarel.s3.amazonaws.com/grafana-1.9.1.tar.gz
find . -type f -name "grafana*" -exec tar -zxvf {} \;
cd $(find . -type d -name "grafana*")
wget http://pastebin.com/raw.php?i=pCMQYCWy -O config.js
rm config.sample.js
tmux new -d -s my-session "python -m SimpleHTTPServer 8095"

cd /opt

wget http://s3.amazonaws.com/influxdb/influxdb_latest_amd64.deb
sudo dpkg -i influxdb_latest_amd64.deb
cd influxdb

sudo chmod 777 -R .

sudo service influxdb start

sleep 10s

curl -X POST 'http://localhost:8086/db?u=root&p=root' -d '{"name": "demo"}'

sudo apt-get -y install python-pip
sudo pip install Flask
sudo pip install influxdb