import json

class Book_List:

    def __init__(self, data):
        self.name = data['name']
        self.author = data['author']
        self.book_url = data['book_url']
        self.intro = data['intro']
        self.kind = data['kind']
        self.cover_url = data['cover_url']
    
    def to_json(self):
        return json.dumps(self.__dict__, ensure_ascii=False)


class Book_Info:

    def __init__(self, data):
        self.name = data['name']
        self.author = data['author']
        self.intro = data['intro']
        self.kind = data['kind']
        self.cover_url = data['cover_url']
        self.last_chapter = data['last_chapter']
        self.toc_info = data['toc_info']

    def get_chapter_url_by_no(self, no):
        return self.toc_info[no-1]['url']
    
    def get_chapter_url_by_name(self, book_name):
        for chapter in self.toc_info:
            if(book_name == chapter['name']):
                return chapter['url']
        return ""

    def save(self, file):
        with open(file, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.__dict__, ensure_ascii=False))

    def to_json(self):
        return json.dumps(self.__dict__, ensure_ascii=False)


