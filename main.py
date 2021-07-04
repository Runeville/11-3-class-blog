from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from db import *
from auth import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, current_user, logout_user, login_user
from forms import *

Bootstrap(app)
app.secret_key = "h4lLUI7i&*"

login_manager = LoginManager(app)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
@redirect_unauthorized
def home():
    get_posts = Post.query.order_by(Post.id.desc()).all()
    posts = []  # Getting all posts
    for post in get_posts:  # Getting all posts
        author = User.query.filter_by(id=post.author).first()  # Finding an author
        posts.append({
            'title': post.title,
            'content': post.content,
            'author': author.username,
            'date': post.date.strftime("%d.%m.%Y")
        })
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
            print("This login is already used")

    return render_template("auth/register.html", form=register_form)


@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_active is True:
        return redirect('/')

    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = User.query.filter_by(login=login_form.login.data).first()  # user = user found by login in DB
        if check_password_hash(user.password, login_form.password.data):  # Check if password is correct
            login_user(user, remember=True)
            return redirect('/')

    return render_template("auth/login.html", form=login_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect("/login")


@app.route('/users')
@redirect_unauthorized
def users():
    users = User.query.all()
    return render_template("blog/users.html", users=users)


@app.route('/add_post', methods=["POST", "GET"])
@redirect_unauthorized
def add_post():
    form = AddPostForm()

    if form.validate_on_submit():
        new_post = Post(title=form.title.data, author=current_user.id, content=form.content.data)  # Adding new post
        db.session.add(new_post)
        db.session.commit()  # Committing new post to DB
        return redirect('/')

    return render_template("blog/add_post.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
