import redis
import json


# r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
r = redis.Redis(host='172.16.220.64', port=6379, db=0, decode_responses=True)
while True:
    new_job = r.blpop('new_jobs', timeout=2)
    if new_job:
        new_job1 = json.loads(new_job[1])
        for _ in range(int(new_job1['instances'])):
            r.lpush('jobs_to_schedule', new_job[1])
    while True:
        if r.llen('free_workers') > 0 and r.llen('jobs_to_schedule') > 0:
            worker  = json.loads(r.rpop('free_workers'))
            job = json.loads(r.rpop('jobs_to_schedule'))
            job['worker_id'] = worker['worker_id']
            r.lpush(f'urls{job["template_name"]}', json.dumps({job['base_url'] : 'parse_listing_page'}))
            r.lpush(worker['server_id'], json.dumps(job))
            r.lpush('scheduled_jobs', json.dumps({job['template_name']: worker['worker_id'] }))
        else:
            break

