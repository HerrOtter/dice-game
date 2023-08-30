from abc import ABC
from typing import List

from ..models import User

class BaseItem(ABC):
    name: str
    description: str
    price: int
    requires: List["BaseItem"]
    enabled: bool = True

    def __init__(self):
        self.requires = []

    def purchasable(self, user: User) -> bool:
        if not self.enabled:
            return False

        if user.points < self.price:
            return False

        # TODO check required items

        return True
