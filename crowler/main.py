import requests
from bs4 import BeautifulSoup
import csv
from http.client import RemoteDisconnected

HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'}
HOST = 'https://www.bbc.com'
TOPICS = ['/news/world/us_and_canada', '/news/world/middle_east', '/news/world/latin_america', '/news/world/europe', '/news/world/australia', '/news/world/asia', '/news/world/africa', '/news/world']
    # ['/regions/oceania-region/', '/regions/central-asia/', '/regions/east-asia/', '/regions/south-asia/', '/regions/southeast-asia/', '/topics/security/', '/topics/politics/', '/topics/diplomacy/', '/topics/economy/', '/topics/society/', '/topics/environment/']
# URL = 'https://thediplomat.com/regions/central-asia/'
FILE = 'bbc.csv'

def save_file(items, path):
    with open(path, 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        # writer.writerow(['text', 'title', 'host', 'link', 'owner', 'label'])
        for item in items:
            writer.writerow([item['text'], item['title'], item['host'], item['link'], item['owner'], item['label']])

def get_text_on_page(url):
    html = get_html(url)

    soup = BeautifulSoup(html.text, 'html.parser')
    try:
        text = soup.find('article', class_='e1nh2i2l6').get_text(strip=True).replace(',','').replace('--', '')
    except:
        text = None
        print('text is none')
    return text


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    # pagination = soup.find('div', class_='field__item').get_text()
    # page = pagination.find().get_text()#.replace('Page 1 of ', '')
    return 1#int(pagination)

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('li', class_='lx-stream__post-container')
    # print(len(items))
    name = []
    for item in items:
        try:
            href = item.find('a', class_='qa-heading-link').get('href')
        except:
            continue
        link = str(HOST + href)
        print(link)
        text = get_text_on_page(link)
        if text == None:
            continue
        else:
            name.append({
                'text': text,
                'title': item.find('a', class_='qa-heading-link').get_text(strip=True).replace(',', ''),
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
            html = get_html(url, params=f'page={page}')
            # html = get_html(url + f'page/{page}/')
            # get_content(html.text)
            articles.extend(get_content(html.text))
        save_file(articles, FILE)
        print(f'получено {len(articles)} статей')
    else:
        print('Error')

if __name__ == '__main__':
    try:
        for topic in TOPICS:
            url = HOST + topic
            parse(url)
    except RemoteDisconnected:
        pass
