from typing import Optional

from flask import Flask, render_template, request
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, logout_user, login_required, current_user

from .admin import admin
from .auth import login_manager
from .models import db, User, Game
from .utils import get_active_game, new_game

# Flask
app = Flask("dice")
app.url_map.strict_slashes = False

# Flask-SQLalchemy
app.secret_key = 'SECRET_DICE'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dice.db"
db.init_app(app)

# Flask-Admin
# https://bootswatch.com/3/
app.config['FLASK_ADMIN_SWATCH'] = 'yeti'
admin.init_app(app)

# Flask-Login
login_manager.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if not current_user.is_authenticated:
        return render_template("auth.html")

    return {}

### API
# Todo put into its own file

@app.route("/api/login", methods=["POST"])
def api_login():
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


    users = db.session.execute(
            db.select(User).filter_by(username=username)
        ).first()

    if not users or not users[0].check_password(password):
        return {
            "error": "invalid_credentials",
        }, 400

    user = users[0]
    login_user(user)
    app.logger.info(f"{user.username} logged in successfully")

    return {
        "status": "login_success",
    }


@app.route("/api/register", methods=["POST"])
def api_register():
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

    app.logger.info('%s registered as a new account', user.username)
    login_user(user)

    return {
        "status": "register_success"
    }

@app.route("/api/logout", methods=["POST"])
def api_logout():
    logout_user()
    return {
        "status": "logout_success"
    }

@app.route("/api/user", methods=["GET"])
@login_required
def api_user():
    return {
        "username": current_user.username,
        "points": current_user.points
    }

@app.route("/api/dice/guess", methods=["POST"])
@login_required
def api_dice_guess():
    active_game = get_active_game()
    if not active_game:
        active_game = new_game()
        if not active_game:
            return {
                "error": "no_dice"
            }, 400

    try:
        guess = int(request.form["guess"])
    except KeyError:
        return {
            "error": "form_missing_field_guess"
        }, 400
    except ValueError:
        return {
            "error": "form_bad_field_guess"
        }, 400

    if guess < 0 or guess > 100:
        return {
            "error": "invalid_guess"
        }, 400

    res = active_game.check_guess(guess)
    db.session.commit()

    if res == 0:
        return {
            "message": "dice_complete"
        }
    elif res > 0:
        return {
            "message": "dice_too_large"
        }
    elif res < 0:
        return {
            "message": "dice_too_small"
        }

    return {
        "error": "invalid_dice"
    }, 400

@app.route("/api/dice/info", defaults={"game_id": None}, methods=["GET"])
@app.route("/api/dice/info/<int:game_id>", methods=["GET"])
@login_required
def api_dice_info(game_id: Optional[int]):
    games = []
    if not game_id:
        game_list = current_user.games
    else:
        specific_game = db.session.get(Game, game_id)
        if (not specific_game or
            specific_game.user != current_user or
            not specific_game.complete):
            return {
                "error": "not_found"
            }, 404
        game_list = [specific_game]


    for game in game_list:
        if not game.complete:
            continue

        games.append({
            "id": game.id,
            "guesses": game.guesses,
            "value": game.value,
        })

    if game_id:
        return games[0]
    return games

@app.route("/api/dice/scoreboard", methods=["GET"])
def api_dice_scoreboard():
    return {}

@app.route("/api/shop/list", defaults={"item_id": None}, methods=["GET"])
@app.route("/api/shop/list/<int:item_id>", methods=["GET"])
@login_required
def api_shop_list(item_id: Optional[int]):
    return {}

@app.route("/api/shop/buy/<int:item_id>", methods=["POST"])
@login_required
def api_shop_buy(item_id: int):
    return {}
