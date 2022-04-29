import csv
import asyncio
import json
import redis
import time


def serve(r : redis.Redis):
    visited_links = []
    while True:
        if r.llen('urls') == 0:
            print('Sleeping......')
            time.sleep(4)
            r.set('links_to_crawl_flag', '0')
            if r.llen('urls') == 0 and r.get('urls_flag') == '0':
                print('exiting.....')
                break
        else:
            r.set('links_to_crawl_flag', '1') 
            url = r.lpop('urls')
            url1 = json.loads(url)
            print(url1)
            key = list(url1.keys())[0]
            if key not in visited_links:
                r.lpush('links_to_crawl', url)
                print('Adding url to crawl')
                visited_links.append(key)
            # r.set('links_to_crawl_flag', '0')


def main(url : str, path : str, ip : str):
    r = redis.Redis(host= ip, port=6379, db=0, decode_responses=True)
    r.flushall()
    r.lpush('links_to_crawl', json.dumps({url : 'parse_listing_page'}))
    serve(r)

    with open(path, 'a') as file1:
        writer = csv.writer(file1)
        data = r.lrange('data', 0, -1)
        for datum in data:
            writer.writerow(json.loads(datum))


url = 'https://scrapeme.live/shop/'
# path = '/home/naveen/Documents/with_redis/pokemon.csv'
path = 'pokemon.csv'
data_required = ['Name', 'Price']


with open(path, 'w') as file1:
    writer = csv.writer(file1)
    writer.writerow(data_required)
    
ip = '172.16.220.64'
main(url, path, ip)
