import redis
import json
import csv
from time import sleep


def write_to_csv(r:redis.Redis, finished_job:dict)-> None:
    with open(f"{finished_job['template_name']}data.csv", 'w') as file1:
        writer = csv.writer(file1)
        data = r.lrange(f"data{finished_job['template_name']}", 0, -1)
        for datum in data:
            writer.writerow(json.loads(datum))


def queue_new_jobs(r: redis.Redis)-> None:
    new_job = r.blpop('new_jobs', timeout=2)
    if new_job:
        new_job1 = json.loads(new_job[1])
        r.sadd('all_jobs', new_job[1])
        if not r.sismember(f"visited{new_job1['template_name']}", new_job1['base_url']):
                r.lpush(f'urls{new_job1["template_name"]}', json.dumps({new_job1['base_url'] : 'parse_listing_page'}))
        for _ in range(int(new_job1['instances'])):
            r.lpush('jobs_to_schedule', new_job[1])


def schedule_job(r:redis.Redis)->None: 
    job = json.loads(r.rpop('jobs_to_schedule'))
    if not r.sismember('finished_jobs', json.dumps({'template_name':job['template_name']})):
        worker  = json.loads(r.rpop('free_workers'))
        job['worker_id'] = worker['worker_id']
        r.lpush(worker['server_id'], json.dumps(job))
        r.sadd('scheduled_jobs', json.dumps({'template_name': job['template_name'], 'worker_id': worker['worker_id']}))


def write_data(r:redis.Redis, finished_jobs:list)->None:
    for job in finished_jobs:
        if not r.sismember('data_written', job):
            job = json.loads(job)
            write_to_csv(r, job)
            r.sadd('data_written', json.dumps(job))


def monitor_workers(r:redis.Redis, finished_jobs:list)->None:
    live_jobs = r.smembers('scheduled_jobs')
    live_jobs = [json.loads(job) for job in live_jobs]
    for job in live_jobs:
        if not r.get(f"hb{job['worker_id']}"):
            r.srem('scheduled_jobs', json.dumps(job))
            if not r.sismember('finished_jobs', job['template_name']):
                all_jobs = r.smembers('all_jobs')
                for job1 in all_jobs:
                    job1 = json.loads(job1)
                    if job['template_name'] == job1['template_name']:
                        r.lpush('jobs_to_schedule', json.dumps(job1))


def main(r: redis.Redis)-> None:    
    flag = 0
    while True:
        queue_new_jobs(r)
        while True:
            if r.llen('free_workers') > 0 and r.llen('jobs_to_schedule') > 0:
                schedule_job(r)
            else:
                break
        finished_jobs = r.smembers('finished_jobs')
        write_data(r, finished_jobs)
        if flag == 0:
            sleep(5)
            flag = 1
        monitor_workers(r, finished_jobs)
        
        
# r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
r = redis.Redis(host='172.16.220.64', port=6379, db=0, decode_responses=True)
main(r)
