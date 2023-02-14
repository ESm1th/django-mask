from django.db import connection

from django_mask.handlers import HANDLERS
from django_mask.fake import DEFAULT_CHUNKS
from django_mask.importer import DjangoModelImporter


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

    def mask(self, faker, chunks=DEFAULT_CHUNKS):
        return self.process_func(faker, chunks)

    def __eq__(self, other: object):
        if type(self) != type(other):
            return False
        return self.func_map == other.func_map


class MaskModel:
    __slots__ = ("__model_path", "__model", "__mask_fields")

    def __init__(self, path) -> None:
        self.__model_path = path
        self.__model = None
        self.__mask_fields = tuple()

    def add_field(self, mask_field):
        self.__mask_fields = self.__mask_fields + (mask_field, )

    @property
    def dj_model(self):
        if self.__model is None:
            self.__model = DjangoModelImporter(self.__model_path).import_model()
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
        return [f.field_name for f in self.__mask_fields]

    def mask(self, faker, chunks=DEFAULT_CHUNKS):
        values = []
        for f in self.__mask_fields:
            values.append(f.mask(faker, chunks))
        return tuple(zip(*values))

    def update_values_with_ids(self, ids, values):
        if len(ids) != len(values):
            raise ValueError("length of list of values not equal with length of ids list")
        with_ids = []
        for idx in range(len(values)):
            with_ids.append(
                (ids[idx],) + values[idx]
            )
        return tuple(with_ids)

    def get_update_sql_query(self, faker, ids):
        query = """
        UPDATE {} as base
        SET
            {}
        FROM (
            VALUES
            {}
        ) AS val(id, {})
        WHERE base.id = val.id
        """

        values = self.mask(faker, len(ids))
        values_with_ids = self.update_values_with_ids(ids, values)
        ordered_db_fields = self.ordered_db_fields

        set_str = ",\n\t    ".join([
            "{} = val.{}".format(field, field)
            for field in ordered_db_fields
        ])
        values_str = ",\n\t    ".join([
            str(val).replace("'", "")
            for val in values_with_ids
        ])
        fields_str = ", ".join(ordered_db_fields)

        query = query.format(
            self.db_table_name,
            set_str,
            values_str,
            fields_str
        )
        return query


class MaskTask:
    __slots__ = ("__locale", "__mask_models")

    def __init__(self, locale=None):
        self.__locale = locale
        self.__mask_models = tuple()

    @property
    def locale(self):
        return self.__locale

    def add_model(self, mask_model):
        self.__mask_models = self.__mask_models + (mask_model, )

    @property
    def models(self):
        return self.__mask_models

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return (self.locale, self.models) == (other.locale, other.models)


class UpdateTask:
    __slots__ = ("__msk_model", "__ids", "__faker")

    def __init__(self, msk_model, ids, faker):
        self.__msk_model = msk_model
        self.__ids = ids
        self.__faker = faker

    @property
    def mask_model(self):
        return self.__msk_model

    @property
    def chunk_ids(self):
        return self.__ids

    @property
    def faker(self):
        return self.__faker

    def process(self):
        update_query = self.mask_model.get_update_sql_query(self.faker, self.chunk_ids)
        cursor = connection.cursor()
        cursor.execute(update_query)
