#! /bin/bash

set -e 

du -a . | sort -n -r | head -n 5
