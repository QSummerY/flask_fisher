from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, Integer, SmallInteger
from contextlib import contextmanager
from datetime import datetime


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        """
        自定义Query  （kwargs  字典）
        替换flask_sqlalchemy源码中的内容去重写filter_by()，使 status = 1 默认为其中的查询参数
        替换Query 在实例化SQLAlchemy的时候进行 添加参数 query_class=Query
        :param kwargs:
        :return:
        """
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)


class SQLAlchemy(_SQLAlchemy):
    """
    将数据自动提交给数据库
    """
    @contextmanager
    def auto_commit(self):
        try:
            yield self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


# 实例化SQLAlchemy对象
db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    """
    设置__abstract__使其不去创建Base表，让Base作为基类
    create_time 记录当前模型生成和保存的时间
    软删除，使用状态标记位来代表其已经被删除  status  若查询条件不包括status=1，则会将删除的数据也显示出来
    """
    __abstract__ = True
    create_time = Column('create_time', Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    def set_attrs(self, attrs_dict):
        """
        如果对象包含某个属性，则将其值赋给这个属性的value
        hasattr（）可以判断一个对象下面是否包含某个属性
        :param attrs_dict:
        :return:
        """
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    @property
    def create_datetime(self):
        """
        将时间戳转换为时间对象，便于后续时间的转化
        :return:
        """
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def delete(self):
        """
        模型的删除操作
        :return:
        """
        self.status = 0
