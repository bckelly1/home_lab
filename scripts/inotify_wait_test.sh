#!/bin/bash
while true; do

# Can handle events such as modify,create,delete
inotifywait -m -e create -r /home/brian/nas_test/ | gawk '{print $1$3; fflush()}' | xargs -L 1 echo "Found file $@" && cp $@ /home/brian/consume_dir
done
