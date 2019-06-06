"""
物理删除：直接将数据从数据库中删除 缺点是有可能误删，互联网分析用户行为
软删除（假删除）：并不是直接删除，而是将其状态改变为删除状态
"""
from flask import current_app
from app.models.base import Base, db
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, desc, func
from sqlalchemy.orm import relationship
from app.spider.yushu_book import YuShuBook
from collections import namedtuple


class Gift(Base):
    """
    launched 用来表示是否赠送出去
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    用来与user模型做关联
    不用这样与book模型关联，因为数据库中没有存书籍数据，数据是直接由API获取的
    直接用isbn = Column(String(15), nullable=False) 表示已关联
    """
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.isbn'))
    launched = Column(Boolean, default=False)

    def is_yourself_gift(self, uid):
        """
        判断是否是自己赠送的礼物，在交易drift时判断
        :param uid:
        :return:
        """
        return True if self.uid == uid else False

    # 对象代表一个礼物，具体内容
    # 类代表礼物这个事物，抽象内容，不是具体的“一个”
    @classmethod
    def recent(cls):
        """
        最近上传内容显示：
        limit(30) 只显示一定数量（30）
        order_by(以时间排序) 按时间倒序(使用desc)排列，最新的排在最前面
        group_by().distinct()去重，同一本书籍的礼物不重复出现（先分组在distinct）
        链式调用(极大的灵活性)  主体：Query 对象  子函数：filter_by、order_by、group_by、limit、distinct
        所有函数都将返回主体Query  链式调用需要触发语句，遇到触发语句将生成一条sql语句，触发语句：all()、first()
        :return:
        """
        recent_gift = Gift.query.filter_by(
            launched=False).group_by(
            Gift.isbn).order_by(
            desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).distinct().all()
        return recent_gift

    @property
    def book(self):
        """
        将最近上传的礼物转变为具体书籍的信息
        property  把方法变成属性
        :return:
        """
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def get_user_gifts(cls, uid):
        """
        查询用户所有的礼物清单（未送出去的礼物）
        :param uid:
        :return:
        """
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(
            desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_list):
        """
        需要一组数量，每本书的想要数量 isbn -- 数量
        使用 mysql 中的 in 查询
        filter和filter_by的不同：filter接收关键表达式，filter_by直接接收参数
        数据保存 db.session
        根据传入的一组isbn,到wish表中计算出某个礼物的Wish心愿数量
        查询结果为  [(1,isbn),(1,isbn)] 可以将结果转变为字典或者对象
        # count_list = [EachGiftWishCount(w[0],w[0]) for w in count_list]  用namedtuple将其转换成字典
        :param isbn_list:
        :return:
        """
        from app.models.wish import Wish
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False,
            Wish.isbn.in_(isbn_list),
            Wish.status == 1).group_by(
            Wish.isbn).all()
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list
