# 重构前 _BookViewModel：
class _BookViewModel:
    # 面向对象中类要描述特征（类变量、实例变量）以及其行为（方法）
    @classmethod
    def package_single(cls, data, keyword):
        """
        处理单本书籍数据情况，是多本的特例
        解析原始数据data
        :param data:
        :param keyword:
        :return:
        """
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword,
        }
        if data:
            returned['total'] = 1
            returned['books'] = [cls.__cut_book_data(data)]
        return returned

    @classmethod
    def package_collection(cls, data, keyword):
        """
        处理多本书籍数据的情况，返回格式
        :param data:
        :param keyword:
        :return:
        """
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword,
        }
        if data:
            returned['total'] = data['total']
            returned['books'] = [cls.__cut_book_data(book) for book in data['books']]
        return returned

    @classmethod
    def __cut_book_data(self, data):
        """
        裁剪展示的数据内容
        处理数据，将原始数据进行调整:用、将作者名连接;若pages或summary为空时用''表示
        :param data:
        :return:
        """
        book = {
            'title': data['title'],
            'author': '、'.join(data['author']),
            'publisher': data['publisher'],
            'pages': data['pages'] or '',
            'price': data['price'],
            'summary': data['summary'] or '',
            'image': data['image'],
        }
        return book


# 重构后


class BookViewModel:
    def __init__(self, book):
        """
        单本书籍的操作
        原始数据存在于yushu_book中
        :param yushu_book:
        """
        self.title = book['title']
        self.publisher = book['publisher']
        self.author = '、'.join(book['author'])
        self.image = book['image']
        self.price = book['price']
        self.summary = book['summary']
        self.pages = book['pages']
        self.isbn = book['isbn']
        self.pubdate = book['pubdate']
        self.binding = book['binding']

    @property
    def intro(self):
        """
        处理搜索结果中 书籍的作者/出版社/价格
        加上@property装饰器，使其能够像属性一样使用
        :return:
        """
        intros = filter(lambda x: True if x else False,
                        [self.author, self.publisher, self.price])
        return '/'.join(intros)


class BookCollection:
    """
    多本书籍的集合处理
    """
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, yushu_book, keyword):
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in yushu_book.books]
