from flask import Flask
from models import db, Role
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def add_tables():
  db.create_all()

def drop_tables():
  db.drop_all()

def add_role():
  roles = ["Admin", "User"]
  for role in roles:
    new_role = Role(
      name=role
    )
    db.session.add(new_role)
    db.session.commit()
    print(f"Added role {new_role.name}")

if __name__ == '__main__':
  with app.app_context():
    drop_tables()
    add_tables()
    add_role()
  