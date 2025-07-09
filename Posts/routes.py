from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from models import db, Post, Likes, Comment
from .form import PostForm, CommentForm

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

@posts.route("/like/posts/<int:post_id>")
@login_required
def like_post(post_id):
  post = Post.query.filter_by(unique_id=post_id).first()
  if not post:
    flash("Post not found", "danger")
    return redirect(url_for('books.home'))
  try:
    existing_like = Likes.query.filter_by(user_id=current_user.id, post_id=post.id).first()
    if not existing_like:
      new_like = Likes(
        user_id = current_user.id,
        post_id = post.id
      )
      db.session.add(new_like)
    else:
      db.session.delete(existing_like)
    db.session.commit()
    return redirect(url_for('books.home'))
  except Exception as e:
    flash(f"{str(e)}", "danger")
    return redirect(url_for('books.home'))

@posts.route("/comment/posts/<int:post_id>", methods=["POST", "GET"])
@login_required
def comment_post(post_id):
  post = Post.query.filter_by(unique_id=post_id).first()
  if not post:
    flash("Post not found", "danger")
    return redirect(url_for('books.home'))
  try:
    form = CommentForm()
    if form.validate_on_submit():
      new_comment = Comment(
        user_id = current_user.id,
        post_id = post.id,
        content = form.comment.data
      )
      db.session.add(new_comment)
      db.session.commit()
      flash("Comment posted successfully", "success")
      return redirect(url_for('posts.comment_post', post_id=post.unique_id))

    if form.errors != {}:
      for err_msg in form.errors.values():
        flash(f"{err_msg}", "danger")
        return redirect(url_for('posts.comment_post', post_id=post.unique_id))

    
  except Exception as e:
    flash(f"{str(e)}", "danger")
    return redirect(url_for('books.home'))

  context = {
    "form":form,
    "post": post
  }

  return render_template("Posts/comment-post.html", **context)
