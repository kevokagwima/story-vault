from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from random import randint
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

class BaseModel(db.Model):
  __abstract__ = True
  id = db.Column(db.Integer(), primary_key=True)
  unique_id = db.Column(db.Integer(), nullable=False)
  created_at = db.Column(db.DateTime())
  updated_at = db.Column(db.DateTime())

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.unique_id = randint(100000, 999999)
    self.created_at = datetime.now()

class Role(BaseModel, db.Model):
  __tablename__ = "role"
  name = db.Column(db.String(10), nullable=False)
  user = db.relationship("Users", backref="user_role", lazy=True)

class Users(BaseModel, db.Model, UserMixin):
  __tablename__ = "Users"
  username = db.Column(db.String(50), nullable=False)
  email = db.Column(db.String(100), nullable=False)
  phone = db.Column(db.String(10), nullable=False)
  password = db.Column(db.String(100))
  role = db.Column(db.Integer(), db.ForeignKey('role.id'))
  profile = db.Column(db.Integer(), db.ForeignKey('Profile.id'))
  posts = db.relationship("Post", backref="user_post", lazy=True)
  comment = db.relationship("Comment", backref="user_comment", lazy=True)
  user_book = db.relationship("UserBook", backref="user_book", lazy=True)

  @property
  def passwords(self):
    return self.passwords

  @passwords.setter
  def passwords(self, plain_text_password):
    self.password = bcrypt.generate_password_hash(plain_text_password).decode("utf-8")

  def check_password_correction(self, attempted_password):
    return bcrypt.check_password_hash(self.password, attempted_password)

class ProfilePicture(BaseModel, db.Model):
  __tablename__ = "Profile"
  name = db.Column(db.String(50))
  bucket = db.Column(db.String(50))
  region = db.Column(db.String(20))
  user = db.relationship("Users", backref="user_profile", lazy=True)

class Book(BaseModel, db.Model):
  __tablename__ = "Books"
  title = db.Column(db.String(200), nullable=False)
  author = db.Column(db.String(100), nullable=False)
  cover_url = db.Column(db.String(255))
  description = db.Column(db.Text)
  isbn = db.Column(db.String(20))
  posts = db.relationship("Post", backref="book", lazy=True)
  user_books = db.relationship("UserBook", backref="book", lazy=True)

class Post(BaseModel, db.Model):
  __tablename__ = "Posts"
  user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
  book_id = db.Column(db.Integer, db.ForeignKey('Books.id'))
  status = db.Column(db.String(50))
  book_title = db.Column(db.String(200))
  book_author = db.Column(db.String(200))
  content = db.Column(db.Text, nullable=False)
  likes = db.relationship("Likes", backref="post_likes", lazy=True)
  comments = db.relationship("Comment", backref="post_comments", lazy=True)

class Likes(BaseModel, db.Model):
  __tablename__ = "likes"
  user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
  post_id = db.Column(db.Integer, db.ForeignKey('Posts.id'), nullable=False)

class Comment(BaseModel, db.Model):
  __tablename__ = "Comments"
  user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
  post_id = db.Column(db.Integer, db.ForeignKey('Posts.id'), nullable=False)
  content = db.Column(db.Text, nullable=False)

class Follow(BaseModel, db.Model):
  __tablename__ = "Follows"
  follower_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
  followed_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)

class UserBook(BaseModel, db.Model):
  __tablename__ = "UserBooks"
  user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
  book_id = db.Column(db.Integer, db.ForeignKey('Books.id'), nullable=False)
  status = db.Column(db.String(20), nullable=False)
  rating = db.Column(db.Integer)
