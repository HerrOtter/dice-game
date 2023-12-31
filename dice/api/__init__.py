"""
API submodules

This module includes all relevant code for the REST API

Reference the openapi specification for routes
"""

from flask import Blueprint

from .auth import auth
from .dice import dice
from .shop import shop

api = Blueprint("api", __name__, url_prefix="/api")

api.register_blueprint(auth)
api.register_blueprint(dice)
api.register_blueprint(shop)
