from typing import Optional

from flask import session

from .models import db, User

def get_current_user() -> Optional[User]:
    """
    returns active user or None if not valid 
    """
    try:
        user_id = session["user"]
    except KeyError:
        return None

    user = db.session.get(User, user_id)
    return user

def is_authenticated() -> bool:
    """
    wrapper around `get_current_user` to check if user is valid
    """
    return get_current_user() is not None
