from flask_login import LoginManager
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
