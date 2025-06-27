from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, FileField
from flask_wtf.file import FileAllowed, FileRequired
from wtforms.validators import Length, EqualTo, DataRequired, ValidationError, Email
from models import Users

class RegistrationForm(FlaskForm):
  username = StringField(label="Username", validators=[DataRequired(message="Username field is required")])
  phone_number = StringField(label="Phone Number", validators=[Length(min=0, max=10, message="Invalid Phone Number"), DataRequired(message="Phone number required")])
  email_address = EmailField(label="Email Address", validators=[Email(), DataRequired(message="Email Address field is required")])
  password = PasswordField(label="Password", validators=[Length(min=5,message="Password has to be between 5 and 25 characters long",), DataRequired(message="Password field required")])
  confirm_password = PasswordField(label="Confirm Password", validators=[EqualTo("password",message="Passwords do not match"), DataRequired(message="Confirm Password field required")])

  def validate_phone_number(self, phone_number_to_validate):
    phone_number = phone_number_to_validate.data
    if phone_number:
      if phone_number[0] != str(0):
        raise ValidationError("Invalid phone number. Phone number must begin with 0")
      elif phone_number[1] != str(7) and phone_number[1] != str(1):
        raise ValidationError("Invalid phone number. Phone number must begin with 0 followed by 7 or 1")
      elif Users.query.filter_by(phone=phone_number_to_validate.data).first():
        raise ValidationError("Phone Number already exists, Please try another one")

  def validate_email_address(self, email_to_validate):
    email = Users.query.filter_by(email=email_to_validate.data).first()
    if email:
      raise ValidationError("Email Address already exists, Please try another one")

class LoginForm(FlaskForm):
  email_address = EmailField(label="Email Address", validators=[DataRequired(message="Email Address field is required")])
  password = PasswordField(label="Password", validators=[DataRequired(message="Password field is required")])

class ResetPasswordForm(FlaskForm):
  email_address = EmailField(label="Email Address", validators=[DataRequired(message="Email Address field is required")])
  password = PasswordField(label="Password", validators=[DataRequired(message="Password field is required")])
  password1 = PasswordField(label="Confirm Password", validators=[EqualTo("password", message="Passwords do not match"), DataRequired(message="Confirm password field is required")])

  def validate_password(form, field):
    special_characters = "!@#$%^&*()_+"
    password = field.data
    if not any(char in special_characters for char in password):
      raise ValidationError("Password must contain at least one special character")

class ProfileForm(FlaskForm):
  id_number = StringField(label="ID Number", validators=[DataRequired(message="ID Number field required")])
  profile_pic = FileField(label="Upload Assignment", validators=[DataRequired(message="Please upload a file"), FileAllowed(['png', 'jpg', 'jpeg', 'txt',], 'Only png, jpg and jpeg files allowed')])
