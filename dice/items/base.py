from abc import ABC
from typing import List, Optional

from flask_login import current_user
from sqlalchemy.exc import IntegrityError

from ..models import db, User, Game, UserItems
from ..i18n import translate

class BaseItem(ABC):
    price: int
    requires: List["BaseItem"]
    enabled: bool = True

    asset_small: Optional[str] = None
    asset_big: Optional[str] = None

    def __init__(self):
        self.requires = []

    def use_item(self, game: Game) -> Optional[int]:
        return None

    def has_item(self, user: User) -> bool:
        item_name = self.__class__.__name__
        item_entry = db.session.execute(
            db.select(UserItems).filter_by(user=current_user, item_name=item_name)
        ).first()

        return bool(item_entry)

    def buy(self, user: User) -> bool:
        if not self.purchasable(user):
            # We are missing something for missing this item
            return False
        elif self.has_item(user):
            # We already own it, so pretend we bought it
            return True

        item_name = self.__class__.__name__
        user.remove_points(self.price)

        item_entry = UserItems(
            user=current_user,
            item_name=item_name
        )

        db.session.add(item_entry)
        try:
            db.session.commit()
        except IntegrityError:
            return False

        return True

    def purchasable(self, user: User) -> bool:
        if not self.enabled:
            return False

        if user.points < self.price:
            return False

        # TODO check required items

        return True

    def get_name(self) -> str:
        return translate(f"shop.item.{self.__class__.__name__}.name")

    def get_description(self) -> str:
        return translate(f"shop.item.{self.__class__.__name__}.description")
