from unittest.mock import patch

import pytest

from django_mask.parser import parse_config
from django_mask.mask_models import MaskField, MaskModel, MaskTask
from django_mask.tests.conftest import fake_django_model
from django_mask.error import Error, INVALID_FILE_CONTENT_FORMAT, IMPORT_ERROR


@pytest.fixture
def valid_conf(mask_model_path):
    return """
    locale: "ru"
    models:
      - path: "{}"
        fields:
          - name: "email"
            mask_func: "email"
          - name: "name"
            mask_func: "name"

      - path: "{}"
        fields:
          - name: "name"
            mask_func: "name"
    """.format(mask_model_path, mask_model_path)


@pytest.fixture
def invalid_conf():
    return """
    locale: "ru"
    models:
        - path: "some_path"
          fields:
            - name: "email"
              mask_func: "email"
            - name: "name"

        - path: "another_path"
          fields:
            - name: "name"
              mask_func: "name"
    """


def test_parse_valid_conf(valid_conf):
    mask_task = MaskTask("ru")
    dj_model = fake_django_model()

    msk_model_1 = MaskModel("some_path", dj_model)
    msk_model_1.add_field(MaskField("email", "email"))
    msk_model_1.add_field(MaskField("name", "name"))
    mask_task.add_model(msk_model_1)

    msk_model_2 = MaskModel("another_path", dj_model)
    msk_model_2.add_field(MaskField("name", "name"))
    mask_task.add_model(msk_model_2)

    with patch("django_mask.mask_models.import_model") as mock_import:
        mock_import.return_value = (dj_model, None)
        task, errors = parse_config(valid_conf)
        assert not errors
        assert len(task.models) == 2


@pytest.mark.parametrize(
    "conf_string",
    [
        "",
        "test_string",
        "models: 1",
        "models: [1,2,3]"
    ]
)
def test_parse_invalid_conf_content_format(conf_string):
    task, errors = parse_config(conf_string)
    assert task is None
    assert isinstance(errors, list)
    assert len(errors) == 1
    assert isinstance(errors[0], Error)
    assert errors[0].message == INVALID_FILE_CONTENT_FORMAT


def test_parse_import_error(invalid_conf):
    task, errors = parse_config(invalid_conf)
    assert task is None
    assert len(errors) == 2
    assert errors[0].message == IMPORT_ERROR.format("some_path")
    assert errors[1].message == IMPORT_ERROR.format("another_path")
