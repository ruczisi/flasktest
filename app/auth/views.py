from flask import render_template,redirect,request,url_for,flash
from flask_login import login_user,login_required,logout_user,current_user
from . import auth
from ..models import User,db
from .forms import LoginForm,ResitrationForm,ChangeEmailForm,ChangePasswordForm,PasswordResetForm,PasswordResetRequestForm
from ..emails import send_email

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        if not current_user.confirmed and request.blueprint != 'auth.' and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('用户名或密码错误！')
    return render_template('auth/login.html',form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已退出系统')
    return redirect(url_for('main.index'))

@auth.route('/register',methods=['GET','POST'])
def register():
    form = ResitrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password = form.password.data)
        db.session.add(user)
        token = user.generate_confirmation_token()
        send_email(user.email,'验证您的账户','auth/email/confirmation',user=user,token=token)
        flash('验证短信已发送至您的邮箱')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('您的用户已通过验证')
    else:
        flash('验证连接已失效')
    return redirect(url_for('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email,'验证您的账户','auth/email/confirmation',user=current_user,token=token)
    flash('验证邮箱已再次发送')
    return redirect(url_for('main.index'))

@auth.route('/change-password',methods = ['GET','POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('密码更改成功')
            return redirect(url_for('main.index'))
        else:
            flash('密码有误')
    return render_template('auth/change_password.html',form=form)

@auth.route('/reset',methods = ['GET','POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email,'重置密码','auth/email/reset_password.html',user=user,token=token)
            flash("重置密码的验证邮件已发送，请根据邮件信息重置密码")
        return redirect(url_for('auth.login'))
    return  render_template('auth/reset_password.html.html',form=form)

@auth.route('/change_email',methods=['GET','POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data.lower()
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email,'邮箱修改确认','auth/email/change_email',user=current_user,token=token)
            flash("已向您新邮箱发送验证邮件，请前往邮箱按提示操作")
            return redirect(url_for('main.index'))
        else:
            flash('邮箱或密码无效')
    return render_template("auth/change_email.html",form=form)

@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash("您的邮箱信息已更新")
    else:
        flash("验证信息已无效")

    return redirect(url_for('main.index'))

