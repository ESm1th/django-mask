from typing import Optional

from faker import Faker


def new_faker(locale: Optional[str] = None):
    f = Faker(locale)
    if isinstance(locale, str):
        f.seed_locale(locale.replace("-", "_"), 0)
    return f
