from bs4 import BeautifulSoup
import requests

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/80.0.3987.149 Safari/537.36'
headers = {
    'User-Agent': user_agent
}
url = "http://www.ziroom.com/z/s100013-p1/"
#html = requests.get(url).content
import pdb
pdb.set_trace()
urls_old = set()
urls_old.add(url)
html = requests.get(url, headers=headers).content
next_page_urls_soup = BeautifulSoup(html, 'xml', from_encoding='utf-8')
next_page_ret = next_page_urls_soup.find('div', class_='Z_pages')
next_page_urls = next_page_ret.find_all('a', class_='next')
for url in next_page_urls:
    next_page_url = 'http:' + url.get('href')
    if next_page_url not in urls_old:
        urls_old.add(next_page_url)
        print(next_page_url)
#print(next_page_url)