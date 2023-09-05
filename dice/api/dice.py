from typing import Optional

from flask import Blueprint, request
from flask_login import login_required, current_user
from sqlalchemy import desc

from ..models import db, User, Game
from ..game import current_game, new_game

dice = Blueprint("dice", __name__, url_prefix="/dice")

@dice.route("/guess", methods=["POST"])
@login_required
def api_dice_guess():
    active_game = current_game
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

    if guess < Game.MIN_VALUE or guess > Game.MAX_VALUE:
        return {
            "error": "invalid_guess",
            "message": "Invalid Guess"
        }, 400

    res = active_game.check_guess(guess)
    db.session.commit()

    if res == 0:
        return {
            "status": "dice_complete",
            "message": "Korrekt!"
        }
    elif res > 0:
        return {
            "status": "dice_too_large",
            "message": "Zu Groß!"
        }
    elif res < 0:
        return {
            "status": "dice_too_small",
            "message": "Zu Klein!"
        }

    return {
        "error": "invalid_dice"
    }, 400

@dice.route("/info", methods=["GET"])
@dice.route("/info/<int:game_id>", methods=["GET"])
@dice.route("/info/current", defaults={"current_game": True}, methods=["GET"])
@login_required
def api_dice_info(game_id: Optional[int] = None, current_game: bool = False):
    games = []
    if current_game:
        game_list = [current_game]
    elif not game_id:
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
        if game is None:
            continue
        elif not current_game and not game.complete:
            continue

        data = {
            "guesses": game.guesses,
            "id": game.id,
            "value": None
        }

        if game.complete:
            data["value"] = game.value,

        games.append(data)

    if game_id or current_game:
        try:
            return games[0]
        except IndexError:
            return {}

    return games

@dice.route("/scoreboard", methods=["GET"])
def api_dice_scoreboard():

    players = db.session.execute(
            db.select(User).order_by(desc(User.collected_points))
        ).all()

    print(players)

    current_position = None
    if current_user:
        try:
            current_position = players.index((current_user,))
        except ValueError:
            pass

    scoreboard = []
    for x in range(0, 5):
        try:
            user = players[x][0]
        except IndexError:
            user = None

        if not user:
            scoreboard.append(None)
            continue

        scoreboard.append({
            "username": user.username,
            "points": user.collected_points
        })

    return {
        "current_position": current_position+1,
        "scoreboard": scoreboard
    }

