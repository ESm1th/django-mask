import enum

from django_mask import fake


class Fields(enum.Enum):
    INN = "inn"
    KPP = "kpp"
    NAME = "name"
    EMAIL = "email"
    USERNAME = "username"


HANDLERS = {
    Fields.INN.value: fake.mask_buisness_inn,
    Fields.KPP.value: fake.mask_kpp,
    Fields.FIRST_NAME.value: fake.mask_first_name,
    Fields.LAST_NAME.value: fake.mask_last_name,
    Fields.MIDDLE_NAME.value: fake.mask_middle_name,
    Fields.OGRN.value: fake.mask_buisness_ogrn,
    Fields.ADDRESS: fake.mask_address,
    Fields.EMAIL.value: fake.mask_email
}
