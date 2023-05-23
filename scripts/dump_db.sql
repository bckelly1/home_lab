#!/bin/bash

set -e

mysqldump --host 192.168.0.12 -u root -p --all-databases /home/brian/backups/db-dump-$(date -I'minutes').sql

