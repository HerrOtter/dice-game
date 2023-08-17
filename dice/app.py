from flask import Flask

from .models import db

app = Flask("dice")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dice.db"
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def hello_world():
    return 'Hello, World!'


