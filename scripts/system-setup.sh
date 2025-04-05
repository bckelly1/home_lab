#!/bin/bash

set -e

sudo apt update
sudo apt upgrade -y
sudo apt install -y \
	cifs-utils \
	git \
	docker-ce \
	net-tools \
	nmap \
	mariadb-client \
	htop \
	vim \
	unattended-upgrades

sudo cp ./logrotate.config /etc/logrotate.d/

