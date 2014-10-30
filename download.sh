#!/bin/bash

START=11000
END=20000
URL="http://www.fdb.cz/film/obsazeni"

export PYTHONIOENCODING=UTF-8

mkdir -p data

for i in `seq ${START} ${END}`; do
	echo $i
	wget -qO- "${URL}/${i}" | ./dump-fdb.py > data/$i.xml
	sleep 0.5s
done

