from flask import url_for

from .base import BaseItem

class dice(BaseItem):
    price = 100
    asset_small = "footage/dice_150x150.webp"
    asset_big = "footage/dice_600x400.webp"
