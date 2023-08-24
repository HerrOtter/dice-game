from abc import ABC, abstractmethod
from typing import Union, Optional, List

from ..models import User, Game

class BaseItem(ABC):
    name: str
    description: str
    price: int
    requires: List["BaseItem"]
    enabled: bool = True

    def __init__(self):
        self.requires = []
