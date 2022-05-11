import json
import redis


r = redis.Redis(host='172.16.220.64', port=6379, db=0, decode_responses=True)
jobs = [{'template_name': 'template_pokemon',
        'template_url': 'https://raw.githubusercontent.com/Naveen-Prathap/cloud1/main/template_pokemon.py',
        'instances': '3',
        'base_url': 'https://scrapeme.live/shop/'},
        {'template_name': 'template_books' ,
        'template_url': 'https://raw.githubusercontent.com/Naveen-Prathap/cloud1/main/template_books.py',
        'instances': '2',
        'base_url': 'http://books.toscrape.com/'}]
for job in jobs:    
    job = json.dumps(job)
    r.lpush('new_jobs', job)