from .book import BookViewModel


class MyWishes:
    """
    心愿处理
    """
    def __init__(self, gifts_of_mine, wish_count_list):
        self.gifts = []
        self.__gifts_of_mine = gifts_of_mine
        self.__wish_count_list = wish_count_list
        self.gifts = self.__parse()

    def __parse(self):
        """
        用临时变量存放处理后的数据
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
