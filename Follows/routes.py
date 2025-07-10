from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from models import db, Follow, Users

follows = Blueprint("follows", __name__)

@follows.route("/follow/<string:username>")
@login_required
def follow(username):
  user = Users.query.filter_by(username=username).first()
  if not user:
    flash("User not found", "danger")
    return redirect(url_for("books.home"))

  try:
    existing_follow = Follow.query.filter_by(follower_id=current_user.id, followed_id=user.id).first()
    if not existing_follow:
      new_follow = Follow(
        follower_id = current_user.id,
        followed_id = user.id
      )
      db.session.add(new_follow)
    else:
      db.session.delete(existing_follow)
    db.session.commit()
    return redirect(request.referrer)
  except Exception as e:
    flash(f"{str(e)}", "danger")
    return redirect(url_for("books.home"))
