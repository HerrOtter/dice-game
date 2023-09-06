from typing import Optional

from flask import Blueprint
from flask_login import login_required, current_user

from ..items import get_items, get_item

shop = Blueprint("shop", __name__, url_prefix="/shop")

@shop.route("/list", methods=["GET"])
@shop.route("/list/<id_name>", methods=["GET"])
@login_required
def list_items(id_name: Optional[str] = None):
    if id_name:
        item = get_item(id_name)
        if not item:
            return {
                "error": "item_not_found"
            }, 404

        all_items = {id_name: item}
    else:
        all_items = get_items()

    buyable_items = []

    for name, item in all_items.items():
        if (id_name or
            (item.purchasable(current_user) and
             not item.has_item(current_user))):
            buyable_items.append({
                "id_name": name,
                "name": item.get_name(),
                "description": item.get_description(),
                "price": item.price,
            })

    if id_name:
        return buyable_items[0]

    return buyable_items


@shop.route("/buy/<id_name>", methods=["POST"])
@login_required
def buy(id_name: str):
    item = get_item(id_name)
    if not item:
        return {
            "error": "item_not_found"
        }, 404

    if not item.buy(current_user):
        return {
            "error": "item_not_purchasable"
        }, 400

    return {
        "message": "item_bought"
    }
