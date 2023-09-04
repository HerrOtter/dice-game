
from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user


main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    if not current_user.is_authenticated:
        return render_template("auth.html")

    return render_template("play.html")

@main.route("/shop", methods=["GET"])
def shop():
    if not current_user.is_authenticated:
        return redirect(url_for("frontend.main.index"))

    return render_template("shop.html")
