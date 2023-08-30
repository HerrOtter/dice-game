from typing import Optional

from flask import Blueprint
from flask_login import login_required, current_user

from ..items import get_items, get_item

shop = Blueprint("shop", __name__, url_prefix="/shop")

@shop.route("/list", defaults={"id_name": None}, methods=["GET"])
@shop.route("/list/<id_name>", methods=["GET"])
@login_required
def api_shop_list(id_name: Optional[str]):
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
        print(item.purchasable(current_user))
        if item.purchasable(current_user):
            buyable_items.append({
                "id_name": name,
                "name": item.name,
                "description": item.description,
                "price": item.price,
            })

    if id_name:
        return buyable_items[0]

    return buyable_items


@shop.route("/api/shop/buy/<int:item_id>", methods=["POST"])
@login_required
def api_shop_buy(item_id: int):
    return {}
