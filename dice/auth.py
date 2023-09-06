from flask_login import LoginManager, current_user
from .models import db, User

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    users = db.session.execute(
            db.select(User).filter_by(id=user_id)
        ).first()

    if not users:
        return None
    return users[0]

# This cannot be merged into the User model because of anonymous users
def is_admin() -> bool:
    if not current_user.is_authenticated:
        return False

    return current_user.admin
