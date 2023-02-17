from django_mask import fake


class Fields:
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
    COMPANY_NAME = "mask_company_name"


HANDLERS = {
    Fields.INN: fake.mask_business_inn,
    Fields.KPP: fake.mask_kpp,
    Fields.FIRST_NAME: fake.mask_first_name,
    Fields.LAST_NAME: fake.mask_last_name,
    Fields.MIDDLE_NAME: fake.mask_middle_name,
    Fields.OGRN: fake.mask_business_ogrn,
    Fields.ADDRESS: fake.mask_address,
    Fields.EMAIL: fake.mask_email,
    Fields.PHONE: fake.mask_phone,
    Fields.USERNAME: fake.mask_username,
    Fields.COMPANY_NAME: fake.mask_company_name
}
