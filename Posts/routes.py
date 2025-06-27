from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from models import db, Post
from .form import PostForm

posts = Blueprint("posts", __name__)

@posts.route("/create/post", methods=["POST", "GET"])
@login_required
def create_post():
  form = PostForm()
  if form.validate_on_submit():
    try:
      new_post = Post(
        user_id = current_user.id,
        content = form.comments.data,
        book_title = form.book_title.data,
        book_author = form.book_author.data,
        status = form.status.data
      )
      db.session.add(new_post)
      db.session.commit()
      flash("Post created successfully", "success")
      return redirect(url_for('books.home'))
    except Exception as e:
      flash(f"{str(e)}", "danger")
      return redirect(url_for('posts.create_post'))
  
  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f"{err_msg}", "danger")
      return redirect(url_for('posts.create_post'))

  context = {
    "form": form
  }
  
  return render_template("Posts/create-post.html", **context)
