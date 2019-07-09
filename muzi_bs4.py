
import os
import requests
from bs4 import BeautifulSoup
import time
import random
import socket
import http.client

user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]

proxy_list = [
    {"http": "120.234.63.196:3128"},
    {"http": "120.210.219.105:80"},
    {"http": "120.210.219.104:80"},
    {"http": "39.137.107.98:80"},
    {"http": "182.92.105.136:3128"},
    {"http": "111.206.6.101:80"},
    {"http": "121.8.98.197:80"},
    {"http": "218.60.8.83:3129"},
    {"http": "60.13.42.24:9999"},
    {"http": "47.99.80.48:80"},
    {"http": "1.65.215.95:8080"},
    {"http": "111.226.211.63:8118"},
    {"http": "117.191.11.113:8080"},
    {"http": "60.13.42.213:9999"},
    {"http": "150.109.51.194:8118"},
    {"http": "119.180.139.156:8060"},
    {"http": "27.188.64.70:8060"},
    {"http": "183.129.207.89:11056"},

]
PROXY=random.choice(proxy_list)
print(PROXY)
US = random.choice(user_agent_list)
print(US)
class mzitu():
    def request(self, url):

        header = {
            #"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            #"Accept-Encoding": "gzip, deflate",
            #"Accept-Language": "zh-CN,zh;q=0.9",
            #"Connection": "keep-alive",
            "User-Agent": US,
            "Referer": "https://www.mzitu.com/tag/tufeiyuanai/"

        }
        timeout = random.choice(range(80, 180))
        try:
            time.sleep(1)
            content = requests.get(url, headers=header, proxies=PROXY, timeout=timeout)
            #content = requests.get(url, headers=header, timeout=timeout)
            content.encoding = 'utf-8'
        except socket.timeout as e:
            print('3:', e)
            time.sleep(random.choice(range(10,30)))
        except socket.error as e:
            print('4:',e)
            time.sleep(random.choice(range(20,60)))
        except http.client.BadStatusLine as e:
            print('5:', e)
            time.sleep(random.choice(range(30,80)))
        except http.client.IncompleteRead as e:
            print('6:',e)
            time.sleep(random.choice(range(10, 40)))

        #except Exception as e:
        #    #print(e)
        #    exit(e)
        else:
            return content

    def html(self, href):
        html = self.request(href)
        max_span = BeautifulSoup(html.text, 'lxml').find('div', class_='pagenavi').find_all('span')[-2].get_text()
        for page in range(1, int(max_span)+1):
            page_url = href+ '/'+ str(page)
            self.img(page_url)

    def img(self,page_url):
        img_html = self.request(page_url)
        img_url = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
        self.save(img_url)

    def save(self,img_url):
        name = img_url[-9:-4]
        name = img_url.split('/')[-1]
        img = self.request(img_url)

        with open(name, 'wb') as f:
            f.write(img.content)

    def mkdir(self, path):
        path = path.strip()
        isExists = os.path.exists(os.path.join('d:\mzitu2', path))
        if not isExists:
            os.mkdir(os.path.join('d:\mzitu2', path))
            os.chdir(os.path.join('d:\mzitu2', path))
            return True
        else:
            print(path, 'file is exists')
            return False

    def all_url(self, url):
        html = self.request(url)
        #from pdb import set_trace;set_trace()
        all_a = BeautifulSoup(html.text, 'lxml').find('div', class_='postlist').find_all('a')
        for a in all_a:
            title = a.get_text()
            path = str(title).replace("?", ' ')
            self.mkdir(path)
            href = a['href']
            self.html(href)


def main():
    Mzitu = mzitu()  ##实例化
    Mzitu.all_url('https://www.mzitu.com/hot/')  ##给函数all_url传入参数

main()
