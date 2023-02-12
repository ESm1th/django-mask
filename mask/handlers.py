import enum


class Fields(enum.Enum):
    INN = "inn"
    KPP = "kpp"
    NAME = "name"
    EMAIL = "email"
    USERNAME = "username"


HANDLERS = {
    Fields.INN.value: 1,
    Fields.KPP.value: 2,
    Fields.NAME.value: 3,
    Fields.EMAIL.value: 4
}
