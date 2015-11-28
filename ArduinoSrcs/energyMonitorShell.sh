#!/bin/bash

timestamp() {
  date
}

cd /home/ubuntu/Documents/LCDDisplay

until python analog.py; do
	echo "analog.py failed with exist code $?. Restarting..." >&2
	echo "analog.py failed with exit code $? at " >> logs/crashdump.txt
	timestamp >> logs/crashdump.txt
	sleep 1
done
