import asyncio
import importlib
import json
from aiohttp import ClientSession
import sys
import redis
import template_pokemon as template

# mod_name = 'template_pokemon'
# path = '10.0.2.2/home/naveen/Documents/new folder'
# sys.path.append(path)
# template = importlib.import_module(mod_name)


async def fetch(url : str, session : ClientSession):
    async with session.get(url) as response:
        x = await response.read()
        return x


async def crawler(r : redis.Redis, session : ClientSession):
    
    while True:
        if r.llen('links_to_crawl') == 0:
            print('Sleeping......')
            await asyncio.sleep(6)
            r.set('urls_flag', '0')
            if r.llen('links_to_crawl') == 0 and r.get('links_to_crawl_flag') == '0':
                print('exiting.....')
                break
        else:
            r.set('urls_flag', '1')
            url = r.lpop('links_to_crawl')  
            url = json.loads(url)
            print(url)
            url1 = list(url.keys())[0]
            fn = list(url.values())[0]
            html = await fetch(url1, session) 
            
            dict1 = getattr(template, fn)(html, url1)
            print('retrieving results')

            for datum in dict1['data']:
                r.lpush('data', json.dumps(datum))
            for url, fn in dict1['urls'].items():
                r.lpush('urls', json.dumps({url:fn}))
            # r.set('urls_flag', '1')
        



async def main(ip):
    async with ClientSession() as session:
        r = redis.Redis(host= ip, port=6379, db=0, decode_responses=True)
        crawlers =  [asyncio.create_task(crawler(r, session)) for _ in range(5)]
        await asyncio.gather(*crawlers)

ip = '172.16.220.64'
asyncio.run(main(ip))
