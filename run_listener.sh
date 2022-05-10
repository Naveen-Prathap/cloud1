#! /bin/sh

# ssh ubuntu@172.16.220.65 -p5190
mkdir test
cd test
# curl -OL https://github.com/Naveen-Prathap/cloud1/blob/main/del_dir.sh
curl -OL https://github.com/Naveen-Prathap/cloud1/blob/main/run_worker.sh
curl _OL https://github.com/Naveen-Prathap/cloud1/blob/main/listener.py
curl -OL https://github.com/Naveen-Prathap/cloud1/blob/main/worker.py
python3 listener.py $1