#-*- encoding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import urllib3
import json
import time
import math

urllib3.disable_warnings()


class AnonyProxy():

    def __init__(self):
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                     'Chrome/80.0.3987.149 Safari/537.36'
        self.headers = {
            'User-Agent': user_agent
        }
        proxy_html = "https://www.xicidaili.com/nn/"
        html = requests.get(proxy_html, headers=self.headers)
        self.soup = BeautifulSoup(html.content, 'lxml', from_encoding='utf-8')

    def parse_html(self):
        ip_list = []
        ip_dict = dict()
        proxys_ret = self.soup.find_all('tr', class_='odd')
        for proxy_ret in proxys_ret:
            if proxy_ret.find_all('td')[6]('div', class_='bar_inner fast'):
                if proxy_ret.find_all('td')[5].text == "HTTP":
                    ip = proxy_ret.find_all('td')[1].text
                    port = proxy_ret.find_all('td')[2].text
                    protocol = proxy_ret.find_all('td')[5].text
                    proxy = protocol.lower() + "://" + ip + ":" + port
                    yield proxy
            else:
                continue

    def check_proxy(self):
        ip_list = []
        test_url = "http://www.ziroom.com/z/s100013-p1/"

        for proxy in self.parse_html():
            try:
                proxies = {"http": proxy}
                ret = requests.get(test_url, headers=self.headers, proxies=proxies, verify=False)
                if ret.status_code == 200:
                    print('proxy is ok')
                    ip_list.append(proxy)
                else:
                    print('proxy is not ok')
            except requests.exceptions.ProxyError as e:
                print('proxy is not ok')
                continue
        return ip_list

    def slave_proxy(self):
        ip_list = self.check_proxy()
        for i in ip_list:
            with open('ip_list.txt', 'w') as f:
                f.write(i)

if __name__ == "__main__":
    test = AnonyProxy()
    test.check_proxy()