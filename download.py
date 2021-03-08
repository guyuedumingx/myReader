import requests
from html.parser import HTMLParser
from lxml import etree
import json
import re
from book_list import *
from bs4 import BeautifulSoup

class Downloader:

    def __init__(self, rules):
        self.rule_search = rules['ruleSearch']
        self.rule_book_info = rules['ruleBookInfo']
        self.rule_toc = rules['ruleToc']
        self.rule_content = rules['ruleContent']
        self.method = rules['method']
        self.key = "圣墟"
        self.charset = rules['charset']
        self.encoding = rules['charset']
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
            self.encoding = response.encoding
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
                data['book_url'] = self.fix_url(data['book_url'])
                book = Book_List(data)
                book_lists.append(book)
            except:
                continue
        return book_lists
        
    def fix_url(self, book_url):
        if(book_url.find("http") == -1):
            return self.sourceUrl + book_url

    def get_book_info(self, book):
        data = {}
        self.url = book.book_url
        html_text = self.get_html()
        info = etree.HTML(html_text)
        data['author'] = info.xpath(self.rule_book_info['author'])[0]
        data['name'] = info.xpath(self.rule_book_info['name'])[0]
        data['intro'] = info.xpath(self.rule_book_info['intro'])[0]
        data['kind'] = info.xpath(self.rule_book_info['kind'])[0]
        data['cover_url'] = info.xpath(self.rule_book_info['cover_url'])[0]
        data['last_chapter'] = info.xpath(self.rule_book_info['last_chapter'])[0]
        data['toc_url'] = info.xpath(self.rule_book_info['toc_url'])[0]
        toc_info = self.get_toc_info(data['toc_url'])
        data['toc_info'] = toc_info
        book = Book_Info(data) 
        return book
    
    def get_toc_info(self, toc):
        chapter_infos = []
        chapter_list = toc.xpath(self.rule_toc['chapterList'])
        for chapter in chapter_list:
            data = {}
            data['name'] = chapter.xpath(self.rule_toc['chapterName'])[0]
            data['url'] = chapter.xpath(self.rule_toc['chapterUrl'])[0]
            data['url'] = self.fix_url(data['url'])
            chapter_infos.append(data)
        if(self.rule_toc['nextTocUrl'] != ""):
            pass
        return chapter_infos
    
    def get_chapter_info(self, chapter_url):
        self.url = chapter_url
        self.data = {}
        html_text = self.get_html()
        info = etree.HTML(html_text)
        content_html = info.xpath(self.rule_content['content'])[0]
        content = etree.tostring(content_html, pretty_print=True, method='html').decode(self.encoding)
        if(self.rule_content['nextContentUrl'] != ""):
            pass
        return self.decodeHtml(content)

    def decodeHtml(self, input):
        h = HTMLParser()
        s = h.unescape(input)
        return s




with open("rules.json", "r", encoding="utf-8") as f:
    rules = json.loads(f.read())
downloader = Downloader(rules[0])
text = downloader.get_html()
book_list = downloader.get_book_list(text)
book_info = downloader.get_book_info(book_list[0])
chapter_url = book_info.get_chapter_url_by_no(1)
content = downloader.get_chapter_info(chapter_url)
books = []
for book in book_list:
    books.append(book.to_json())

with open("books.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(books))
book_info.save("book_info.json")

