from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
    email = StringField('邮箱',validators=[DataRequired('请输入用户邮箱'),Length(1,64),Email()])
    password = PasswordField('密码',validators=[DataRequired('密码不能为空')])
    remember_me = BooleanField('记住我！')
    submit = SubmitField('登录')

class ResitrationForm(FlaskForm):
    email = StringField('邮箱',validators=[DataRequired('邮箱不能为空'),Length(1,64),Email()])
    username = StringField('用户名',validators=[DataRequired('用户名不能为空'),Length(1,64),
                                             Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'用户名只能包含字母,数字,点或下划线')])
    password = PasswordField('密码',validators=[DataRequired(),EqualTo('password2',message='两次输入的密码不相同')])
    password2 = PasswordField('验证密码',validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('旧密码',validators=[DataRequired()])
    password = PasswordField('新密码',validators=[DataRequired(),
                                               EqualTo('password2',message='两次输入密码必须相同')])
    password2 = PasswordField('重复新密码',validators=[DataRequired()])
    submit = SubmitField('保存')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('邮箱',validators=[DataRequired(),Length(1,64),
                                         Email()])
    submit = SubmitField('重置密码')

class PasswordResetForm(FlaskForm):
    password = PasswordField('新密码', validators=[
        DataRequired(), EqualTo('password2', message='两次输入密码必须相同')])
    password2 = PasswordField('重复新密码', validators=[DataRequired()])
    submit = SubmitField('重置密码')


class ChangeEmailForm(FlaskForm):
    email = StringField('新邮箱',validators=[DataRequired(),Length(1,64),Email()])
    password = PasswordField('密码',validators=[DataRequired()])
    submit = SubmitField('保存')

    def validate_email(self,field):
        if User.query.filter_by(email = field.data.lower()).first():
            raise ValidationError('邮箱已存在')