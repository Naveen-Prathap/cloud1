# import csv
import asyncio
from asyncio import subprocess
import json
import redis
from aiohttp import ClientSession
import importlib
import sys
import os
# import template_pokemon as template

mod_name = sys.argv[2]
path = os.getcwd()
sys.path.append(path)
template = importlib.import_module(mod_name)


async def fetch(url : str, session : ClientSession):
    async with session.get(url) as response:
        x = await response.read()
        return x


async def crawler(r : redis.Redis, session : ClientSession):
    template_name = sys.argv[2]
    while True:
        if r.llen('urls'+template_name) == 0:
            print('Sleeping......')
            r.set('urls_flag'+template_name, '0')
            await asyncio.sleep(5)
            if r.llen('urls'+template_name) == 0 and r.get('urls_flag'+template_name) == '0':
                print('exiting.....')
                break
        else:
            # import pdb; pdb.set_trace()
            r.set('urls_flag'+template_name, '1')
            url = r.lpop('urls'+template_name)  
            url = json.loads(url)
            print(url)
            url1 = list(url.keys())[0]
            fn = list(url.values())[0]
            if r.sismember('visited'+template_name, url1):
                continue
            await asyncio.sleep(0.2)
            html = await fetch(url1, session) 
            r.incr(f'{template_name}_pulse')
            print('retrieving results')
            dict1 = getattr(template, fn)(html, url1)
            r.sadd('visited'+template_name, url1)

            print("Storing data and urls")
            for datum in dict1['data']:
                r.lpush('data'+template_name, json.dumps(datum))
            for url, fn in dict1['urls'].items():
                if not r.sismember('visited'+template_name, url):
                    r.lpush('urls'+template_name, json.dumps({url:fn}))
        

async def main(r):
    async with ClientSession() as session:
        crawlers =  [asyncio.create_task(crawler(r, session)) for _ in range(3)]
        await asyncio.gather(*crawlers)
        
        dict1 = json.dumps({'server_id' : sys.argv[3], 'worker_id' : f'{sys.argv[3]} {sys.argv[4]}'})
        dict2 = json.dumps({'template_name' : sys.argv[2]})
        r.lpush('free_workers', dict1)
        r.sadd('finished_jobs', dict2)


redis_ip = sys.argv[1]
r = redis.Redis(host= redis_ip, port=6379, db=0, decode_responses=True)
asyncio.run(main(r))


# path = path.split('/')[:-1]
# path = ('/').join(path)
# path += 'del_dir.sh'
# subprocess.run['chmod', '+x', path]
# subprocess.Popen([path, sys.argv[3]])
