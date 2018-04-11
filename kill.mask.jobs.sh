#!/bin/bash

for job in `ps -f | awk '$9 ~ /mask/ {print $2}'`; do kill -9 $job; done

