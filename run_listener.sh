#! /bin/sh

# ssh ubuntu@172.16.220.65 -p5190
mkdir test
cd test
# curl -OL https://github.com/Naveen-Prathap/cloud1/blob/main/del_dir.sh
curl -OLJ https://raw.githubusercontent.com/Naveen-Prathap/cloud1/main/run_worker.sh
curl -OLJ https://raw.githubusercontent.com/Naveen-Prathap/cloud1/main/listener.py
curl -OLJ https://raw.githubusercontent.com/Naveen-Prathap/cloud1/main/worker.py
python3 listener.py $1