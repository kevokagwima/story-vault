from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional

class BookForm(FlaskForm):
  title = StringField('Title', validators=[DataRequired()])
  author = StringField('Author', validators=[DataRequired()])
  cover_url = StringField('Cover URL', validators=[Optional()])
  description = TextAreaField('Description', validators=[Optional()])
  isbn = StringField('ISBN', validators=[Optional()])
  submit = SubmitField('Add Book')
