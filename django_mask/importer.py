from abc import ABC, abstractmethod
from importlib import import_module


class FakeModel:

    def __init__(self, first_name: str, second_name: str, email: str, inn: str, kpp: str, okpo: str) -> None:
        self.first_name = first_name
        self.second_name = second_name
        self.email = email
        self.inn = inn
        self.kpp = kpp
        self.okpo = okpo


class Importer(ABC):

    def __init__(self, model_path: str) -> None:
        self.__model_path = model_path

    def model_path(self):
        return self.__model_path

    @abstractmethod
    def import_model(self):
        return


class FakeImporter(Importer):

    def import_model(self):
        return FakeModel


class DjangoImporter(Importer):

    def import_model(self):
        return import_module(self.__model_path)
