from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, Posts
from datetime import datetime

main = Blueprint('main', __name__)

# Home Page
@main.route('/', methods = ["GET", "POST"])
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
            return redirect(url_for('main.index'))
        except Exception as e:
            return f"ERROR {e}"


# Full Post
@main.route("/post/<int:id>")
def post_detail(id):
    post = Posts.query.get_or_404(id)
    return render_template("post_detail.html", post=post)


# Delete a Post
@main.route("/post/<int:id>/delete", methods=["POST"])
def delete_post(id):
    post = Posts.query.get_or_404(id)
    try:
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    except Exception as e:
        return f"Error {e}"


# Create New Post
@main.route("/newPost", methods = ["GET", "POST"])
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
            return redirect(url_for('main.index'))
        except Exception as e:
            return f"ERROR {e}"