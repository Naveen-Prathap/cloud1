#! /bin/sh

curl curl -v -H "Cache-Control: no-cache" -OLJ $1
python3 worker.py $2 $3 $4 $5
