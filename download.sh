#!/bin/bash

START=10001
END=10005
URL="http://www.fdb.cz/film/obsazeni"

export PYTHONIOENCODING=UTF-8

mkdir -p data

for i in `seq ${START} ${END}`; do
	echo $i
	wget -qO- "${URL}/${i}" | ./dump-fdb.py > data/$i.xml
	sleep 1s
done

