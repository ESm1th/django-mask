from unittest.mock import Mock, PropertyMock, patch

from django_mask import fake
from django_mask.tests.conftest import fake_django_model
from django_mask.queries import Queries
from django_mask.tests.conftest import existing_db_values

Queries.get_existing_values = Mock()
Queries.get_existing_values.return_value = existing_db_values
Queries.__init__ = Mock()
Queries.__init__.return_value = None


def test_mask_model_model_path(mask_model, mask_model_path):
    assert mask_model.model_path == mask_model_path


def test_mask_model_db_table_name(mask_model, db_table_name):
    with patch("django_mask.mask_models.MaskModel.dj_model", new_callable=PropertyMock) as mock_property:
        mock_property.return_value = fake_django_model()
        assert mask_model.db_table_name == db_table_name


def test_mask_model_is_empty_false(mask_model):
    with patch("django_mask.mask_models.MaskModel.dj_model", new_callable=PropertyMock) as mock_property:
        mock_property.return_value = fake_django_model()
        assert not mask_model.is_empty


def test_mask_model_is_empty_true(mask_model):
    with patch("django_mask.mask_models.MaskModel.dj_model", new_callable=PropertyMock) as mock_property:
        mock_property.return_value = fake_django_model(exists=False)
        assert mask_model.is_empty


def test_mask_model_ordered_db_fields(mask_model, field_handlers):
    assert tuple(sorted(field_handlers.keys())) == tuple(mask_model.ordered_db_fields)
    assert not tuple(reversed(sorted(field_handlers.keys()))) == tuple(mask_model.ordered_db_fields)


def test_mask_model_values(mask_model, locale_str, existing_values_from_db):
    fk = fake.new_faker(locale_str)

    email_values = fake.mask_email(fk, existing_values_from_db[0])
    first_names_values = fake.mask_first_name(fk, existing_values_from_db[1])
    last_names_values = fake.mask_last_name(fk, existing_values_from_db[2])
    phone_values = fake.mask_phone(fk, existing_values_from_db[3])
    test_values = zip(email_values, first_names_values, last_names_values, phone_values)

    fk.seed_locale(locale_str, 0)
    masked_values = mask_model.mask(fk, existing_values_from_db)
    assert tuple(test_values) == tuple(masked_values)


def test_mask_update_values_with_ids(mask_model, locale_str, existing_values_from_db):
    fk = fake.new_faker(locale_str)
    ids = (111, 222, 333)
    masked_values = tuple(mask_model.mask(fk, existing_values_from_db))
    masked_values_with_ids = tuple(mask_model.update_values_with_ids(ids, masked_values))
    assert ids[0] == masked_values_with_ids[0][0]
    assert ids[1] == masked_values_with_ids[1][0]
    assert ids[2] == masked_values_with_ids[2][0]


def test_mask_get_update_sql_query(mask_model, locale_str, existing_values_from_db):
    fk = fake.new_faker(locale_str)
    ids = (111, 222, 333)

    # Порядок данных вызовов имеет значение, т.к. далее в `mask_model.get_update_sql_query(fk, ids)` они будут идти
    # в этом же порядке (отсортированные по имени поля).
    # Тут это нужно для того чтобы далее можно было сравнить получившиеся sql запросы.
    # Если эти вызовы сделать в другом порядке - тест не пройдет.
    # Так работает генератор случайных значений в faker, несмотря на то что ниже идет сброс зерна (seed) к тому же
    # значению что было изначально установлено в factory функции `fake.new_faker`.
    email_values = fake.mask_email(fk, existing_values_from_db[0])
    first_names_values = fake.mask_first_name(fk, existing_values_from_db[1])
    last_names_values = fake.mask_last_name(fk, existing_values_from_db[2])
    phone_values = fake.mask_phone(fk, existing_values_from_db[3])
    test_values = tuple(zip(email_values, first_names_values, last_names_values, phone_values))

    expected = """
    UPDATE order_order as base
    SET
        email = val.email,
        first_name = val.first_name,
        last_name = val.last_name,
        phone = val.phone
    FROM (
        VALUES
        (111, {}),
        (222, {}),
        (333, {})
    ) AS val(id, email, first_name, last_name, phone)
    WHERE base.id = val.id
    """.format(
        ", ".join(["'{}'".format(val) for val in test_values[0]]),
        ", ".join(["'{}'".format(val) for val in test_values[1]]),
        ", ".join(["'{}'".format(val) for val in test_values[2]])
    )
    expected_lines = expected.splitlines()

    with patch("django_mask.mask_models.MaskModel.dj_model", new_callable=PropertyMock) as mock_property:
        fk.seed_locale(locale_str, 0)
        mock_property.return_value = fake_django_model()
        update_task = mask_model.create_update_task(fk, ids)
        for idx, line in enumerate(update_task.query.splitlines()):
            assert line.strip() == expected_lines[idx].strip()
