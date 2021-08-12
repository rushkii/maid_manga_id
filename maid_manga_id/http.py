from .utils import to_async
from bs4 import BeautifulSoup as bsoup
import requests, lxml, re

BASE = "https://maid.my.id"

@to_async
def scrape(path:str):
    if bool(re.match(r'((http|https):\/\/)?(www.)?maid.my.id/(.*)', path)):
        url = path
    elif not path.startswith('/'):
        url = f'{BASE}/{path}'
    else:
        url = BASE+path
    response =  requests.get(url)
    soup =  bsoup(response.text, 'lxml')
    return soup

@to_async
def api(**kwargs):
    response =  requests.post(
        f'{BASE}/wp-admin/admin-ajax.php',
        **kwargs
    )
    soup =  bsoup(response.text, 'lxml')
    return soup

@to_async
def new(method, url, **kwargs):
    return requests.request(method, url, **kwargs)