#! /bin/sh

# ssh ubuntu@172.16.220.64 -p5190
mkdir test
cd test
curl -OLJ https://raw.githubusercontent.com/Naveen-Prathap/cloud1/main/scheduler.py
python3 scheduler.py