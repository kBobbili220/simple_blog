# Imports
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_scss import Scss
from datetime import datetime

app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
db = SQLAlchemy(app)

# Post Data
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    body = db.Column(db.Text, nullable=False)
    posted_at = db.Column(db.DateTime, default=datetime.now)

# Home Page
@app.route('/', methods = ["GET", "POST"])
def index():
    # Display all posts if GET
    if request.method == "GET":
        posts = Posts.query.all()
        print(posts)
        return render_template("index.html", posts=posts)
    # Create a new blog post
    else:
        title = request.form.get('title')
        author = request.form.get('author')
        body = request.form.get('body')
        newPost = Posts(title=title, body=body, author=author)

        try:
            db.session.add(newPost)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            return f"ERROR {e}"


# Full Post
@app.route("/post/<int:id>")
def post_detail(id):
    post = Posts.query.get_or_404(id)
    return render_template("post_detail.html", post=post)


# Delete a Post
@app.route("/post/<int:id>/delete", methods=["POST"])
def delete_post(id):
    post = Posts.query.get_or_404(id)
    try:
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error {e}"


# Create New Post
@app.route("/newPost", methods = ["GET", "POST"])
def create_post():
    if request.method == "GET":
        return render_template("new_post.html")
    else:
        title = request.form.get('title')
        author = request.form.get('author')
        body = request.form.get('body')
        newPost = Posts(title=title, body=body, author=author)

        try:
            db.session.add(newPost)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            return f"ERROR {e}"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
    app.run(debug = True)
