from abc import ABC
from typing import List

class BaseItem(ABC):
    name: str
    description: str
    price: int
    requires: List["BaseItem"]
    enabled: bool = True

    def __init__(self):
        self.requires = []
