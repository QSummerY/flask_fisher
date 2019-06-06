# 书籍搜索、书籍详情页
from flask import jsonify, request, render_template, flash
from flask_login import current_user
from app.forms.book import SearchForm
from app.libs.helper import is_isbn_or_key
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook
from app.view_models.trade import TradeInfo
from . import web
from app.view_models.book import BookCollection, BookViewModel


@web.route('/book/search')
def search():
    """
    q ：普通关键字  isbn
    page ： start  count
    ?q=金庸&page=1
    通过Request获取查询对象
    :return:
    """
    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)

        books.fill(yushu_book, q)
        # python 不能直接序列化对象，但是能够序列化字典 一般的对象可以用.__dict__方法  这里使用json.dumps()
        # return jsonify(books.__dict__)
        # return json.dumps(books, default=lambda o: o.__dict__)
    else:
        flash('搜索的关键字不符合要求，请重新输入关键字0')
        # return jsonify(form.errors)
    return render_template('search_result.html', books=books)


@web.route('/test')
def test():
    # 字典中data['age']
    r = {
        'name': '',
        'age': 20,
    }
    r1 = {

    }
    flash('hello, SummerY', category='error')
    flash('hello, July', category='warning')
    # 引入模板 HTML(没有数据)
    return render_template('test.html', data=r, data1=r1)
    # return render_template('test2.html', data=r, data1=r1)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    """
    显示书籍的详情数据
    has_in_gifts、has_in_wishes  在礼物清单、在心愿清单中  默认情况(未登录)
    取书籍详情数据并将其渲染到模板中
    :param isbn:
    :return:
    """
    has_in_gifts = False
    has_in_wishes = False

    # 取书籍详情数据
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)

    # 登录后，判断是赠书者还是心愿者
    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_wishes = True

    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

    trade_wishes_model = TradeInfo(trade_wishes)
    trade_gifts_model = TradeInfo(trade_gifts)

    return render_template('book_detail.html', book=book,
                           wishes=trade_wishes_model, gifts=trade_gifts_model,
                           has_in_gifts=has_in_gifts, has_in_wishes=has_in_wishes)


@web.route('/test1')
def test1():
    from flask import request
    from app.libs.none_local import n
    print(n.v)
    n.v = 2
    print('--------------')
    print(getattr(request, 'v', None))
    setattr(request, 'v', 2)
    print('--------------')
    return ''
