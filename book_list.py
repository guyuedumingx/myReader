class Book_List:

    def __init__(self, data):
        self.name = data['name']
        self.author = data['author']
        self.book_url = data['book_url']
        self.intro = data['intro']
        self.kind = data['kind']
        self.cover_url = data['cover_url']

class Book_Info:

    def __init__(self, data):
        self.name = data['name']
        self.author = data['author']
        self.intro = data['intro']
        self.kind = data['kind']
        self.cover_url = data['cover_url']
        self.toc_url = data['toc_url']
        self.last_chapter = data['last_chapter']


