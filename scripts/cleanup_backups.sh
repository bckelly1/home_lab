#!/bin/bash

set -e

backup_dir=$1

echo "found $backup_dir"

# Count files
# If file count > 5 begin cleanup
file_count=$(ls $backup_dir | wc -l)

echo "found $file_count backups"

if [ $file_count -gt 5 ]
then
  echo "trimming backups to latest 5"
else
  echo "no need to trim backups"
fi

latest_5_files=($(ls $backup_dir -t | head -5))

for file in "${latest_5_files[@]}"
do
  :
  echo "Found /home/brian/backups/$file"
done

