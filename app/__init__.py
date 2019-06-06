from flask import Flask
from app.models.book import db
from flask_login import LoginManager
from flask_mail import Mail

# login 插件的初始化
login_manager = LoginManager()
# mail 插件的实例化
mail = Mail()


def create_app():
    """
    初始化 flask 核心对象
    app = Flask(__name__, static_folder='view_models/statics') 静态文件操作可以这样
    template_folder 模板文件可以这样修改
    :return:
    """
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)

    # 将SQLAlchemy的对象 db 和flask核心对象 app 关联起来
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或注册'

    # 注册mail插件
    mail.init_app(app)

    with app.app_context():
        db.create_all(app=app)
    return app


def register_blueprint(app):
    """
    在核心对象app中注册蓝图
    :param app:
    :return:
    """
    from app.web.book import web
    app.register_blueprint(web)
