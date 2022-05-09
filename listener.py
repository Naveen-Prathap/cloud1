import redis
import json
import sys
from getmac import get_mac_address
import subprocess
import os


class Listener:
    def __init__(self, redis_ip:str, workers=5) -> None:
        self.redis_ip = redis_ip
        self.r = redis.Redis(host=redis_ip, port=6379, db=0, decode_responses=True)
        self.mac = get_mac_address()
        workers=[]
        for i in range(1,6):
            workers.append({'server_id':self.mac, 'worker_id': f'{self.mac} {i}'})
        self.r.lpush('free_workers', *workers)
        self.path = f'{os.getcwd()}/run_worker.sh'
        subprocess.run['chmod', '+x', self.path]

    def listen(self) -> None:
        while True:
            job = self.r.brpop(self.mac, timeout=2)
            if job:
                job = json.loads(job)
                subprocess.Popen([self.path, job['template_url'], self.redis_ip, job['template_name'], job['worker_id'], self.mac])


redis_ip = sys.argv[1]
listener = Listener(redis_ip)
listener.listen()
