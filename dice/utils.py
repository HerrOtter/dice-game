from typing import Optional

from flask import session
from sqlalchemy.exc import IntegrityError

from .models import db, User, Game

def get_current_user_id() -> Optional[int]:
    try:
        return session["user"]
    except KeyError:
        return None

def get_current_user() -> Optional[User]:
    """
    returns active user or None if not valid 
    """
    user_id = get_current_user_id()
    if user_id is None:
        return None

    user = db.session.get(User, user_id)
    return user

def is_authenticated() -> bool:
    """
    wrapper around `get_current_user` to check if user is valid
    """
    return get_current_user() is not None


def get_active_game() -> Optional[Game]:
    user_id = get_current_user_id()
    if not user_id:
        return None

    active_game = db.session.execute(db.select(Game).filter_by(user_id=user_id, complete=0)).first()
    if not active_game:
        return None
    return active_game[0]

def new_game() -> Optional[Game]:
    user_id = get_current_user_id()
    if user_id is None:
        return None

    game = Game(user_id=user_id)
    game.generate_value()

    db.session.add(game)
    try:
        db.session.commit()
    except IntegrityError:
        return None

    return game
