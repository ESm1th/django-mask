import os
from types import FunctionType
from typing import List, Dict, Optional, Tuple
from collections import OrderedDict

from django.db.models import Model as DjangoModel
from mask.handlers import HANDLERS
from mask.importer import FakeImporter, DjangoImporter


IMPORTER = DjangoImporter if not os.getenv("TEST_IMPORTER") else FakeImporter


class MaskField:
    __slots__ = ("__name", "__func_name")

    def __init__(self, name: str, func_name: str) -> None:
        self.__name = name
        self.__func_name = func_name

    @property
    def field_name(self):
        return self.__name

    @property
    def process_func(self):
        return HANDLERS[self.__func_name]

    @property
    def func_map(self) -> Tuple[str, FunctionType]:
        return (self.field_name, self.process_func)

    def __eq__(self, __o: object) -> bool:
        if type(self) != type(__o):
            return False
        return self.func_map == __o.func_map


class MaskModel:
    __slots__ = ("__model_path", "__model", "__mask_fields", "__func_map")

    def __init__(self, path: str) -> None:
        self.__model_path = path
        self.__model = None
        self.__mask_fields: Tuple[MaskField] = tuple()
        self.__func_map: Optional[Dict] = None

    def add_field(self, mask_field: MaskField) -> None:
        self.__mask_fields = self.__mask_fields + (mask_field, )

    @property
    def dj_model(self) -> DjangoModel:
        if self.__model is None:
            self.__model = IMPORTER(self.__model_path).import_model()
        return self.__model

    @property
    def model_path(self):
        return self.__model_path

    @property
    def func_map(self):
        if self.__func_map is None:
            f_map = []
            for f in self.__mask_fields:
                f_map.append(f.func_map)
            self.__func_map = OrderedDict(f_map)
        return self.__func_map

    @property
    def is_empty(self):
        return self.__model.objects.exists()

    def __eq__(self, __o: object) -> bool:
        if type(self) != type(__o):
            return False
        return (self.model_path, self.func_map, self.__mask_fields) == \
               (__o.model_path, __o.func_map, __o.__mask_fields)


class MaskTask:
    __slots__ = ("__locale", "__mask_models")

    def __init__(self, locale: Optional[str] = None) -> None:
        self.__locale = locale
        self.__mask_models: Tuple[MaskModel] = tuple()

    @property
    def locale(self):
        return self.__locale

    def add_model(self, mask_model: MaskModel) -> None:
        self.__mask_models = self.__mask_models + (mask_model, )

    @property
    def models(self):
        return self.__mask_models

    def __eq__(self, __o: object) -> bool:
        if type(self) != type(__o):
            return False
        return (self.locale, self.models) == (__o.locale, __o.models)


class UpdateTask:
    __slots__ = ("__tablename", "__ids", "__handlers")

    def __init__(self, tablename: str, ids: List[int], handlers: List[Dict[str, str | int]]) -> None:
        self.__tablename = tablename
        self.__ids = ids
        self.__handlers = handlers

    @property
    def db_table_name(self):
        return self.__tablename

    @property
    def chunk_ids(self):
        return self.__ids

    @property
    def handlers(self):
        return self.__handlers
