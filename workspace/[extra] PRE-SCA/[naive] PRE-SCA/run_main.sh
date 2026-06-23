#! /bin/bash

echo "${0} script ${1} run"

for ((i=0; i<${1}; i++)); do
	echo "try : $i "
	python3 ./main.py
	sleep 2
done
