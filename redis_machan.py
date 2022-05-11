import redis

r = redis.Redis(host='172.16.220.64', port=6379, db=0, decode_responses=True)
while True:
    for key in r.keys():
        try:
            print(f'{key} : {r.llen(key)}')
        except:
            pass