from flask import request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from __init__ import app
from flask_login import LoginManager, UserMixin

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog_database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    username = db.Column(db.String(40), nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"{self.username}"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    update_date = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"{self.title}"


def search_posts():
    """ Return all posts depending on search GET request """
    get_posts = Post.query.order_by(Post.id.desc()).all()
    posts = []  # Getting all posts
    if request.args.get('search') is None:
        for post in get_posts:  # Getting all posts
            author = User.query.filter_by(id=post.author).first()  # Finding an author

            try:  # Catching update_date if exist
                update_date = post.update_date.strftime("%d.%m.%Y")
            except AttributeError:
                update_date = None
            posts.append({
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'author': author.username,
                'date': post.date.strftime("%d.%m.%Y"),
                'update_date': update_date
            })
    else:
        for post in get_posts:  # Getting all posts
            author = User.query.filter_by(id=post.author).first()  # Finding an author
            try:  # Catching update_date if exist
                update_date = post.update_date.strftime("%d.%m.%Y")
            except AttributeError:
                update_date = None
            if post.title.find(request.args.get('search')) >= 0:
                posts.append({
                    'id': post.id,
                    'title': post.title,
                    'content': post.content,
                    'author': author.username,
                    'date': post.date.strftime("%d.%m.%Y"),
                    'update_date': update_date
                })
    return posts


db.create_all()
