#create users blueprint
from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from flaskblog import db, bcrypt
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required 
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)
#change all @app.route to users. route...users is defined with blueprint above

@users.route("/register", methods=['GET', 'POST'])
# include methods to accept both post and get requests so that registration forms can submit
def register():
    #condition prevents register page from opening after user has logged in already
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # if form submits, hash the passwords in db. Then add registered users to database
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('users.login'))
        # After successful submission, redirect to home page. success after form.username is a bootsrap attribute
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    #condition prevents login page from opening after user has logged in already. If current user is logged in rediret to home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        #Check if any email in database is equal to input email
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            #login_user function takes in a remeber arguement as well
            login_user(user, remember=form.remember.data)
            #If a user tries to access account page directly by putting /account in browser withou logging in, they will
            #be redirected to login page after which they should be redirected to the page they want instead of home
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form) 

#create logout route
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=['GET', 'POST'])
#login is required for account route to work
@login_required
def account():
    form = UpdateAccountForm()
    #change username and email on account page 
    if form.validate_on_submit():
        #save picture on account with file name created above
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file #image_file is used in model whilr picture is used in forms
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('users.account'))
    #display current username and email on account page
    elif request.method=='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form) 

#posts for one user
@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    # get all posts by this user
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date.desc()).paginate(page=page, per_page=3) 
    return render_template('user_posts.html', posts=posts, user=user)

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    #User has to be logged out to access this page. If current user is logged in rediret to home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit:
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

#route to reset password
@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    #User has to be logged out to access this page. If current user is logged in rediret to home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # if form submits, hash the passwords in db. Then add registered users to database
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You can now log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)