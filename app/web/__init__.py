from flask import Blueprint, render_template

web = Blueprint('web', __name__)


@web.app_errorhandler(404)
def not_found(e):
    """
    app_errorhandler 装饰器属于蓝图对象的 监听404的异常
    在 not_found() 内部可以实现任何想实现的业务逻辑
    基于AOP思想 面向切片编程
    :param e:
    :return:
    """
    return render_template('404.html'), 404


# 导入执行视图函数
from app.web import book
from app.web import auth
from app.web import drift
from app.web import gift
from app.web import main
from app.web import wish
