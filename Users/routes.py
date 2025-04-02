from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user
from models import ProfilePicture

users = Blueprint("users", __name__)

@users.route("/")
@users.route("/home")
def home():
  return render_template("index.html")

@users.route("/about")
def about():
  return render_template("about-us.html")
