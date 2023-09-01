from flask_login import current_user

def is_admin() -> bool:
    if not current_user.is_authenticated:
        return False

    return current_user.admin

