"""
Items submodule

Defines all items and helper methods to load and query those
"""

from typing import Dict, Optional
from pathlib import Path
from os.path import dirname, join
import glob
from importlib import import_module

from .base import BaseItem
__ITEMS__ = {}

def import_items() -> int:
    files = glob.glob(join(dirname(__file__), "*.py"))
    for file in files:
        filepath = Path(file)
        if filepath.name in ["base.py", "__init__.py"]:
            continue

        module_name = f"dice.items.{filepath.stem}"
        import_module(module_name)

    __ITEMS__.clear()

    for cls in BaseItem.__subclasses__():
        if not cls.enabled:
            continue

        if cls.__name__ in __ITEMS__:
            raise Exception(f"Item {cls.name} has a duplicate entry")

        __ITEMS__[cls.__name__] = cls()

    return len(__ITEMS__)

def get_item(name: str) -> Optional[BaseItem]:
    return __ITEMS__.get(name)

def get_items() -> Dict[str, BaseItem]: 
    return __ITEMS__
