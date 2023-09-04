from typing import List

from flask_sqlalchemy import SQLAlchemy
from flask_login.mixins import UserMixin
from random import randint 
import hmac

db = SQLAlchemy()

COMPLETED_POINTS = 25

HASH_FUNCTIONS = [
    # hmac_sha256 with username salt
    lambda pw, salt: hmac.new(
        key=salt.encode("utf-8"),
        msg=pw.encode("utf-8"),
        digestmod="sha256",
    ).hexdigest(),

    # hmac_sha3_512 with username and a static msg
    lambda pw, salt: hmac.new(
        key=salt.encode("utf-8"),
        msg="SALT_KEY".encode("utf-8"),
        digestmod="sha3_512",
    ).hexdigest(),

    # hmac_sha3_512 with username and a static msg
    lambda pw, salt: hmac.new(
        key="SECRET_SALT_KEY".encode("utf-8"),
        msg=pw.encode("utf-8"),
        digestmod="sha3_512",
    ).hexdigest(),
]
DEFAULT_HASH_INDEX = 2

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    hash_type = db.Column(db.Integer, nullable=False)
    lang = db.Column(db.String, nullable=True)

    collected_points = db.Column(db.Integer, default=0, nullable=False)
    points = db.Column(db.Integer, default=0, nullable=False)

    admin = db.Column(db.Boolean, default=False, nullable=False)

    games = db.relationship("Game", viewonly=True)
    items = db.relationship("UserItems", viewonly=True)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.username}({self.id})>"

    def __int__(self) -> int:
        return self.id

    def __str__(self) -> str:
        return self.username

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

    def get_items(self) -> List[str]:
        return [x.item_name for x in self.items]

    def add_points(self, points: int) -> int:
        self.points += points
        self.collected_points += points

        return self.points

    def remove_points(self, points: int) -> int:
        self.points -= points
        if self.points < 0:
            self.points = 0

        return self.points 

class UserItems(db.Model):
    __tablename__ = "user_items"
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    user = db.relationship(User)
    item_name = db.Column(db.String, primary_key=True)

class Game(db.Model):
    MIN_VALUE= 0
    MAX_VALUE = 100

    __tablename__ = "game"
    id = db.Column(db.Integer, primary_key=True)
    guesses = db.Column(db.Integer, default=0, nullable=False)
    value = db.Column(db.Integer, nullable=False)
    complete = db.Column(db.Boolean, default=False, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship(User)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.id}>"

    def generate_value(self):
        """
        Generates a value between the given a constant min and max value
        specified in the project description
        """
        self.value = randint(self.MIN_VALUE, self.MAX_VALUE)

    def check_guess(self, guess: int) -> int:
        """
        Returns:

        - 1 when guess is too big
        - 0 when guess is correct
        - 1 when guess is too small

        Invalid guesses do not increment the guess counter
        """
        if self.complete:
            return 0
        elif guess < self.MIN_VALUE:
            return -1
        elif guess > self.MAX_VALUE:
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
