#!/bin/bash

docker run --rm -i -v "$(pwd)":/workdir:rw mikenye/youtube-dl $@

