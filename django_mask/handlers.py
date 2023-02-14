import enum

from django_mask import fake


class Fields(enum.Enum):
    INN = "mask_inn"
    KPP = "mask_kpp"
    NAME = "mask_name"
    EMAIL = "mask_email"
    USERNAME = "mask_username"
    FIRST_NAME = "mask_first_name"
    LAST_NAME = "mask_last_name"
    MIDDLE_NAME = "mask_middle_name"
    OGRN = "mask_ogrn"
    ADDRESS = "mask_address"
    PHONE = "mask_phone"


HANDLERS = {
    Fields.INN.value: fake.mask_buisness_inn,
    Fields.KPP.value: fake.mask_kpp,
    Fields.FIRST_NAME.value: fake.mask_first_name,
    Fields.LAST_NAME.value: fake.mask_last_name,
    Fields.MIDDLE_NAME.value: fake.mask_middle_name,
    Fields.OGRN.value: fake.mask_buisness_ogrn,
    Fields.ADDRESS: fake.mask_address,
    Fields.EMAIL.value: fake.mask_email,
    Fields.PHONE.value: fake.mask_phone,
}
