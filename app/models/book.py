"""
book 为书籍业务模型
选择sqlalchemy自动映射数据库
"""
from sqlalchemy import Column, Integer, String
from app.models.base import db


class Book(db.Model):
    """
    书编号、标题、作者、装帧版本（精装/平装）、出版社、价格、页数、出版时间、isbn、简介、图片
    """
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column(String(30), default='未名')
    binding = Column(String(20))
    publisher = Column(String(50))
    price = Column(String(20))
    pages = Column(Integer)
    pubdate = Column(String(20))
    isbn = Column(String(15), nullable=False, unique=True)
    summary = Column(String(1000))
    image = Column(String(50))

    def sample(self):
        """
        样本
        :return:
        """
        pass
