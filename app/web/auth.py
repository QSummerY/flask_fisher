"""
用户系统 注册、登录、找回密码、修改密码
"""
from . import web
from flask import render_template, request, redirect, url_for, flash
from app.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm
from app.models.user import User
from app.models.base import db
from flask_login import login_user, logout_user
from app.libs.email import send_mail


@web.route('/register', methods=['GET', 'POST'])
def register():
    """
    注册视图函数，使用form验证层
    注册成功后跳转到登录页面，使用redirect重定向
    :return:
    """
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User()
        user.set_attrs(form.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('web.login'))
        # user.password = generate_password_hash(form.password.data)  使密码加密的笨方法
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    """
    remember=True 加上这句话代表是一个持续的cookie
    :return:
    """
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            next_url = request.args.get('next')
            if not next_url or not next_url.startswith('/'):
                next_url = url_for('web.index')
            return redirect(next_url)
        else:
            flash("账号不存在或密码错误")
    return render_template('auth/login.html', form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    """
    忘记密码，使用邮箱重置密码  验证邮箱  验证邮箱的用户是否存在
    first_or_404():一旦查询没有找到任何结果，后续代码不会被执行，其内部抛出异常，呈现404页面
    first_or_404内部 可调用对象 _aborter 对象 当做 函数来调用，那么对象的类中必须有 __call__ 方法
    可调用对象的意义：简化对象下方法的调用（只有一个方法、对象下某个方法使用很多的时候）、模糊了对象和函数的区别（同一调用接口）
    :return:
    """
    form = EmailForm(request.form)
    if request.method == 'POST':
        if form.validate():
            account_email = form.email.data
            user = User.query.filter_by(email=account_email).first_or_404()
            send_mail(form.email.data, '重置你的密码',
                      'email/reset_password.html', user=user,
                      token=user.generate_token())
            flash('一封邮件已发送到邮箱' + account_email + '，请及时查收')
            # return redirect(url_for('web.login'))
    return render_template('auth/forget_password_request.html', form=form)


# 单元测试


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        success = User.reset_password(token, form.password1.data)
        if success:
            flash('你的密码已更新，请使用新密码登录')
            return redirect(url_for('web.login'))
        else:
            flash('密码重置失败')
    return render_template('auth/forget_password.html', form=form)


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))
