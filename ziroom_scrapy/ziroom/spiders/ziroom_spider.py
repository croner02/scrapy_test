#-*- encoding:utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
import requests
import time
import math
from ziroom.items import ZiroomItem
from PIL import Image
from aip import AipOcr
from scrapy.utils.project import get_project_settings
import random
from ziroom.spiders.anonymous_proxy import AnonyProxy

APP_ID = '19383742'
API_KEY = 'yVlspwRqI1giqXTGX051hofL'
SECRET_KEY = 'ZChUT1fZLWdRpVyGoMwwA492TqViYEnG'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


class ZiroomSpider(scrapy.Spider):
    name = 'ziroom'
    allowed_domains = ['ziroom.com']
    start_urls = (
        'http://www.ziroom.com/z/s100013-p1/',
    )
    custom_settings = {
        'LOG_LEVEL': 'DEBUG',
        'LOG_FILE': '5688_log_%s.txt' % time.time(),
        "DEFAULT_REQUEST_HEADERS": {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        }
    }

    def parse(self, response):
        data = {}
        html_body = response.body
        soup = BeautifulSoup(html_body, 'xml', from_encoding='utf-8')
        room_rets = soup.find_all('div', class_='info-box')
        for ret in room_rets:
            data['title'] = ret.find('a').get_text()
            data['href'] = ret.find('a').get('href')
            data['desc'] = ret.find('div', class_='desc').find('div').get_text()
            data['location'] = ret.find('div', class_='location').get_text().strip()
            data['price'] = self._get_price(ret)
            item = ZiroomItem(title=data['title'], href=data['href'], desc=data['desc'],
                              location=data['location'], price=data['price'])
            yield item
        try:
            next_page_urls_soup = BeautifulSoup(html_body, 'xml', from_encoding='utf-8')
            next_page_ret = next_page_urls_soup.find('div', class_='Z_pages')
            next_page_url = 'http:' + next_page_ret.find('a', class_='next').get('href')
            if next_page_url not in self.start_urls:
                time.sleep(10)
                print('url:' + next_page_url)
                yield scrapy.Request(next_page_url, callback=self.parse)
        except TimeoutError as e:
            return e
        except AssertionError as e:
            return e

    def _get_price_img_urls(self, soup):
        price_pos = []
        price_url = set()
        links = soup.find_all('span', class_='num')
        for link in links:
            img_url = link.get('style').split(';')[0].split('(')[-1][0:-1]
            pos = link.get('style').split(':')[-1].strip()[1:-2]
            price_url.add(img_url)
            price_pos.append(pos)
        if len(price_url) == 1:
            return price_url.pop(), price_pos

    def _img_change(self, img):
        im = Image.open(img)
        w, h = im.size
        p = Image.new('RGBA', im.size, (255, 255, 255))
        p.paste(im, (0, 0, w, h), im)
        p.save(img)

    def _pos(self, pos):
        return math.floor(float(pos)/19.3)

    def _get_price(self, soup):
        price = []
        url, pos = self._get_price_img_urls(soup)
        img_ret = requests.get('http:' + url)
        with open('tmp.png', 'wb') as f:
            f.write(img_ret.content)
        self._img_change('tmp.png')
        with open('tmp.png', 'rb') as f:
            img = f.read()
            time.sleep(3)
            res = client.basicGeneral(img)['words_result'][0]['words']
        for v_pos in pos:
            price_rmb = res[self._pos(v_pos)]
            price.append(price_rmb)
        return ''.join(price)


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(ZiroomSpider)
    process.start()
