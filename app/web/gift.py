from flask import current_app, flash, redirect, url_for, render_template

from app.libs.enums import PendingStatus
from app.models.drift import Drift
from app.view_models.trade import MyTrades
from . import web
from flask_login import login_required, current_user
from app.models.gift import Gift
from app.models.base import db
from app.view_models.gift import MyGifts


@web.route('/my/gifts')
@login_required
def my_gifts():
    """
    用插件的装饰器@login_required来控制必须要登录后才能去这个页面
    赠送清单：礼物清单、倒序排列、书籍想要人的数量、我的礼物总数量、可撤销
    :return:
    """
    uid = current_user.id
    gifts_of_mine = Gift.get_user_gifts(uid)
    isbn_list = [gift.isbn for gift in gifts_of_mine]
    wish_count_list = Gift.get_wish_counts(isbn_list)
    # view_model = MyGifts(gifts_of_mine, wish_count_list)
    # return render_template('my_gifts.html', gifts=view_model.gifts)
    view_model = MyTrades(gifts_of_mine, wish_count_list)
    return render_template('my_gifts.html', gifts=view_model.trades)
    # return 'My Gifts'


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    """
    赠送书籍
    current_user 就是我们实例化后的User模型，可以通过模型去拿到属性
    :param isbn:
    :return:
    """
    if current_user.can_save_to_list(isbn):
        # 事务 提交与回滚
        try:
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id

            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    else:
        # ajax 技术进行改善原本所在页面在完成要求后回到原页面
        flash('这本书已添加至你的赠送清单或已存在于你的心愿清单，请不要重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
@login_required
def redraw_from_gifts(gid):
    """
    撤销礼物
    若是在交易等待情况下，不能直接撤销掉礼物，应先处理交易
    :param gid:
    :return:
    """
    gift = Gift.query.filter_by(id=gid, launched=False).first_or_404()
    drift = Drift.query.filter_by(
        gift_id=gid, pending=PendingStatus.Waiting).first()
    if drift:
        flash('这个礼物正处于交易状态，请先前往鱼漂完成该交易')
    else:
        with db.auto_commit():
            current_user.beans -= current_app.config['BEANS_UPLOAD_ONE_BOOK']
            gift.delete()
    return redirect(url_for('web.my_gifts'))



