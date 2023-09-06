"""
Frontend submodule

Contains all the logic for the frontend to function
"""

from flask import Blueprint

from .main import main

frontend = Blueprint("frontend", __name__,
    template_folder="templates",
    static_folder="static"
)

frontend.register_blueprint(main)
