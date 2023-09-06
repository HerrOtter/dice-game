"""
i18n submodule

Basic i18n submodule that recursively looks up translations via keys
"""
import glob
from pathlib import Path
from os.path import dirname, join
import json

from werkzeug.local import LocalProxy
from flask_login import current_user

from ..models import db

DEFAULT_LANG = "de"

__TRANSLATIONS__ = {}

def load_translations():
    __TRANSLATIONS__.clear()

    files = glob.glob(join(dirname(__file__), "*.json"))
    for file in files:
        filepath = Path(file)
        handle = open(file, "r")
        data = json.load(handle)
        __TRANSLATIONS__[filepath.stem] = data

def translate(key: str, lang: str = None) -> str:
    keys = key.split(".")

    if not lang:
        lang = get_current_lang()

    try:
        entry = __TRANSLATIONS__[lang]

        for key_part in keys:
            entry = entry[key_part]

        return entry
    except KeyError:
        return f"#{key}"

def set_current_lang(lang: str):
    if current_user and hasattr(current_user, "lang"):
        current_user.lang = lang
        db.session.commit()

def get_current_lang() -> str:
    lang = None
    if hasattr(current_user, "lang"):
        lang = current_user.lang
    if not lang:
        lang = DEFAULT_LANG

    return lang

current_lang = LocalProxy(lambda: get_current_lang())

def i18n_context_processor():
    return dict(
        t=translate,
        current_lang=get_current_lang()
    )

class i18n_manager:
    @classmethod
    def init_app(cls, app):
        load_translations()
        app.context_processor(i18n_context_processor)
