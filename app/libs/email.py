from threading import Thread
from flask import current_app, render_template
from app import mail
from flask_mail import Message


"""
使用flask-mail插件的mail对象来发送邮件
to 邮件目标用户的地址
subject 发送的邮件标题
template 指定的模板名称
**kwargs 传入到template中的一组参数
"""


def send_async_mail(app, msg):
    """
    异步函数，异步进行邮件的发送
    代理对象受到线程的影响，直接使用flask对象进行操作
    :param msg:
    :return:
    """
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            pass


def send_mail(to, subject, template, **kwargs):
    """
    异步发送电子邮件 aaa@qq.com 为自己邮箱测试 自己给自己发送邮件
    # msg = Message('测试邮件', sender='aaa@qq.com', body='Test',
    #               recipients=['aaa@qq.com'])
    :param to:
    :param subject:
    :param template:
    :param kwargs:
    :return:
    """
    msg = Message('[鱼书]' + ' ' + subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.html = render_template(template, **kwargs)
    # 拿到真实的flask核心对象app
    app = current_app._get_current_object()
    # 线程
    thr = Thread(target=send_async_mail, args=[app, msg])
    thr.start()
