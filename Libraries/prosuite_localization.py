import localization_bg
import localization_en
import localization_ru
import localization_fr

from prosuite_localization_utils import Localization, get_lang


LOCALIZATIONS = {
    "bg": localization_bg,
    "en": localization_en,
    "fr": localization_fr,
    "ru": localization_ru,
}


def get_localization():
    """
    """
    return Localization(loc_source=LOCALIZATIONS["en"].localization_dict)
    return Localization(loc_source=LOCALIZATIONS[get_lang()].localization)
