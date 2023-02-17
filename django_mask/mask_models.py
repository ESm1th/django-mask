import sys
from django.db import connection

from django_mask.handlers import HANDLERS
from django_mask.fake import new_faker
from django_mask.utils import import_model
from django_mask.error import Error
from django_mask.queries import Queries


class MaskField:
    __slots__ = ("__name", "__func_name")

    def __init__(self, name, func_name):
        self.__name = name
        self.__func_name = func_name

    @property
    def field_name(self):
        return self.__name

    @property
    def process_func(self):
        return HANDLERS[self.__func_name]

    @property
    def func_map(self):
        return (self.field_name, self.process_func)

    def mask(self, faker, values):
        return self.process_func(faker, values)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.func_map == other.func_map


class MaskModel:
    __slots__ = ("__model_path", "__model", "__mask_fields")

    def __init__(self, path, dj_model):
        self.__model_path = path
        self.__model = dj_model
        self.__mask_fields = tuple()

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return (self.model_path, self.ordered_db_fields) == (other.model_path, other.ordered_db_fields)

    @classmethod
    def new(cls, path):
        dj_model, error = import_model(path)
        if isinstance(error, Error):
            return None, error
        return cls(path, dj_model), None

    def add_field(self, mask_field):
        self.__mask_fields = self.__mask_fields + (mask_field, )

    @property
    def dj_model(self):
        return self.__model

    @property
    def model_path(self):
        return self.__model_path

    @property
    def db_table_name(self):
        return self.dj_model._meta.db_table

    @property
    def is_empty(self):
        return not self.dj_model.objects.exists()

    @property
    def ordered_db_fields(self):
        return tuple(sorted([f.field_name for f in self.__mask_fields]))

    def mask(self, faker, values):
        faked_values = []
        for i, f in enumerate(sorted(self.__mask_fields, key=lambda mf: mf.field_name)):
            faked_values.append(f.mask(faker, values[i]))
        return tuple(zip(*faked_values))

    def update_values_with_ids(self, ids, values):
        if len(ids) != len(values):
            raise ValueError("length of list of values not equal with length of ids list")
        with_ids = []
        for idx in range(len(values)):
            with_ids.append(
                (ids[idx],) + values[idx]
            )
        return tuple(with_ids)

    def create_update_task(self, faker, ids):
        queries = Queries()
        values_from_db = queries.get_existing_values(self.db_table_name, self.ordered_db_fields, ids)
        values_to_update = self.mask(faker, values_from_db)
        values_to_update = self.update_values_with_ids(ids, values_to_update)
        update_query = queries.build_update_query(self.db_table_name, self.ordered_db_fields, values_to_update)
        task = UpdateTask(update_query)
        return task

    def get_update_tasks(self, chunks, faker):
        update_tasks = []
        start = 0
        stop = chunks
        while True:
            ids = self.dj_model.objects.values_list('id', flat=True)[start:stop]
            if not ids:
                break
            update_tasks.append(self.create_update_task(faker, ids))
            start = stop
            stop += chunks
        return update_tasks


class MaskTask:
    __slots__ = ("__locale", "__mask_models")

    def __init__(self, locale=None):
        self.__locale = locale
        self.__mask_models = tuple()

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return (self.locale, self.models) == (other.locale, other.models)

    @property
    def locale(self):
        return self.__locale

    def add_model(self, mask_model):
        self.__mask_models = self.__mask_models + (mask_model, )

    @property
    def models(self):
        return self.__mask_models

    def get_update_tasks(self, chunks):
        fk = new_faker(self.locale)
        update_tasks = []
        for mask_model in self.models:
            if mask_model.is_empty:
                continue
            update_tasks.extend(mask_model.get_update_tasks(chunks, fk))
        return update_tasks


class UpdateTask:
    __slots__ = "__query"

    def __init__(self, query):
        self.__query = query

    @property
    def query(self):
        return self.__query

    def process(self, cursor=None, print_query=False):
        if cursor is None:
            cursor = connection.cursor()
        if print_query:
            sys.stdout.write("{}\n".format(self.query))
        cursor.execute(self.query)
