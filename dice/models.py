from flask_sqlalchemy import SQLAlchemy
from random import randint 
import hmac

db = SQLAlchemy()

COMPLETED_POINTS = 25

HASH_FUNCTIONS = [
    lambda pw, salt: hmac.new(
        key=salt.encode("utf-8"),
        msg=pw.encode("utf-8"),
        digestmod="sha256",
    ).hexdigest(),
]
DEFAULT_HASH_INDEX = 0

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    passwort = db.Column(db.String)
    hash_type = db.Column(db.Integer)
    points = db.Column(db.Integer)

    games = db.relationship("Game")
    items = db.relationship("UserItems")

    def hash_password(self, password: str) -> str:
        if self.hash_type is None:
            self.hash_type = DEFAULT_HASH

        return HASH_FUNCTIONS[self.hash_type](password, self.username)

    def set_password(self, password: str, upgrade: bool = True):
        if upgrade:
            self.hash_type = DEFAULT_HASH
        self.password = self.hash_password(password)

    def check_password(self, password: str) -> bool:
        return self.hash_password(password) == self.password

    def add_points(self, points: int) -> int:
        self.points += points
        return self.points

class UserItems(db.Model):
    __tablename__ = "user_items"
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    item_name = db.Column(db.String, primary_key=True)

class Game(db.Model):
    __tablename__ = "game"
    id = db.Column(db.Integer, primary_key=True)
    guesses = db.Column(db.Integer)
    complete = db.Column(db.Boolean)
    value = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship(User)

    def generate_value(self):
        self.value = randint(0, 100)

    def check_guess(self, guess: int) -> bool:
        if self.complete:
            return False

        if guess < 0 or guess > 100:
            return False

        self.guesses += 1
        if self.value == guess:
            self.complete = True
            self.user.add_points(COMPLETED_POINTS)
