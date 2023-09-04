import glob
from pathlib import Path
from os.path import dirname, join
import json

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

def translate(key: str, lang: str = DEFAULT_LANG) -> str:
    keys = key.split(".")

    try:
        entry = __TRANSLATIONS__[lang]

        for key_part in keys:
            entry = entry[key_part]

        return entry
    except KeyError:
        return f"#{key}"

def i18n_context_processor():
    return dict(
        t=translate,
    )

class i18n_manager:
    @classmethod
    def init_app(cls, app):
        load_translations()
        app.context_processor(i18n_context_processor)
