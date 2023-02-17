from faker import Faker
from faker.providers.phone_number.ru_RU import Provider

PHONE_NUMBER_FORMAT = "+7##########"

Provider.formats = (
    PHONE_NUMBER_FORMAT,
)

DEFAULT_CHUNKS = 1
BUSINESS_INN_LENGTH = 10
INDIVIDUALS_INN_LENGTH = 12
BUSINESS_OGRN_LENGTH = 13
INDIVIDUALS_OGRN_LENGTH = 15


def new_faker(locale=None):
    f = Faker(locale)
    f.seed_locale(locale, 0)
    return f


def mask_from_chunks(func, chunks):
    items = tuple()
    for _ in range(chunks):
        items += (func(), )
    return items


def mask_full_name(f, values):
    return mask_from_chunks(f.name, len(values))


def mask_first_name(f, values):
    first_names = tuple()
    for idx in range(len(values)):
        func = f.first_name_male
        if idx % 2 != 0:
            func = f.first_name_female
        first_names += (func(),)
    return first_names


def mask_last_name(f, values):
    last_names = tuple()
    for idx in range(len(values)):
        func = f.last_name_male
        if idx % 2 != 0:
            func = f.last_name_female
        last_names += (func(),)
    return last_names


def mask_middle_name(f, values):
    middle_names = tuple()
    for idx in range(len(values)):
        func = f.middle_name_male
        if idx % 2 != 0:
            func = f.middle_name_female
        middle_names += (func(),)
    return middle_names


def mask_company_name(f, values):
    return mask_from_chunks(f.company, len(values))


def mask_address(f, values):
    return mask_from_chunks(f.address, len(values))


def mask_city(f, values):
    return mask_from_chunks(f.city_name, len(values))


def mask_inn(f, values):
    inns = tuple()
    for value in values:
        inn = ("", )
        if value:
            func = mask_individuals_inn if len(value) != BUSINESS_INN_LENGTH else mask_business_inn
            inn = func(f, (value, ))
        inns += inn
    return inns


def mask_business_inn(f, values):
    return mask_from_chunks(f.businesses_inn, len(values))


def mask_individuals_inn(f, values):
    return mask_from_chunks(f.individuals_inn, len(values))


def mask_kpp(f, values):
    return mask_from_chunks(f.kpp, len(values))


def mask_ogrn(f, values):
    ogrns = tuple()
    for value in values:
        ogrn = ("", )
        if value:
            func = mask_individuals_ogrn if len(value) != BUSINESS_OGRN_LENGTH else mask_business_ogrn
            ogrn = func(f, (value, ))
        ogrns += ogrn
    return ogrns


def mask_business_ogrn(f, values):
    return mask_from_chunks(f.businesses_ogrn, len(values))


def mask_individuals_ogrn(f, values):
    return mask_from_chunks(f.individuals_ogrn, len(values))


def mask_email(f, values):
    return mask_from_chunks(f.email, len(values))


def mask_phone(f, values):
    return mask_from_chunks(f.phone_number, len(values))


def mask_username(f, values):
    return mask_from_chunks(f.unique.user_name, len(values))
