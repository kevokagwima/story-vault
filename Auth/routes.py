from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from .form import RegistrationForm, LoginForm, ResetPasswordForm, ProfileForm
from models import db, Users, Role, ProfilePicture
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
  try:
    form = RegistrationForm()
    if form.validate_on_submit():
      new_user = Users(
        unique_id = random.randint(100000,999999),
        first_name = form.first_name.data,
        last_name = form.last_name.data,
        email = form.email_address.data,
        phone = form.phone_number.data,
        role = Role.query.filter_by(name="User").first().id
      )
      db.session.add(new_user)
      generated_password = generate_password()
      new_user.password = bcrypt.generate_password_hash(generated_password).decode("utf-8")
      db.session.commit()
      flash("Registration successfull", category="success")
      return redirect(url_for('auth.signin'))
    
    if form.errors != {}:
      for err_msg in form.errors.values():
        flash(f"{err_msg}", category="danger")
        return redirect(url_for('auth.signup'))

    return render_template("signup.html", form=form)

  except Exception as e:
    flash(f"{repr(e)}", category="danger")
    return redirect(url_for('auth.signup'))

def generate_password():
  characters = ["1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","!","@","#","$","%","^","&","*"]
  generated_password = ''.join(random.choice(characters) for _ in range(10))
  print(generated_password)
  return generated_password

@auth.route("/signin", methods=["POST", "GET"])
def signin():
  form = LoginForm()
  if form.validate_on_submit():
    user = Users.query.filter_by(email=form.email_address.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      login_user(user, remember=True)
      flash("Login successfull", category="success")
      next = request.args.get("next")
      if user.profile:
        return redirect(next or url_for("users.home"))
      else:
        return redirect(next or url_for("auth.profile", user_id=user.unique_id))
    elif user is None:
      flash("No user with that email", category="danger")
      return redirect(url_for('auth.signin'))
    else:
      flash("Invalid credentials", category="danger")
      return redirect(url_for('auth.signin'))

  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f"{err_msg}", category="danger")

  return render_template("signin.html", form=form)

@auth.route("/reset-password", methods=["POST", "GET"])
def reset_password():
  form = ResetPasswordForm()
  if form.validate_on_submit():
    user = Users.query.filter_by(email=form.email_address.data).first()
    if user:
      if user.check_password_correction(attempted_password=form.password.data):
        flash("New password cannot be same as old", category="danger")
      else:
        user.password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        db.session.commit()
        flash("Your password has been reset successfully", category="success")
        return redirect(url_for("users.signin"))
    else:
      flash("No user with that email", category="danger")
      return redirect(url_for('auth.reset_password'))

  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f"{err_msg}", category="danger")
      return redirect(url_for('auth.reset_password'))

  return render_template("reset-password.html", form=form)

@auth.route("/profile/<int:user_id>", methods=["POST", "GET"])
async def profile(user_id):
  form = ProfileForm()
  user = Users.query.filter_by(unique_id=user_id).first()
  if not user:
    flash("User not found", category="danger")
    return redirect(url_for('auth.signin'))
  if form.validate_on_submit():
    user.id_number = form.id_number.data
    file = request.files["profile_pic"]
    if file:
      asyncio.create_task(upload_file(user.id, file))
    return redirect(url_for('users.home'))

  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f"{err_msg}", category="danger")

  return render_template("profile.html", form=form, user=user)

async def upload_file(user_id, file):
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
      async with aiohttp.ClientSession() as session:
        async with session.put(f"s3://{bucket_name}/{file.filename}", data=file.read()) as response:
          if response.status == 200:
            flash("Profile Updated successfully", category="success")
          else:
            flash("Profile failed to upload", category="danger")
    except Exception as e:
      flash(f"{repr(e)}", category="danger")

@auth.route("/logout")
@login_required
def logout():
  logout_user()
  flash("Logout successfull", category="success")
  return redirect(url_for('auth.signin'))
