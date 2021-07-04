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
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    update_date = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"{self.title}"


db.create_all()
