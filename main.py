from flask import Flask, render_template
from __init__ import app
from flask_bootstrap import Bootstrap
from db import db, User, Post
from auth import RegisterForm
from werkzeug.security import generate_password_hash


Bootstrap(app)
app.secret_key = "h4lLUI7i&*"


# new_post = Post(title="title", author=1, content="sdfsaf")
# db.session.add(new_post)
# db.session.commit()


get_posts = Post.query.all()
posts = []
for post in get_posts:
    posts.append({
        'title': post.title,
        'content': post.content,
        'author': post.author,
        'date': post.date.strftime("%d.%m.%Y")
    })


@app.route('/')
def home():
    return render_template("blog/index.html", posts=posts)


@app.route('/register', methods=["POST", "GET"])
def register():
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        if not User.query.filter_by(login=register_form.login.data).first():  # Making sure there's no user with the
            # same login
            password = generate_password_hash(register_form.password.data)  # Getting a hashed password
            new_user = User(login=register_form.login.data, username=register_form.username.data, password=password)
            db.session.add(new_user)  # Making new user
            db.session.commit()
        else:
            print("This login is already used")

    return render_template("auth/register.html", form=register_form)


@app.route('/add_post')
def add_post():
    return "Add post"


if __name__ == "__main__":
    app.run(debug=True)
