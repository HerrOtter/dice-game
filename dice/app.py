from typing import Optional

from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy.exc import IntegrityError

from .items import get_items
from .models import db, User
from .utils import get_current_user, is_authenticated

app = Flask("dice")

app.secret_key = 'SECRET_DICE'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dice.db"
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if not is_authenticated():
        print("NOT LOGGED IN")
        return render_template("auth.html")

    return {}

### API
# Todo put into its own file

@app.route("/api/login", methods=["POST"])
def api_login():
    if is_authenticated():
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


    user = db.session.execute(db.select(User).filter_by(username=username)).first()

    if not user or not user.User.check_password(password):
        return {
            "error": "invalid_credentials",
        }, 400

    user_entity = user.User

    session["user"] = user_entity.id

    return {
        "status": "login_success",
    }


@app.route("/api/register", methods=["POST"])
def api_register():
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

    user = User(username=request.form["username"])
    user.set_password(request.form["password"])
    print(user.password)

    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        return {
            "error": "username_exists",
        }, 400

    session["user"] = user.id

    return {
        "status": "register_success"
    }

@app.route("/api/logout", methods=["POST"])
def api_logout():
    try:
        del session["user"]
    except KeyError:
        pass
    return {
        "status": "logout_success"
    }

@app.route("/api/user", methods=["GET"])
def api_user():
    user = get_current_user()

    print(user)
    if not user:
        return {
            "error": "not_authenticated"
        }, 401

    return {
        "username": user.username,
        "points": user.points
    }

@app.route("/api/dice/guess", methods=["POST"])
def api_dice_guess():
    return {}

@app.route("/api/dice/info", defaults={"game_id": None}, methods=["POST"])
@app.route("/api/dice/info/<int:game_id>", methods=["POST"])
def api_dice_info(game_id: Optional[int]):
    return {}

@app.route("/api/dice/scoreboard", methods=["GET"])
def api_dice_scoreboard():
    return {}

@app.route("/api/shop/list", defaults={"item_id": None}, methods=["GET"])
@app.route("/api/shop/list/<int:item_id>", methods=["GET"])
def api_shop_list(item_id: Optional[int]):
    return {}

@app.route("/api/shop/buy/<int:item_id>", methods=["POST"])
def api_shop_buy(item_id: int):
    return {}
