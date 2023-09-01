from typing import Optional

from flask_login import current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.local import LocalProxy

from .models import db, Game

def get_active_game() -> Optional[Game]:
    """
    Gets the first active game for the current user
    """
    if not current_user.is_authenticated:
        return None

    active_game = db.session.execute(
            db.select(Game).filter_by(user=current_user, complete=0)
        ).first()
    if not active_game:
        return None
    return active_game[0]

current_game = LocalProxy(lambda: get_active_game())

def new_game() -> Optional[Game]:
    """
    Attempts to create a new game for the current user
    """
    if not current_user.is_authenticated:
        return None

    game = Game(user=current_user)
    game.generate_value()

    db.session.add(game)
    try:
        db.session.commit()
    except IntegrityError:
        return None

    return game

def _game_context_processor():
    return dict(current_game=get_active_game())

