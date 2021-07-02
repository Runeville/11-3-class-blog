from flask import Flask, render_template
from db import db, User, Post

app = Flask(__name__)

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


@app.route('/add_post')
def add_post():
    return "Add post"


if __name__ == "__main__":
    app.run(debug=True)
