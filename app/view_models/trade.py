from app.view_models.book import BookViewModel


class TradeInfo:
    def __init__(self, goods):
        self.total = 0
        self.trades = []
        self.__parse(goods)

    def __parse(self, goods):
        """
        多个数据信息的转换
        :param goods:
        :return:
        """
        self.total = len(goods)
        self.trades = [self.__map_to_trade(single) for single in goods]

    def __map_to_trade(self, single):
        """
        单个数据信息的转化
        将数据的格式转换为需要展示的内容格式
        strftime()将时间戳转化为日期格式
        :param single:
        :return:
        """
        if single.create_datetime:
            time = single.create_datetime.strftime('%Y-%m-%d')
        else:
            time = "未知"
        return dict(
            user_name=single.user.nickname,
            time=time,
            id=single.id
        )

# Gift or Wish   -->  MyTrades 是 Gift 和 Wish 的基类


class MyTrades:
    def __init__(self, trades_of_mine, trade_count_list):
        self.trades = []

        self.__trades_of_mine = trades_of_mine
        self.__trade_count_list = trade_count_list

        self.trades = self.__parse()

    def __parse(self):
        temp_trades = []
        for trade in self.__trades_of_mine:
            my_trade = self.__matching(trade)
            temp_trades.append(my_trade)
        return temp_trades

    def __matching(self, trade):
        count = 0
        for trade_count in self.__trade_count_list:
            if trade.isbn == trade_count['isbn']:
                count = trade_count['count']
        r = {
            'wishes_count': count,
            'book': BookViewModel(trade.book),
            'id': trade.id,
        }
        return r
