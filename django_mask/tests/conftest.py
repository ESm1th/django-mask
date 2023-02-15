import os
from unittest.mock import Mock

import pytest

from django_mask import mask_models


TEST_LOCALE = "ru"
TEST_MASK_MODEL_PATH = "some.test.path"
TEST_DB_TABLE_NAME = "order_order"


def fake_django_model(db_table="", exists=True):
    m = Mock()
    m.objects.exists.return_value = exists
    m._meta.db_table = db_table or TEST_DB_TABLE_NAME
    return m


@pytest.fixture
def locale_str():
    locale_from_env = os.environ.get("TEST_LOCALE")
    return locale_from_env or TEST_LOCALE


@pytest.fixture
def mask_model_path():
    return TEST_MASK_MODEL_PATH


@pytest.fixture
def db_table_name():
    return TEST_DB_TABLE_NAME


@pytest.fixture
def field_handlers():
    return {
        "first_name": "mask_first_name",
        "last_name": "mask_last_name",
        "email": "mask_email",
        "phone": "mask_phone",
    }


@pytest.fixture
def mask_model(mask_model_path, field_handlers):
    mm = mask_models.MaskModel(mask_model_path, fake_django_model())
    for field_name, function_name in field_handlers.items():
        mm.add_field(mask_models.MaskField(field_name, function_name))
    return mm
