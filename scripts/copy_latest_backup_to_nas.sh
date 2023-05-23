#!/bin/bash

set -e

backups_directory=/home/brian/backups
nas_directory=/mnt/nas/Files/OS\ Backups/Home\ assistant/

# Find the latest file in directory
file_name=$(ls -Art $backups_directory | grep home_lab_backup | tail -n 1)

full_filename_path=$backups_directory/$file_name

echo "Copying $full_filename_path to $nas_directory"
cp $full_filename_path "$nas_directory"

