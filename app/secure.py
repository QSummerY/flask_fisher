"""
配置文件:
1、类似于数据密码等机密信息的存放
2、生产环境和开发环境不同的参数存放
"""
# SQLALCHEMY_TRACK_MODIFICATIONS修改SQLALCHEMY的源码
# cymysql 数据库驱动
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:123456@localhost:3306/fisher'

SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = '\x88D\xf09\x91\x07\x98\x89\x96\xa0A\xc68\xf9\xecJ:U\x17\xc5V\xbe\x87'

"""
Email 配置
MAIL_SERVER:电子邮件服务器地址，使用qq的公开电子邮件服务器
MAIL_PORT：电子邮件服务器地址
MAIL_USE_SSL：qq使用的是ssl协议
"""
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TSL = False
MAIL_USERNAME = ''
MAIL_PASSWORD = ''

# MAIL_SUBJECT_PREFIX = '[鱼书]'
# # MAIL_SENDER = '鱼书 <hello@yushu.im>'
