from faker import Faker
from faker.providers.phone_number.ru_RU import Provider


Provider.formats = (
    "+7##########",
)

DEFAULT_CHUNKS = 1


def new_faker(locale=None):
    f = Faker(locale)
    if isinstance(locale, str):
        f.seed_locale(locale, 0)
    return f


def mask_from_chunks(func, chunks):
    items = tuple()
    for _ in range(chunks):
        items += (func(), )
    return items


def mask_first_name(f, chunks=DEFAULT_CHUNKS):
    first_names = tuple()
    for idx in range(chunks):
        func = f.first_name_male
        if idx % 2 != 0:
            func = f.first_name_female
        first_names += (func(),)
    return first_names


def mask_last_name(f, chunks=DEFAULT_CHUNKS):
    last_names = tuple()
    for idx in range(chunks):
        func = f.last_name_male
        if idx % 2 != 0:
            func = f.last_name_female
        last_names += (func(),)
    return last_names


def mask_middle_name(f, chunks=DEFAULT_CHUNKS):
    middle_names = tuple()
    for idx in range(chunks):
        func = f.middle_name_male
        if idx % 2 != 0:
            func = f.middle_name_female
        middle_names += (func(),)
    return middle_names


def mask_company_name(f, chunks=DEFAULT_CHUNKS):
    return mask_from_chunks(f.company, chunks)


def mask_address(f, chunks=DEFAULT_CHUNKS):
    return mask_from_chunks(f.address, chunks)


def mask_city(f, chunks=DEFAULT_CHUNKS):
    return mask_from_chunks(f.city_name, chunks)


def mask_buisness_inn(f, chunks=DEFAULT_CHUNKS):
    return mask_from_chunks(f.buisnesses_inn, chunks)


def mask_individual_inn(f, chunks=DEFAULT_CHUNKS):
    return mask_from_chunks(f.individuals_inn, chunks)


def mask_kpp(f, chunks=DEFAULT_CHUNKS):
    return mask_from_chunks(f.kpp, chunks)


def mask_buisness_ogrn(f, chunks=DEFAULT_CHUNKS):
    return mask_from_chunks(f.buisnesses_ogrn, chunks)


def mask_individual_ogrn(f, chunks=DEFAULT_CHUNKS):
    return mask_from_chunks(f.individuals_ogrn, chunks)


def mask_email(f, chunks=DEFAULT_CHUNKS):
    return mask_from_chunks(f.email, chunks)


def mask_phone(f, chunks=DEFAULT_CHUNKS):
    return mask_from_chunks(f.phone_number, chunks)
