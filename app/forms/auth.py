from wtforms import Form, StringField, PasswordField
from wtforms.validators import Length, DataRequired, Email, ValidationError, EqualTo
from app.models.user import User


class RegisterForm(Form):
    """
    注册校验
    """
    email = StringField(validators=[DataRequired(), Length(8, 64),
                        Email(message="电子邮箱不符合规范")])

    password = PasswordField(validators=[
        DataRequired(message="密码不可以为空，请输入你的密码"), Length(6, 25)])

    nickname = StringField(validators=[
        DataRequired(), Length(2, 10, message="昵称至少需要2个字符，最多10个字符")])

    def validate_email(self, field):
        """
        自定义的验证器不用加入到上面中，因为它自己知道是对email的验证
        业务校验，数据库中是否已经存在输入的email，通过查询一遍数据
        field 表示传入的email参数 用.first()触发查询 只返回一条
        filter_by() 是查询条件，可以放入一组查询内容
        :return:
        """
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("电子邮件已被注册")

    def validate_nickname(self, field):
        """
        自定义验证器 验证昵称是否存在
        :param field:
        :return:
        """
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError("昵称已存在")


class LoginForm(Form):
    """
    登录校验
    """
    email = StringField(validators=[DataRequired(), Length(8, 64),
                                    Email(message="电子邮箱不符合规范")])
    password = PasswordField(validators=[
        DataRequired(message="密码不可以为空，请输入你的密码"), Length(6, 32)])


class EmailForm(Form):
    """
    电子邮箱校验
    """
    email = StringField(validators=[DataRequired(), Length(8, 64),
                                    Email(message="电子邮箱不符合规范")])


class ResetPasswordForm(Form):
    """
    更改密码或重置密码时：新密码与确认密码验证
    """
    password1 = PasswordField(validators=[
        DataRequired(),
        Length(6, 32, message='密码长度至少需要在6到20个字符之间'),
        EqualTo('password2', message='两次输入的密码不相同')])
    password2 = PasswordField(validators=[
        DataRequired(), Length(6, 32)])
