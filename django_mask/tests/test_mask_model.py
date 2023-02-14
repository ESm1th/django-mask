from unittest.mock import Mock, PropertyMock, patch
from collections import OrderedDict

import pytest

from django_mask import mask_models
from django_mask import fake


TEST_MASK_MODEL_PATH = "agora.core.order"
TEST_DB_TABLE_NAME = "order_order"


def fake_django_model(db_table="", exists=True):
    m = Mock()
    m.objects.exists.return_value = exists
    m._meta.db_table = db_table or TEST_DB_TABLE_NAME
    return m


@pytest.fixture
def field_handlers():
    return OrderedDict({
        "first_name": "mask_first_name",
        "last_name": "mask_last_name",
        "email": "mask_email",
        "phone": "mask_phone",
    })


@pytest.fixture
def mask_model(field_handlers):
    mm = mask_models.MaskModel(TEST_MASK_MODEL_PATH)
    for field_name, function_name in field_handlers.items():
        mm.add_field(mask_models.MaskField(field_name, function_name))
    return mm


def test_mask_model_model_path(mask_model):
    assert TEST_MASK_MODEL_PATH == mask_model.model_path


def test_mask_model_db_table_name(mask_model):
    with patch("django_mask.mask_models.MaskModel.dj_model", new_callable=PropertyMock) as mock_property:
        mock_property.return_value = fake_django_model()
        assert TEST_DB_TABLE_NAME == mask_model.db_table_name


def test_mask_model_is_empty_false(mask_model):
    with patch("django_mask.mask_models.MaskModel.dj_model", new_callable=PropertyMock) as mock_property:
        mock_property.return_value = fake_django_model()
        assert not mask_model.is_empty


def test_mask_model_is_empty_true(mask_model):
    with patch("django_mask.mask_models.MaskModel.dj_model", new_callable=PropertyMock) as mock_property:
        mock_property.return_value = fake_django_model(exists=False)
        assert mask_model.is_empty


def test_mask_model_ordered_db_fields(mask_model, field_handlers):
    assert tuple(field_handlers.keys()) == tuple(mask_model.ordered_db_fields)
    assert not tuple(reversed(field_handlers.keys())) == tuple(mask_model.ordered_db_fields)


def test_mask_model_values(mask_model):
    fk = fake.new_faker("ru")
    chunks = 3

    first_names_values = fake.mask_first_name(fk, chunks)
    last_names_values = fake.mask_last_name(fk, chunks)
    email_values = fake.mask_email(fk, chunks)
    phone_values = fake.mask_phone(fk, chunks)
    test_values = zip(first_names_values, last_names_values, email_values, phone_values)

    fk.seed_locale("ru", 0)
    masked_values = mask_model.mask(fk, chunks)
    assert tuple(test_values) == tuple(masked_values)


def test_mask_update_values_with_ids(mask_model):
    fk = fake.new_faker("ru")
    ids = (111, 222, 333)
    chunks = len(ids)
    masked_values = tuple(mask_model.mask(fk, chunks))
    masked_values_with_ids = tuple(mask_model.update_values_with_ids(ids, masked_values))
    assert ids[0] == masked_values_with_ids[0][0]
    assert ids[1] == masked_values_with_ids[1][0]
    assert ids[2] == masked_values_with_ids[2][0]


def test_mask_get_update_sql_query(mask_model):
    fk = fake.new_faker("ru")
    ids = (111, 222, 333)
    chunks = len(ids)

    first_names_values = fake.mask_first_name(fk, chunks)
    last_names_values = fake.mask_last_name(fk, chunks)
    email_values = fake.mask_email(fk, chunks)
    phone_values = fake.mask_phone(fk, chunks)
    test_values = tuple(zip(first_names_values, last_names_values, email_values, phone_values))

    expected = """
    UPDATE order_order as base
    SET
        first_name = val.first_name,
        last_name = val.last_name,
        email = val.email,
        phone = val.phone
    FROM (
        VALUES
        (111, {}),
        (222, {}),
        (333, {})
    ) AS val(id, first_name, last_name, email, phone)
    WHERE base.id = val.id
    """.format(
        ", ".join(test_values[0]),
        ", ".join(test_values[1]),
        ", ".join(test_values[2])
    ).splitlines()

    with patch("django_mask.mask_models.MaskModel.dj_model", new_callable=PropertyMock) as mock_property:
        mock_property.return_value = fake_django_model()
        fk.seed_locale("ru", 0)
        query = mask_model.get_update_sql_query(fk, ids)
        for idx, line in enumerate(query.splitlines()):
            assert line.strip() == expected[idx].strip()
