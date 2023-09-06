from random import randint

from flask import url_for

from .base import BaseItem
from ..models import Game
class dice(BaseItem):
    price = 100
    asset_small = "footage/dice_150x150.webp"
    asset_big = "footage/dice_600x400.webp"

    def use_item(self, game):
        return randint(Game.MIN_VALUE, Game.MAX_VALUE)
