from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SelectField
from flask_wtf.file import FileAllowed, FileRequired
from wtforms.validators import DataRequired, Optional

class PostForm(FlaskForm):
  status = SelectField(label="What would you like to share?", choices=[("", "-- Select an option"), ("finished", "Finished Reading"), ("current", "Currently Reading"), ("start", "Planning to read")], validators=[DataRequired()])
  book_title = StringField(label="Book Title", validators=[DataRequired(message="Book title field is required")])
  book_author = StringField(label="Book Author", validators=[DataRequired(message="Book author field is required")])
  book_cover = FileField(label="Book Cover (Optional)", validators=[Optional()])
  comments = TextAreaField(label="Caption", validators=[DataRequired(message="Book author field is required")])
