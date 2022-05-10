import redis
import json


r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
while True:
    new_job = r.blpop('new_jobs', timeout=2)
    if new_job:
        new_job1 = json.loads(new_job)
        for _ in range(new_job1['instances']):
            r.lpush('jobs_to_schedule', new_job)
    while True:
        if r.llen('free_workers') > 0 and r.llen('jobs_to_schedule') > 0:
            worker  = json.loads(r.rpop('free_workers'))
            job = json.loads(r.rpop('jobs_to_schedule'))
            job['worker_id'] = worker['worker_id']
            r.lpush(f'urls{job["template_name"]}', job['base_url'])
            r.lpush(worker['server_id'], json.dumps(job))
            r.lpush('scheduled_jobs', json.dumps({job['id']: worker['worker_id'] }))
        else:
            break

