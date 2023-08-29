from flask_sqlalchemy import SQLAlchemy
from flask_login.mixins import UserMixin
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

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    hash_type = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, default=0, nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)

    games = db.relationship("Game", viewonly=True)
    items = db.relationship("UserItems", viewonly=True)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.username}>"

    def hash_password(self, password: str) -> str:
        if self.hash_type is None:
            self.hash_type = DEFAULT_HASH_INDEX

        return HASH_FUNCTIONS[self.hash_type](password, self.username)

    def set_password(self, password: str, upgrade: bool = True):
        if upgrade:
            self.hash_type = DEFAULT_HASH_INDEX
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
    guesses = db.Column(db.Integer, default=0, nullable=False)
    complete = db.Column(db.Boolean, default=False, nullable=False)
    value = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship(User)

    def generate_value(self):
        self.value = randint(0, 100)

    def check_guess(self, guess: int) -> int:
        """
        Returns:
          1 when guess is too big
          0 when guess is correct
         -1 when guess is too small

        Invalid guesses are not counted
        """
        if self.complete:
            return 0
        elif guess < 0:
            return -1
        elif guess > 100:
            return 1

        self.guesses += 1
        if self.value == guess:
            self.complete = True
            self.user.add_points(COMPLETED_POINTS)
            return 0
        elif self.value < guess:
            return 1
        elif self.value > guess:
            return -1
