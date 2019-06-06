from .book import BookViewModel
from collections import namedtuple


# MyGift = namedtuple('MyGift', ['id', 'book', 'wishes_count'])


class MyGifts:
    def __init__(self, gifts_of_mine, wish_count_list):
        self.gifts = []
        self.__gifts_of_mine = gifts_of_mine
        self.__wish_count_list = wish_count_list
        self.gifts = self.__parse()

    def __parse(self):
        """
        解析过程,两个列表的解析需要双重循环，将另一重循环写到__matching()函数中
        不建议直接在__parse中将my_gift添加进gifts中，不在一个函数中直接修改（不可以修改但是可以读取）实例的属性
        :return:
        """
        temp_gifts = []
        for gift in self.__gifts_of_mine:
            my_gift = self.__matching(gift)
            temp_gifts.append(my_gift)
        return temp_gifts

    def __matching(self, gift):
        """
        第二重循环，将匹配到的结果count返回回去
        还是不使用namedtuple，不容易序列化，使用字典去实现
        :param gift:
        :return:
        """
        count = 0
        for wish_count in self.__wish_count_list:
            if gift.isbn == wish_count['isbn']:
                count = wish_count['count']
        r = {
            'wishes_count': count,
            'book': BookViewModel(gift.book),
            'id': gift.id,
        }
        return r
        # my_gift = MyGift(gift.id, BookViewModel(gift.book), count)
        # return my_gift


