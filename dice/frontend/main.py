from typing import Optional

from flask import Blueprint, render_template
from flask_login import login_required, current_user

from ..items import get_items, get_item

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    if not current_user.is_authenticated:
        return render_template("auth.html")

    return {}
