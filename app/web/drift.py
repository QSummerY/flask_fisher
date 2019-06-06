# 鱼漂：发送鱼漂、鱼漂记录页、拒绝赠书、同意赠书并已邮寄、撤销请求
from flask import flash, redirect, url_for, render_template, request, current_app
from sqlalchemy import desc, or_
from app.forms.book import DriftForm
from app.libs.email import send_mail
from app.libs.enums import PendingStatus
from app.models.base import db
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.user import User
from app.models.wish import Wish
from app.view_models.book import BookViewModel
from app.view_models.drift import DriftCollection
from . import web
from flask_login import login_required, current_user

__author__ = '七月'


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    """
    发送鱼漂，请求书籍
    :param gid:
    :return:
    """
    current_gift = Gift.query.get_or_404(gid)
    # 自己不能向自己请求书籍
    if current_gift.is_yourself_gift(current_user.id):
        flash('这本书是你自己的^_^,不能向自己索要书籍嗷~~')
        return redirect(url_for('web.book_detail', isbn=current_gift.isbn))

    # 判断鱼豆以及索取和赠送关系是否满足条件
    can = current_user.can_send_drift()
    if not can:
        return render_template('not_enough_beans.html', beans=current_user.beans)

    # 输入的参数校验
    form = DriftForm(request.form)
    if request.method == 'POST' and form.validate():
        save_drift(form, current_gift)
        send_mail(current_gift.user.email, '有人想要一本书',
                  'email/get_gift.html', wisher=current_user, gift=current_gift)
        return redirect(url_for('web.pending'))

    gifter = current_gift.user.summary
    return render_template('drift.html',
                           gifter=gifter, user_beans=current_user.beans, form=form)


@web.route('/pending')
@login_required
def pending():
    """
    显示交易记录 我作为赠送者 or 我作为请求者
    使用or_() 进行or关系的转化
    :return:
    """
    drifts = Drift.query.filter(
        or_(Drift.requester_id == current_user.id, Drift.gifter_id == current_user.id)).order_by(
        desc(Drift.create_time)).all()

    views = DriftCollection(drifts, current_user.id)
    return render_template('pending.html', drifts=views.data)


@web.route('/drift/<int:did>/reject')
@login_required
def reject_drift(did):
    """
    拒绝
    使用filter查询，查询两个表Gift和Drift
    进行超权控制
    :param did:
    :return:
    """
    with db.auto_commit():
        drift = Drift.query.filter(Gift.uid == current_user.id,
                                   Drift.id == did).first_or_404()
        drift.pending = PendingStatus.Reject
        requester = User.query.get_or_404(drift.requester_id)
        requester.beans += 1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/redraw')
@login_required
def redraw_drift(did):
    """
    索要书籍等待时的撤销操作
    安全问题：超权
    假设：uid:1 -> did:1   uid:2 -> did:2
    若uid:1 将传入的did改为2，下面的逻辑仍然可以执行   ->  超权问题
    解决办法：在查询条件中加上requester_id判断
    :param did:
    :return:
    """
    with db.auto_commit():
        drift = Drift.query.filter_by(
            requester_id=current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.Redraw
        current_user.beans += 1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/mailed')
@login_required
def mailed_drift(did):
    """
    已邮寄  launched 判断是否成功交易
    Gift部分：是否成功赠送
    Wish部分：心愿完成后的数据修改
    两部分执行逻辑一样，写法不一致罢了
    数据库事务的支持：事务保持一致性
    :param did:
    :return:
    """
    with db.auto_commit():
        drift = Drift.query.filter_by(
            gifter_id=current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.Success
        current_user.beans += 1

        gift = Gift.query.filter_by(id=drift.gift_id).first_or_404()
        gift.launched = True

        Wish.query.filter_by(isbn=drift.isbn, uid=drift.requester_id,
                             launched=False).update({Wish.launched: True})
    return redirect(url_for('web.pending'))


def save_drift(drift_form, current_gift):
    """
    将交易填入的信息装在到模型中
    :param drift_form:
    :param current_gift:
    :return:
    """
    with db.auto_commit():
        drift = Drift()
        # drift.message = drift_form.message.data
        drift_form.populate_obj(drift)

        drift.gift_id = current_gift.id
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        drift.gifter_id = current_gift.user.id
        drift.gifter_nickname = current_gift.user.nickname

        book = BookViewModel(current_gift.book)
        drift.book_title = book.title
        drift.book_author = book.author
        drift.book_img = book.image
        drift.isbn = book.isbn

        current_user.beans -= 1

        db.session.add(drift)
