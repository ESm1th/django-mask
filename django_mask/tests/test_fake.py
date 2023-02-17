import re

import pytest

from django_mask import fake


def test_mask_inn(locale_str):
    inns = (
        "407594767788",
        "2295251628",
        "319560623873",
        "0767180497"
    )
    f = fake.new_faker(locale_str)
    values = fake.mask_inn(f, inns)
    assert len(values[0]) == fake.INDIVIDUALS_INN_LENGTH
    assert len(values[1]) == fake.BUSINESS_INN_LENGTH
    assert len(values[2]) == fake.INDIVIDUALS_INN_LENGTH
    assert len(values[3]) == fake.BUSINESS_INN_LENGTH


def test_mask_empty_inn(locale_str):
    inns = (
        "",
        None
    )
    f = fake.new_faker(locale_str)
    values = fake.mask_inn(f, inns)
    assert len(values) == len(inns)
    assert values[0] == ""
    assert values[1] == ""


def test_mask_ogrn(locale_str):
    ogrns = (
        "301027775666368",
        "5234351118843",
        "301027775666368",
        "1084319313935"
    )
    f = fake.new_faker(locale_str)
    values = fake.mask_ogrn(f, ogrns)
    assert len(values[0]) == fake.INDIVIDUALS_OGRN_LENGTH
    assert len(values[1]) == fake.BUSINESS_OGRN_LENGTH
    assert len(values[2]) == fake.INDIVIDUALS_OGRN_LENGTH
    assert len(values[3]) == fake.BUSINESS_OGRN_LENGTH


def test_mask_empty_ogrn(locale_str):
    ogrns = (
        "",
        None
    )
    f = fake.new_faker(locale_str)
    values = fake.mask_inn(f, ogrns)
    assert len(values) == len(ogrns)
    assert values[0] == ""
    assert values[1] == ""


@pytest.mark.parametrize(
    "value",
    (1, 2, 3)
)
def test_mask_phone(locale_str, value):
    f = fake.new_faker(locale_str)
    phone_pattern = r"^\+7\d{%d}$" % fake.PHONE_NUMBER_FORMAT.count("#")
    phones = fake.mask_phone(f, (value, ))
    assert len(phones) == 1
    assert re.match(phone_pattern, phones[0])
