from flask import Flask, flash, abort
from flask_login import login_manager, LoginManager
from flask_migrate import Migrate
from Posts.routes import posts
from Books.routes import books
from Auth.routes import auth
from Errors.handlers import errors
from models import db, Users
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(posts)
app.register_blueprint(books)
app.register_blueprint(auth)
app.register_blueprint(errors)
login_manager = LoginManager()
login_manager.blueprint_login_views = {
  'posts': '/auth/signin'
}
login_manager.login_message = "Please login to access this page"
login_manager.login_message_category = "danger"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
  try:
    return Users.query.filter_by(unique_id=user_id).first()
  except:
    flash("Unable to load user", category="danger")
    abort(500)

if __name__ == "__main__":
  app.run(debug=True)
