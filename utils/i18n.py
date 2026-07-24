import os
import gettext

LOCALES_DIR = os.path.join(os.path.dirname(__file__),'..','locales')
DEFAULT_LANG ='uz'


def _(key:str, lang: str=DEFAULT_LANG, **kwargs) -> str:
    try:
        translator = gettext.translation(
            domain='bot',
            localedir=LOCALES_DIR,
            languages=[lang],
        )
        text=translator.gettext(key)
    except FileNotFoundError:
        text = key
    return text.format(**kwargs) if kwargs else text
        
        