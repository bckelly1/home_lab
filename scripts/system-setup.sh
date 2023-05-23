#!/bin/bash

set -e

sudo apt update
sudo apt upgrade -y
sudo apt install -y \
	cifs-utils \
	git \
	docker-ce \
	iconfig \
	nmap \
	htop \
	vim \
	unattended-upgrades

sudo cp ./logrotate.conf /etc/logrotate.d/

