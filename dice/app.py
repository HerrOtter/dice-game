from typing import Optional

from flask import Flask, render_template, request, redirect, url_for

from .items import get_items
from .models import db

app = Flask("dice")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dice.db"
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        return redirect(url_for("register"))

    return render_template("index.html")

@app.route("/register", methods=["GET" , "POST"])
def register():

    return render_template("register.html")


### API
# Todo put into its own file

@app.route("/api/login", methods=["POST"])
def api_login():
    print("api_login")
    return {}

@app.route("/api/register", methods=["POST"])
def api_register():
    return {}

@app.route("/api/user", methods=["GET"])
def api_user():
    return {}

@app.route("/api/dice/guess", methods=["POST"])
def api_dice_guess():
    return {}

@app.route("/api/dice/info", defaults={"game_id": None}, methods=["POST"])
@app.route("/api/dice/info/<int:game_id>", methods=["POST"])
def api_dice_info(game_id: Optional[int]):
    return {}

@app.route("/api/dice/scoreboard", methods=["GET"])
def api_dice_scoreboard():
    return {}

@app.route("/api/shop/list", defaults={"item_id": None}, methods=["GET"])
@app.route("/api/shop/list/<int:item_id>", methods=["GET"])
def api_shop_list(item_id: Optional[int]):
    return {}

@app.route("/api/shop/buy/<int:item_id>", methods=["POST"])
def api_shop_buy(item_id: int):
    return {}
