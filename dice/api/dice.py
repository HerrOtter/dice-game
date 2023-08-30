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

@dice.route("/info", defaults={"game_id": None}, methods=["GET"])
@dice.route("/info/<int:game_id>", methods=["GET"])
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

@dice.route("/scoreboard", methods=["GET"])
def api_dice_scoreboard():
    return {}

