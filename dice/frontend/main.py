
from flask import Blueprint, render_template
from flask_login import current_user


main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    if not current_user.is_authenticated:
        return render_template("auth.html")

    return {}
