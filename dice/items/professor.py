from flask import url_for

from .base import BaseItem

class professor(BaseItem):
    price = 1000
    asset_small = "footage/professor_150x150.webp"
    asset_big = "footage/professor_600x400.webp"
