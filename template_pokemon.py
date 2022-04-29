from bs4 import BeautifulSoup
import urllib.parse as parse


def parse_listing_page(html, url):
    print('Parsing listing page')
    soup = BeautifulSoup(html, 'html.parser')
    
    link_to_listing_page = []
    try:
        link_to_listing_page = soup.find('a', class_ = 'next page-numbers').get('href')
        link_to_listing_page = parse.urljoin(url, link_to_listing_page)
    except:
        pass

    links_with_tags = soup.find_all('a', class_ = 'woocommerce-LoopProduct-link woocommerce-loop-product__link')
    product_links = [link.get('href') for link in links_with_tags]

    dict1 = {}
    dict1['data'] = {}
    dict1['urls'] = {}

    for link in product_links:
        dict1['urls'][link] = 'parse_product_page'
    if link_to_listing_page != []: 
        dict1['urls'][link_to_listing_page] = 'parse_listing_page'
    print('Parsing lisitng page done')
    # print(dict1)
    return dict1


def parse_product_page(html, url):
    print('Parsing product page')
    soup = BeautifulSoup(html, 'html.parser')
    name = soup.find('h1', class_ = 'product_title entry-title').text
    price = soup.find('p', class_ = 'price').text

    dict1 = {}
    dict1['data'] = [[name, price]]
    dict1['urls'] = {}
    print('Parsing product page done')

    return dict1



