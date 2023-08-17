from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id          = db.Column(db.Integer, primary_key=True)
    username    = db.Column(db.String, unique=True)
    passwort    = db.Column(db.String)
    points      = db.Column(db.Integer)

    games       = db.relationship("Game")

class Game(db.Model):
    __tablename__ = "game"
    id          = db.Column(db.Integer, primary_key=True)
    guesses     = db.Column(db.Integer)
    complete    = db.Column(db.Boolean)
    value       = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user    = db.relationship(User)
