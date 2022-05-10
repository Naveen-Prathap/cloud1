#! /bin/sh

curl -OL $1
python3 worker.py $2 $3 $4 $5
