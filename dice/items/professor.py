from math import ceil, floor


from .base import BaseItem
from ..models import Game

# TODO
# currently the professor by simply adding / substracting
# half the difference between the last guess and the value.
# To correctly implement this we need a guess history

class professor(BaseItem):
    price = 1000
    asset_small = "footage/professor_150x150.webp"
    asset_big = "footage/professor_600x400.webp"

    def use_item(self, game):
        if not game or not game.last_guess:
            return floor((Game.MAX_VALUE - Game.MIN_VALUE) / 2)

        guess_offset = (game.value - game.last_guess) / 2
        if guess_offset < 0:
            guess_offset = floor(guess_offset)
        else:
            guess_offset = ceil(guess_offset)
        new_guess = game.last_guess + guess_offset

        return new_guess
