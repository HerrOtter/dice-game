from typing import Optional

from flask import Blueprint, request
from flask_login import login_required, current_user

from ..models import db, Game
from ..utils import get_active_game, new_game

dice = Blueprint("dice", __name__, url_prefix="/dice")

@dice.route("/guess", methods=["POST"])
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
            "message": "Correct!"
        }
    elif res > 0:
        return {
            "status": "dice_too_large",
            "message": "Too large!"
        }
    elif res < 0:
        return {
            "status": "dice_too_small",
            "message": "Too small!"
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
        game_list = [get_active_game()]
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
    return {}

