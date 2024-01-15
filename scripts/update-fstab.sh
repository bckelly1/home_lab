#!/usr/bin/env bash

# This needs to run as root. It adds an entry to the /etc/fstab to auto-mount the NAS folder. This allows the docker
#   mounts to use a single external volume mount rather than each individually connecting to the NAS.

NAS_IP=192.168.0.12
NAS_SHARE_FOLDER=brian-home
LOCAL_SHARE_FOLDER=/mnt/nas
LOCAL_CREDENTIALS_FILE=/home/brian/.cifs-nas

MOUNT_STRING=$(printf '\n//%s/%s %s cifs credentials=%s 0 0\n\n' $NAS_IP $NAS_SHARE_FOLDER $LOCAL_SHARE_FOLDER $LOCAL_CREDENTIALS_FILE)
echo $MOUNT_STRING >> /etc/fstab

#Example output: //192.168.0.12/brian-home /mnt/nas cifs credentials=/home/brian/.cifs-nas 0 0
