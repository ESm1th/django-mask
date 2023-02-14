from abc import ABC, abstractmethod
from importlib import import_module


class Importer(ABC):

    def __init__(self, model_path):
        self.__path = model_path

    @abstractmethod
    def import_model(self):
        pass


class DjangoModelImporter(Importer):

    def import_model(self):
        return import_module(self.__path)
