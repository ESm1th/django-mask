from django_mask import fake


class FuncsNames:
    INN = "mask_inn"
    KPP = "mask_kpp"
    BIK = "mask_bik"
    NAME = "mask_name"
    EMAIL = "mask_email"
    USERNAME = "mask_username"
    FIRST_NAME = "mask_first_name"
    LAST_NAME = "mask_last_name"
    MIDDLE_NAME = "mask_middle_name"
    FULL_NAME = "mask_full_name"
    OGRN = "mask_ogrn"
    ADDRESS = "mask_address"
    PHONE = "mask_phone"
    COMPANY_NAME = "mask_company_name"
    BANK = "mask_bank"
    CORR_ACCOUNT = "mask_corr_account"
    PAY_ACCOUNT = "mask_pay_account"
    IBAN = "mask_iban"
    SWIFT = "mask_swift"


HANDLERS = {
    FuncsNames.INN: fake.mask_business_inn,
    FuncsNames.KPP: fake.mask_kpp,
    FuncsNames.FIRST_NAME: fake.mask_first_name,
    FuncsNames.LAST_NAME: fake.mask_last_name,
    FuncsNames.MIDDLE_NAME: fake.mask_middle_name,
    FuncsNames.FULL_NAME: fake.mask_full_name,
    FuncsNames.OGRN: fake.mask_business_ogrn,
    FuncsNames.ADDRESS: fake.mask_address,
    FuncsNames.EMAIL: fake.mask_email,
    FuncsNames.PHONE: fake.mask_phone,
    FuncsNames.USERNAME: fake.mask_username,
    FuncsNames.COMPANY_NAME: fake.mask_company_name,
    FuncsNames.BANK: fake.mask_bank,
    FuncsNames.BIK: fake.mask_bik,
    FuncsNames.CORR_ACCOUNT: fake.mask_corr_account,
    FuncsNames.PAY_ACCOUNT: fake.mask_pay_account,
    FuncsNames.IBAN: fake.mask_iban,
    FuncsNames.SWIFT: fake.mask_swift,
}
