from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from .form import RegistrationForm, LoginForm, ResetPasswordForm, ProfileForm
from models import db, Users, Role, ProfilePicture, Follow
import random, boto3, os, asyncio, aiohttp

auth = Blueprint("auth", __name__, url_prefix="/auth")
bcrypt = Bcrypt()

s3 = boto3.resource(
  "s3",
  aws_access_key_id = os.environ.get("aws_access_key"),
  aws_secret_access_key = os.environ.get("aws_secret_key")
)
client = boto3.client(
  "s3",
  aws_access_key_id = os.environ.get("aws_access_key"),
  aws_secret_access_key = os.environ.get("aws_secret_key")
)
bucket_name = os.environ.get("bucket_name")
region = os.environ.get("region")

@auth.route("/signup", methods=["POST", "GET"])
def signup():
  form = RegistrationForm()
  if form.validate_on_submit():
    try:
      new_user = Users(
        username = form.username.data,
        email = form.email_address.data,
        phone = form.phone_number.data,
        role = Role.query.filter_by(name="User").first().id,
        passwords = form.password.data
      )
      db.session.add(new_user)
      db.session.commit()
      flash("Registration successfull", "success")
      return redirect(url_for('auth.signin'))
    
    except Exception as e:
      flash(f"{str(e)}", "danger")
      return redirect(url_for('auth.signup'))

    if form.errors != {}:
      for err_msg in form.errors.values():
        flash(f"{err_msg}", "danger")
        return redirect(url_for('auth.signup'))

  return render_template("Auth/signup.html", form=form)

@auth.route("/signin", methods=["POST", "GET"])
def signin():
  form = LoginForm()
  if form.validate_on_submit():
    try:
      user = Users.query.filter_by(email=form.email_address.data).first()
      if user and bcrypt.check_password_hash(user.password, form.password.data):
        login_user(user, remember=True)
        flash("Login successfull", "success")
        next = request.args.get("next")
        return redirect(next or url_for("books.home"))
      elif user is None:
        flash("No user with that email", "danger")
        return redirect(url_for('auth.signin'))
      else:
        flash("Invalid credentials", "danger")
        return redirect(url_for('auth.signin'))
    except Exception as e:
      flash(f"{str(e)}", "danger")
      return redirect(url_for('auth.signin'))

  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f"{err_msg}", "danger")

  return render_template("Auth/signin.html", form=form)

@auth.route("/reset-password", methods=["POST", "GET"])
def reset_password():
  form = ResetPasswordForm()
  if form.validate_on_submit():
    user = Users.query.filter_by(email=form.email_address.data).first()
    if user:
      if user.check_password_correction(attempted_password=form.password.data):
        flash("New password cannot be same as old", "danger")
      else:
        user.password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        db.session.commit()
        flash("Your password has been reset successfully", "success")
        return redirect(url_for("users.signin"))
    else:
      flash("No user with that email", "danger")
      return redirect(url_for('auth.reset_password'))

  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f"{err_msg}", "danger")
      return redirect(url_for('auth.reset_password'))

  return render_template("reset-password.html", form=form)

@auth.route("/profile/<string:username>", methods=["POST", "GET"])
def profile(username):
  form = ProfileForm()
  user = Users.query.filter_by(username=username).first()
  if not user:
    flash("User not found", "danger")
    return redirect(url_for('auth.signin'))
  if form.validate_on_submit():
    user.id_number = form.id_number.data
    file = request.files["profile_pic"]
    if file:
      upload_file(user.id, file)
    return redirect(url_for('users.home'))

  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f"{err_msg}", "danger")

  context = {
    "form": form,
    "user": user,
    "followers": Follow.query.filter_by(followed_id=user.id).all(),
    "following": Follow.query.filter_by(follower_id=user.id).all()
  }

  return render_template("Auth/profile.html", **context)

def upload_file(user_id, file):
  if file:
    user = Users.query.get(user_id)
    existing_profile_pic = ProfilePicture.query.filter_by(id=user.profile).first()
    if not existing_profile_pic:
      profile_pic = ProfilePicture(
        name = file.filename,
        bucket = bucket_name,
        region = region,
      )
      db.session.add(profile_pic)
    else:
      existing_profile_pic.name = file.filename
    user.profile = ProfilePicture.query.filter_by(name=file.filename).first().id
    db.session.commit()
    try:
      flash("Profile Updated successfully", "success")
    except Exception as e:
      flash(f"{repr(e)}", "danger")

@auth.route("/logout")
@login_required
def logout():
  logout_user()
  flash("Logout successfull", "success")
  return redirect(url_for('auth.signin'))
