from app.libs.Http import HTTP
from flask import current_app


class YuShuBook:
    """
    模型层 MVC M层
    描述书籍
    """
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        self.total = 0
        self.books = []

    def __fill_single(self, data):
        """
        单本书籍
        :param data:
        :return:
        """
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self, data):
        """
        多本书籍
        :param data:
        :return:
        """
        self.books = data['books']
        self.total = data['total']

    def search_by_isbn(self, isbn):
        """
        isbn 搜索（以后考虑缓存数据问题）
        :param isbn:
        :return:
        """
        url = self.isbn_url.format(isbn)
        result = HTTP.get(url)
        self.__fill_single(result)

    def search_by_keyword(self, keyword, page=1):
        """
        关键字搜索
        :param keyword:
        :param page:
        :return:
        """
        url = self.keyword_url.format(keyword, current_app.config['PER_PAGE'],
                                      self.calculate_start(page))
        result = HTTP.get(url)
        self.__fill_collection(result)

    def calculate_start(self, page):
        """
        计算开始
        :param page:
        :return:
        """
        return (page-1) * current_app.config['PER_PAGE']

    @property
    def first(self):
        """
        返回books的第0号元素
        :return:
        """
        return self.books[0] if self.total >= 1 else None
