from math import ceil, floor

from flask import url_for

from .base import BaseItem

class professor(BaseItem):
    price = 1000
    asset_small = "footage/professor_150x150.webp"
    asset_big = "footage/professor_600x400.webp"

    def use_item(self, game):
        guess_offset = (game.value - game.last_guess) / 2
        if guess_offset < 0:
            guess_offset = floor(guess_offset)
        else:
            guess_offset = ceil(guess_offset)
        new_guess = game.last_guess + guess_offset

        return new_guess
