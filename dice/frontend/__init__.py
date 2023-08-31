"""
Frontend submodule

freestanding flask frontend
"""

from flask import Blueprint

from .main import main

frontend = Blueprint("frontend", __name__,
    template_folder="templates",
    static_folder="static"
)

frontend.register_blueprint(main)
