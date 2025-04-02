from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Role(db.Model):
  __tablename__ = "Roles"
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(10), nullable=False)
  user = db.relationship("Users", backref="user_role", lazy=True)

class Users(db.Model, UserMixin):
  __tablename__ = "Users"
  id = db.Column(db.Integer(), primary_key=True)
  unique_id = db.Column(db.Integer(), nullable=False)
  first_name = db.Column(db.String(50), nullable=False)
  last_name = db.Column(db.String(50), nullable=False)
  email = db.Column(db.String(100), nullable=False)
  phone = db.Column(db.String(10), nullable=False)
  id_number = db.Column(db.String(20))
  password = db.Column(db.String(100))
  role = db.Column(db.Integer(), db.ForeignKey('Roles.id'))
  profile = db.Column(db.Integer(), db.ForeignKey('Profile.id'))

class ProfilePicture(db.Model):
  __tablename__ = "Profile"
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(50))
  bucket = db.Column(db.String(50))
  region = db.Column(db.String(20))
  user = db.relationship("Users", backref="user_profile", lazy=True)
