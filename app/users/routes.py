from app.users.models import User
from app.posts.models import Post
from app.utils.helpers import send_reset_email
from app.users.forms import RegistrationForm, LoginForm, UpdateForm, RequestPasswordForm, RequestResetForm
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required


users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        flash('Registered successfully', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_user(email=form.email.data)
        if not user or not user.check_password(form.password.data):
            flash('Invalid credentials, try again.', 'danger')
            return redirect(url_for('users.login'))
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        flash('Logged in successfully.', 'success')
        return redirect(next_page) if next_page else redirect(url_for('main.home'))
    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        User.update_user(user=current_user, form=form)
        flash('Updated successfully', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.get_user(username=username)
    posts = Post.get_all_posts(page=page, author=user)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.get_user(email=form.email.data)
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset password',
                           form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token=token)
    if not user:
        flash('Invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = RequestPasswordForm()
    if form.validate_on_submit():
        User.reset_password(user=user, form=form)
        flash('Password updated successfully', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset password', form=form)
