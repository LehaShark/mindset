import requests
from bs4 import BeautifulSoup
import csv
from http.client import RemoteDisconnected

TOPICS = ['/regions/central-asia/', '/regions/east-asia/', '/regions/oceania-region/', '/regions/south-asia/', '/regions/southeast-asia/', '/topics/security/', '/topics/politics/', '/topics/diplomacy/', '/topics/economy/', '/topics/society/', '/topics/environment/']
URL = 'https://thediplomat.com/regions/central-asia/'
HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'}
HOST = 'https://thediplomat.com'
FILE = 'thediplomat.csv'

def save_file(items, path):
    with open(path, 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        #writer.writerow(['text', 'title', 'host', 'link', 'owner', 'label'])
        for item in items:
            writer.writerow([item['text'], item['title'], item['host'], item['link'], item['owner'], item['label']])

def get_text_on_page(url):
    html = get_html(url)

    soup = BeautifulSoup(html.text, 'html.parser')
    text = soup.find('section', class_='td-prose').get_text()
    return text


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find('div', class_='td-list-pager')
    page = pagination.find().get_text().replace('Page 1 of ', '')
    return int(page)

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_='td-post')
    name = []
    for item in items:
        link = str(HOST + item.get('href'))
        text = get_text_on_page(link)
        name.append({
            'text': text,
            'title': item.find('h4').get_text().replace(',', ''),
            'host': HOST,
            'link': link,
            'owner': 'mindset',
            'label': '0.930000'
        })
    return name

def parse(url):
    html = get_html(url)
    if html.status_code == 200:
        articles = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count}')
            html = get_html(URL + f'page/{page}/')
            get_content(html.text)
            articles.extend(get_content(html.text))
            #print(articles)
        save_file(articles, FILE)
        print(f'получено {len.articles} статей')
    else:
        print('Error')

if __name__ == '__main__':
    try:
        for topic in TOPICS:
            url = HOST + topic
            parse(URL)
    except RemoteDisconnected:
        pass
