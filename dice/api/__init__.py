from flask import Blueprint

from .auth import auth
from .dice import dice
from .shop import shop

api = Blueprint("api", __name__, url_prefix="/api")

api.register_blueprint(auth)
api.register_blueprint(dice)
api.register_blueprint(shop)
