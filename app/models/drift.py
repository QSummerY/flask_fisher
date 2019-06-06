from app.libs.enums import PendingStatus
from app.models.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, SmallInteger


class Drift(Base):
    """
    Drift的实质是记录 鱼漂信息：一次具体的交易信息
    没有使用模型关联：在user模型中已经存在,使用信息冗余
    模型中有关联：每次查询时，关联模型的信息都是最新的
        缺：没事忠实记录交易时的状态、关联查询需要查询多张表，查询速度慢
    模型中无关联：不是实时的，是历史的记录，数据有冗余（合理的利用冗余），减少查询次数

    鱼漂有四种交易状态（pending）：等待、撤销（请求者）、成功、拒绝（赠送者）
    """
    id = Column(Integer, primary_key=True)

    # 邮寄信息
    recipient_name = Column(String(20), nullable=False)
    address = Column(String(100), nullable=False)
    message = Column(String(200))
    mobile = Column(String(20), nullable=False)

    # 书籍信息
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(50))

    # 请求者信息
    requester_id = Column(Integer)
    requester_nickname = Column(String(20))

    # 赠送者信息
    gifter_id = Column(Integer)
    gift_id = Column(Integer)
    gifter_nickname = Column(String(20))

    _pending = Column('pending', SmallInteger, default=1)

    # 模型关联
    # requester_id = Column(Integer, ForeignKey('user.id'))
    # requester = relationship('User')
    # gift_id = Column(Integer, ForeignKey('gift.id'))
    # gift = relationship('Gift')

    @property
    def pending(self):
        """
        获取枚举类型，直接.pending得到
        :return:
        """
        return PendingStatus(self._pending)

    @pending.setter
    def pending(self, status):
        """
        将枚举类型转化成数字类型，例：直接.pengding.Waiting
        :param status:
        :return:
        """
        self._pending = status.value
