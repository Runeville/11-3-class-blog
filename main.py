import os
from flask import Flask, render_template, session, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from db import *
from auth import *
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_required, current_user, logout_user, login_user
from forms import *
from datetime import datetime


Bootstrap(app)
app.secret_key = "h4lLUI7i&*"

UPLOAD_FOLDER = '/static/images/'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

login_manager = LoginManager(app)
login_manager.init_app(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
@redirect_unauthorized
def home():
    posts = search_posts()
    return render_template("blog/index.html", posts=posts)


@app.route('/register', methods=["POST", "GET"])
def register():
    if current_user.is_active is True:
        return redirect('/')
    register_form = RegisterForm()

    if register_form.validate_on_submit():  # Catching POST request

        login = register_form.login.data
        username = register_form.username.data
        password = generate_password_hash(register_form.password.data)  # Getting a hashed password

        if not User.query.filter_by(login=login).first():  # Making sure there's no user with the same login

            new_user = User(login=login, username=username, password=password)  # Creating new user
            db.session.add(new_user)  # Creating new user
            db.session.commit()

            login_user(new_user, remember=True)
            return redirect(url_for("home"))
        else:
            flash("This login is already used")

    return render_template("auth/register.html", form=register_form)


@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_active:
        return redirect('/')

    login_form = LoginForm()

    if login_form.validate_on_submit():
        try:
            user = User.query.filter_by(login=login_form.login.data).first()  # user = user found by login in DB
            if check_password_hash(user.password, login_form.password.data):  # Check if password is correct
                login_user(user, remember=True)
                return redirect('/')
            else:
                flash("Incorrect password")
        except AttributeError:
            flash("No such user registered")

    return render_template("auth/login.html", form=login_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect("/login")


@app.route('/users', methods=["POST", "GET"])
@redirect_unauthorized
def users():
    users = User.query.all()

    # If request method is POST change user status to selected
    if request.method == "POST":
        user_id = int(list(request.form.keys())[0])
        changed_status = int(request.form[str(user_id)])  # Return number of updated status

        user = User.query.filter_by(id=user_id).first()
        user.status = changed_status

        db.session.commit()

    return render_template("blog/users.html", users=users)


@app.route('/profile', methods=["POST", "GET"])
@redirect_unauthorized
def profile():
    username_form = UpdateProfileForm(username=current_user.username)
    password_form = UpdatePasswordForm()

    if username_form.validate_on_submit():
        current_user.username = username_form.username.data
        db.session.commit()

    if password_form.validate_on_submit():
        if check_password_hash(current_user.password, password_form.password.data):
            current_user.password = generate_password_hash(password_form.new_password.data)
            db.session.commit()
        else:
            flash("Incorrect old password")

    return render_template("blog/profile.html", username_form=username_form, password_form=password_form)


@app.route('/add_post', methods=["POST", "GET"])
@redirect_unauthorized
@redirect_with_status(1)
def add_post():
    form = AddPostForm()

    if form.validate_on_submit():
        file = form.image.data
        filename = secure_filename(file.filename)
        if allowed_file(filename):
            path = os.getcwd().replace("\\", "/")
            file.save(path + app.config['UPLOAD_FOLDER'] + filename)
            new_post = Post(title=form.title.data, author=current_user.id,
                            content=form.content.data, image=filename)  # Adding new post
        else:
            new_post = Post(title=form.title.data, author=current_user.id,
                            content=form.content.data)  # Adding new post
        db.session.add(new_post)
        db.session.commit()  # Committing new post to DB
        return redirect('/')

    return render_template("blog/add_post.html", form=form)


@app.route('/update_post/<int:post>', methods=["POST", "GET"])
def update_post(post):
    post = Post.query.filter_by(id=post).first()
    if not current_user.is_active or current_user.id != post.author:
        return redirect('/')

    form = UpdatePostForm(title=post.title, content=post.content)

    if form.validate_on_submit():
        file = form.image.data
        filename = secure_filename(file.filename)
        if allowed_file(filename):
            path = os.getcwd().replace("\\", "/")
            file.save(path + app.config['UPLOAD_FOLDER'] + filename)
            post.image = filename

        post.title = form.title.data
        post.content = form.content.data
        post.update_date = datetime.utcnow()

        db.session.commit()  # Committing new post to DB
        return redirect('/')

    return render_template("blog/update_post.html", form=form)


@app.route('/delete_post/<int:post>')
def delete_post(post):
    post = Post.query.filter_by(id=post).first()

    if current_user.is_active and current_user.status > 1 or current_user.id == post.author and current_user.status > 0:
        db.session.delete(post)
        db.session.commit()

    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
