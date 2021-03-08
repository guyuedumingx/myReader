import requests
from lxml import etree
import json
import re
from book_list import *
from bs4 import BeautifulSoup

class Downloader:

    def __init__(self, rules):
        self.rule_search = rules['ruleSearch']
        self.rule_book_info = rules['ruleBookInfo']
        self.method = rules['method']
        self.key = "圣墟"
        self.charset = rules['charset']
        self.url = rules['searchUrl']
        self.sourceUrl = rules['bookSourceUrl']
        self.data = {}
        self.headers = {'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'}
        self.replace_key()
        self.split_params()

    def replace_key(self):
        self.url = re.sub("\{\{\w+\}\}", self.encode_data(self.key), self.url)


    def split_params(self):
        if("GET" == self.method):
            url, params = self.url.split("?")
            self.url = url + "?"
            params = params.split("&")
            for para in params:
                key, value = para.split("=")
                self.data[key] = value

    def encode_data(self, key):
        if(self.charset != ""):
            info = str(key.encode(self.charset))[2:-1]
            return info.replace(r'\x',r'%')
        return key


    def get_html(self):
        if(self.method == "POST"):
            response = requests.post(self.url,data=self.data)
            response.encoding = response.apparent_encoding
            return response.text
        else:
            response = requests.get(self.url, headers=self.headers, params=self.data)
            response.encoding = response.apparent_encoding
            return response.text


    def get_book_list(self, text):
        book_lists = []
        data = {}
        html = etree.HTML(text)
        books = html.xpath(self.rule_search['bookList'])
        for book_list in books:
            try:
                data['name'] = book_list.xpath(self.rule_search['name'])[0]
                data['author'] = book_list.xpath(self.rule_search['author'])[0]
                data['book_url'] = book_list.xpath(self.rule_search['bookUrl'])[0]
                data['intro'] = book_list.xpath(self.rule_search['intro'])[0]
                data['kind'] = book_list.xpath(self.rule_search['kind'])[0]
                data['cover_url'] = book_list.xpath(self.rule_search['coverUrl'])[0]
                data['book_url'] = self.fix_book_url(data['book_url'])
                book = Book_List(data)
                book_lists.append(book)
            except:
                continue
        return book_lists
        
    def fix_book_url(self, book_url):
        if(book_url.find("http") == -1):
            return self.sourceUrl + book_url

    def get_book_info(self, book):
        self.data = {}
        self.url = book.book_url
        html_text = self.get_html()
        html = etree.HTML(html_text)
        books = html.xpath(self.rule_search['bookList'])


with open("rules.json", "r", encoding="utf-8") as f:
    rules = json.loads(f.read())
downloader = Downloader(rules[0])
text = downloader.get_html()
book_list = downloader.get_book_list(text)
print(book_list)

