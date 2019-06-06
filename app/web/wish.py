from flask import flash, redirect, url_for, render_template

from app.libs.email import send_mail
from app.models.base import db
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.trade import MyTrades
from app.view_models.wish import MyWishes
from . import web
from flask_login import login_required, current_user

__author__ = '七月'


@web.route('/my/wish')
@login_required
def my_wish():
    uid = current_user.id
    wishes_of_mine = Wish.get_user_wishes(uid)
    isbn_list = [wish.isbn for wish in wishes_of_mine]
    gift_count_list = Wish.get_gifts_counts(isbn_list)
    # view_model = MyWishes(wishes_of_mine, gift_count_list)
    # return render_template('my_wish.html', wishes=view_model.gifts)
    view_model = MyTrades(wishes_of_mine, gift_count_list)
    return render_template('my_wish.html', wishes=view_model.trades)


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.uid = current_user.id
            wish.isbn = isbn
            db.session.add(wish)
    else:
        flash('这本书已添加至你的赠送清单或已存在于你的心愿清单，请不要重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
@login_required
def satisfy_wish(wid):
    """
    向别人赠送书籍，通过发邮件询问的方式
    :param wid:
    :return:
    """
    wish = Wish.query.get_or_404(wid)
    gift = Gift.query.filter_by(uid=current_user.id, isbn=wish.isbn).first()
    if not gift:
        flash('你还没有上传此书，'
              '请点击“加入到赠送清单”添加此书，添加前，请确保自己可以赠送此书')
    else:
        send_mail(Wish.user.email,
                  '有人想送你一本书', 'email/satisfy_wish.html',
                  wish=wish, gift=gift)
        flash('已向他/她发送了一封邮件，如果他/她愿意接受你的赠送，你将收到一个鱼漂')
    return redirect(url_for('web.book_detail', isbn=wish.isbn))



@web.route('/wish/book/<isbn>/redraw')
@login_required
def redraw_from_wish(isbn):
    """
    撤销心愿，不涉及鱼漂交易状态
    :param isbn:
    :return:
    """
    wish = Wish.query.filter_by(isbn=isbn, launched=False).first_or_404()
    with db.auto_commit():
        wish.delete()
    return redirect(url_for('web.my_wish'))

