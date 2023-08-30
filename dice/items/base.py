from abc import ABC
from typing import List

from flask_login import current_user
from sqlalchemy.exc import IntegrityError

from ..models import db, User, UserItems

class BaseItem(ABC):
    name: str
    description: str
    price: int
    requires: List["BaseItem"]
    enabled: bool = True

    def __init__(self):
        self.requires = []

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
