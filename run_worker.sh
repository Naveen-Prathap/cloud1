#! /bin/sh
mkdir worker$4
cd worker$4
curl -OL $1
curl -OL https://github.com/Naveen-Prathap/cloud1/blob/main/worker.py
python3 worker.py $2 $3 $4 $5
