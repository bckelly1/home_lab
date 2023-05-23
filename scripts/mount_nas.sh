#!/bin/bash

# Requires sudo apt install cifs-utils
# /mnt/nas must exist and be a directory
# Credential file must be formatted as:
#  username=****
#  password=****

sudo mount.cifs //192.168.0.12/brian-home /mnt/nas -o credentials=/home/brian/.cifs-nas

