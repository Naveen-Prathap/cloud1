#! /bin/sh

ssh ubuntu@172.16.220.64 -p5190
mkdir test
cd test
curl -OL https://github.com/Naveen-Prathap/cloud1/blob/main/scheduler.py
python3 scheduler.py