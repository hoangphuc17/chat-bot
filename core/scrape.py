import urllib.request
from urllib.parse import urlparse
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.Phuc
NEWS = db.NEWS


def crawler(chatbot, url, category):
    htmltext = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(htmltext, 'html.parser')
    links = soup.findAll('a')

    # g_data = soup.findAll('div', {'class': 'box_vertical pkg'})
    # for item in g_data:
    #     print(item)

    list_item_url = []
    list_image_url = []
    list_title = []
    list_subtitle = []

    module_thumb = soup.findAll('div', {'class': 'module-thumb'})
    for item in module_thumb:
        a = item.contents[1]  # lấy ra thẻ a
        item_url = a.get('href')  # lấy ra item_url
        list_item_url.append(item_url)

        img = a.contents[0]  # lấy ra thẻ img
        image_url = img.get('data-src')  # lấy ra image_url
        list_image_url.append(image_url)

    info_vertical_news = soup.findAll('div', {'class': 'info_vertical_news'})
    for item in info_vertical_news:
        title = item.find('h2').contents[0].text
        title = title.replace('\n', '')
        list_title.append(title)
        # print('Title:', title)

        subtitle = item.find('div', {'class': 'sapo_news'}).contents[0]
        list_subtitle.append(subtitle)
        # print('Subtitle:', subtitle)

    # print(list_image_url)
    # print(list_item_url)
    # print(list_title)
    # print(list_subtitle)

    A = zip(list_image_url, list_item_url, list_subtitle, list_title)
    for item in A:
        new_news = {
            'chatbot': chatbot,
            'category': category,
            'image_url': item[0],
            'item_url': item[1],
            'subtitle': item[2],
            'title': item[3]
        }
        NEWS.insert_one(new_news)


def delete_old_news(chatbot, category):
    NEWS.delete_many({'chatbot': chatbot, 'category': category})


def scrape(chatbot, category, url):
    delete_old_news(chatbot, category)
    crawler(chatbot, url, category)


scrape('saostar', 'giai tri', 'https://saostar.vn/giai-tri/')
scrape('saostar', 'am nhac', 'https://saostar.vn/am-nhac/')
