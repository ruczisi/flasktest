from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms import StringField,SubmitField,TextAreaField,BooleanField,SelectField,ValidationError
from wtforms.validators import DataRequired,Length,Email,Regexp
from ..models import Role,User

class EditProfileForm(FlaskForm):
    name = StringField('真实姓名',validators=[Length(0,64)])
    location = StringField('所在地',validators=[Length(0,64)])
    about_me = TextAreaField('个人简介')
    submit = SubmitField('提交')

class EditProfileAdminForm(FlaskForm):
    email = StringField('邮箱',validators=[DataRequired(),Length(1,64),Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          '用户名只能包含字母、数字或.或下划线')])
    confirmed = BooleanField('验证')
    role = SelectField('角色',coerce=int)
    name = StringField('真实姓名',validators=[Length(0,64)])
    location = StringField('所在地',validators=[Length(0,64)])
    about_me = TextAreaField('个人简介')
    submit = SubmitField('提交')

    def __init__(self,user,*args,**kwargs):
        super(EditProfileAdminForm,self).__init__(*args,**kwargs)
        self.role.choices = [(role.id,role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

        def validate_email(self,field):
            if field.data != self.user.email and User.query.filter_by(email=field.data).first():
                raise ValidationError('邮箱已存在！')

        def validate_username(self,field):
            if field.data != self.user.username and User.query.filter_by(username=field.data).first():
                raise ValidationError('用户名已存在！')

class PostForm(FlaskForm):
    body = PageDownField('文章',validators=[DataRequired("多少说两句")])
    submit = SubmitField('提交')

class CommentForm(FlaskForm):
    body = StringField('评论',validators=[DataRequired()])
    submit = SubmitField('提交')
