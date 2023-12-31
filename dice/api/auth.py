from flask import Blueprint, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError

from ..models import db, User
from ..i18n import set_current_lang, get_current_lang

auth = Blueprint("auth", __name__, url_prefix="/auth")

@auth.route("/login", methods=["POST"])
def login():
    if current_user.is_authenticated:
        # We are already authenticated, what are we doing?
        return {
            "status": "login_success",
        }, 200


    try:
        username = request.form["username"]
    except KeyError:
        return {
            "error": "form_missing_field_username",
        }, 400

    try:
        password = request.form["password"]
    except KeyError:
        return {
            "error": "form_missing_field_password",
        }, 400

    if (len(username) < 3):
        return {
            "error": "username"
        }, 400

    users = db.session.execute(
            db.select(User).filter_by(username=username)
        ).first()

    if not users:
        return {
            "error": "invalid_user",
            "message": "Invalider Nutzer",
        }, 404

    if not users[0].check_password(password):
        return {
            "error": "invalid_credentials",
            "message": "Invalide Credentials"
        }, 400

    user = users[0]
    login_user(user)
    current_app.logger.info(f"{user.username} logged in successfully")

    return {
        "status": "login_success",
    }


@auth.route("/register", methods=["POST"])
def register():
    if current_user.is_authenticated:
        # We are logged in, why register again?
        return {
            "error": "logged_in",
        }, 404

    try:
        username = request.form["username"]
    except KeyError:
        return {
            "error": "form_missing_field_username",
        }, 400

    try:
        password = request.form["password"]
    except KeyError:
        return {
            "error": "form_missing_field_password",
        }, 400

    user = User(username=username)
    user.set_password(password)

    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        return {
            "error": "username_exists",
        }, 400

    current_app.logger.info('%s registered as a new account', user.username)
    login_user(user)

    return {
        "status": "register_success"
    }

@auth.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return {
        "status": "logout_success"
    }

@auth.route("/user", methods=["GET"])
@login_required
def user():
    inventory = []
    for item in current_user.get_items():
        inventory.append(item)

    return {
        "username": current_user.username,
        "points": current_user.points,
        "lang": get_current_lang(),
        "inventory": inventory
    }

@auth.route("/change_language", methods=["POST"])
@login_required
def change_language():
    try:
        language = request.form["language"]
    except KeyError:
        return {
            "error": "form_missing_field_language",
        }, 400

    set_current_lang(language)

    return ""