from urllib import request
from bs4 import BeautifulSoup
import urllib.parse as parse
import requests
from aiohttp import ClientSession


def parse_listing_page(html, url):
    print('Parsing listing page')
    soup = BeautifulSoup(html, 'html.parser')

    # links_to_listing_pages = soup.find('ul', class_ = 'nav nav-list').find_all('a')
    # links_to_listing_pages = [link.get('href') for link in links_to_listing_pages]
    # links_to_listing_pages = [parse.urljoin(url, link) for link in links_to_listing_pages]
    link_to_listing_page = []
    try:
        link_to_listing_page = soup.find('li', class_ = 'next').find('a').get('href')
        link_to_listing_page = parse.urljoin(url, link_to_listing_page)
    except:
        pass

    product_links = soup.find('section').find_all('div', class_='image_container')
    product_links = [parse.urljoin(url, link.find('a').get('href')) for link in product_links]

    dict1 = {}
    dict1['data'] = {}
    dict1['urls'] = {}

    for link in product_links:
        dict1['urls'][link] = 'parse_product_page'
    if link_to_listing_page != []:
        dict1['urls'][link_to_listing_page] = 'parse_listing_page'

    return dict1


def parse_product_page(html, url):
    print('Parsing product page')
    soup = BeautifulSoup(html, 'html.parser')
    name = soup.find('h1').text
    price = soup.find('p', class_ = 'price_color').text
    catagory = soup.find('ul', class_ = 'breadcrumb').find_all('li')[2].text.strip()
    stock = soup.find('p', class_= 'instock availability').text.strip()

    dict1 = {}
    dict1['data'] = [[name, price, catagory, stock]]
    dict1['urls'] = {}

    return dict1

# For Debugging
# async def fetch(url, session):
#     async with session.get(url) as response:
#         x = await response.read()
#         y = response.url
#         return (x, y)


# async def main():
#     with ClientSession() as session:
#         (html, url) = fetch()



# if __name__ == '__main__':
#     parse_listing_page(requests.get('http://books.toscrape.com/'))
