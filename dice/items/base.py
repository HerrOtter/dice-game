from typing import Union, Optional, List

class BaseItem:
    name: str
    description: str
    price: int
    requires: List["BaseItem"]
    enabled: bool = True

    def __init__(self):
        self.requires = []
