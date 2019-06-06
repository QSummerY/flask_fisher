from math import floor
from flask import current_app
from sqlalchemy import Column, Integer, String, Boolean, Float
from app.libs.enums import PendingStatus
from app.models.base import Base, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login_manager
from app.libs.helper import is_isbn_or_key
from app.models.drift import Drift
from app.spider.yushu_book import YuShuBook
from app.models.gift import Gift
from app.models.wish import Wish
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(UserMixin, Base):
    """
    # __tablename__ = 'user1'
    beans 存放的就是鱼豆的数量
    """
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))
    _password = Column('password', String(128), nullable=False)

    @property
    def password(self):
        """
        对某一属性的读取  一般称为getter  对操作的数据预处理
        :return:
        """
        return self._password

    @password.setter
    def password(self, raw):
        """
        属性的赋值  一般称为setter  对操作的数据预处理 加密后赋值
        :param raw:
        :return:
        """
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        """
        raw 获取的明文密码，将其加密再与数据库中的密码进行比较
        :param raw:
        :return:
        """
        return check_password_hash(self._password, raw)

    # def get_id(self):
    #     """
    #     flask-login要求的
    #     函数名固定，不能更改，返回用户确定的id号
    #     用继承UserMixin的方式后就不用自己写这样的函数了
    #     如果不是用id来表示用户的身份，还是需要重写这个函数来覆盖get_id的内容
    #     :return:
    #     """
    #     return self.id

    def can_save_to_list(self, isbn):
        """
        校验：
        1、不满足isbn的规范则不允许保存书籍
        2、验证图书数据库中是否存在这本书籍
        3、不允许一个用户同时赠送多本相同的图书
        4、一个用户不可能同时成为赠送者和索要者
        :param isbn:
        :return:
        """
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False

        # 赠送图书既不在赠送清单也不再心愿清单中才能添加
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        if not gifting and not wishing:
            return True
        else:
            return False

    def generate_token(self, expiration=600):
        """
        生成token值（在token中放入用户的ID，还可以放其他信息），方便重置密码时确定用户
        Serializer() 实例化一个序列化器
        s.dumps({'id': self.id}) 结果为 字节类型，用decode将其转换成字符串
        :param expiration:
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        """
        重置密码，通过token获取用户的id
        将用户重置后的密码替换原本的密码
        :param token:
        :param new_password:
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        uid = data.get('id')
        with db.auto_commit():
            user = User.query.get(uid)
            user.password = new_password
        return True

    def can_send_drift(self):
        """
        判断是否能够发起交易：
        鱼豆必须大于等于1
        每索取两本书，自己必须送出一本书
        :return:
        """
        if self.beans < 1:
            return False
        success_gifts_count = Gift.query.filter_by(
            uid=self.id, launched=True).count()
        success_receive_count = Drift.query.filter_by(
            requester_id=self.id, pending=PendingStatus.Success).count()

        return True if \
            floor(success_receive_count / 2) <= floor(success_gifts_count) \
            else False

    @property
    def summary(self):
        """
        摘取部分信息渲染索要书籍信息页面
        :return:
        """
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.send_counter) + '/' + str(self.receive_counter)
        )


@login_manager.user_loader
def get_user(uid):
    """
    把id号转化为对象模型，这样current_user就变成用户模型
    :param uid:
    :return:
    """
    return User.query.get(int(uid))
