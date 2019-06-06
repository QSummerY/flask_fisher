from app.libs.enums import PendingStatus


class DriftCollection:
    """
    集合类型的DriftViewModel
    """
    def __init__(self, drifts, current_user_id):
        self.data = []
        self.__parse(drifts, current_user_id)

    def __parse(self, drifts, current_user_id):
        for drift in drifts:
            temp = DriftViewModel(drift, current_user_id)
            self.data.append(temp.data)


class DriftViewModel:
    """
    单个的
    """
    def __init__(self, drift, current_user_id):
        """
        用字典来代表所有的实例属性
        :param drift:
        """
        self.data = self.__parse(drift, current_user_id)

    @staticmethod
    def requester_or_gifter(drift, current_user_id):
        """
        判断控制状态变量是 requester 还是 gifter
        :param drift:
        :param current_user_id:
        :return:
        """
        if drift.requester_id == current_user_id:
            you_are = 'requester'
        else:
            you_are = 'gifter'
        return you_are

    def __parse(self, drift, current_user_id):
        """
        处理原始数据向ViewModel转化的过程
        you_are: 控制状态变量
        :param drift:
        :return:
        """
        you_are = self.requester_or_gifter(drift, current_user_id)
        pending_status = PendingStatus.pending_str(drift.pending, you_are)

        r = {
            'you_are': you_are,
            'drift_id': drift.id,
            'book_title': drift.book_title,
            'book_author': drift.book_author,
            'book_img': drift.book_img,
            'date': drift.create_datetime.strftime('%Y-%m-%d'),
            'message': drift.message,
            'address': drift.address,
            'recipient_name': drift.recipient_name,
            'mobile': drift.mobile,
            'status': drift.pending,
            'operator': drift.requester_nickname if you_are != 'requester' else drift.gifter_nickname,
            'status_str': pending_status,
        }
        return r
