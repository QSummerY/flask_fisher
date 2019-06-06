from app.models.base import Base, db
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, desc, func
from sqlalchemy.orm import relationship
from app.spider.yushu_book import YuShuBook


class Wish(Base):
    """
    心愿模型，与gift模型类似
    """
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)

    @property
    def book(self):
        """
        类似于gift中的
        :return:
        """
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def get_user_wishes(cls, uid):
        """
        查询用户所有的心愿清单
        :param uid:
        :return:
        """
        wishes = Wish.query.filter_by(uid=uid, launched=False).order_by(
            desc(Wish.create_time)).all()
        return wishes

    @classmethod
    def get_gifts_counts(cls, isbn_list):
        """
        类似于gift中的内容
        :param isbn_list:
        :return:
        """
        from app.models.gift import Gift
        count_list = db.session.query(func.count(Gift.id), Gift.isbn).filter(
            Gift.launched == False,
            Gift.isbn.in_(isbn_list),
            Gift.status == 1).group_by(
            Gift.isbn).all()
        count_list = [{'count': g[0], 'isbn': g[1]} for g in count_list]
        return count_list
