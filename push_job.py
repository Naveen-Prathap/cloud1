import json
import redis


r = redis.Redis(host='172.16.220.64', port=6379, db=0, decode_responses=True)
job = {'template_name': 'template_pokemon',
        'template_url': 'https://github.com/Naveen-Prathap/cloud1/blob/main/template_pokemon.py',
        'instances': '3',
        'first_url': 'https://scrapeme.live/shop/'}
        # {'template_name': 'template_books' ,
        # 'template_url': 'https://github.com/Naveen-Prathap/cloud1/blob/main/template_books.py',
        # 'instances': '3',
        # 'first_url': 'http://books.toscrape.com/'}]
job = json.dumps(job)
r.lpush('new_jobs', job)