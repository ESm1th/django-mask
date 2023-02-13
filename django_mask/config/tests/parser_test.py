import os

import pytest
from django_mask.config.parser import parse
from django_mask.mask_models import MaskField, MaskModel, MaskTask


os.environ["TEST_IMPORTER"] = "1"


@pytest.fixture
def valid_conf():
    return """
    locale: "ru"
    models:
      - path: "some_path"
        fields:
          - name: "email"
            processor: "email"
          - name: "name"
            processor: "name"

      - path: "another_path"
        fields:
          - name: "name"
            processor: "name"
    """


@pytest.fixture
def invalid_conf():
    return """
    locale: "ru"
    models:
        - path: "some_path"
            fields:
            - name: "email"
                processor: "email"
            - name: "name"

        - path: "another_path"
            fields:
            - name: "name"
                processor: "name"
    """


def test_parse_valid_conf(valid_conf):
    mask_task = MaskTask("ru")

    msk_model_1 = MaskModel("some_path")
    msk_model_1.add_field(MaskField("email", "email"))
    msk_model_1.add_field(MaskField("name", "name"))
    mask_task.add_model(msk_model_1)

    msk_model_2 = MaskModel("another_path")
    msk_model_2.add_field(MaskField("name", "name"))
    mask_task.add_model(msk_model_2)

    task = parse(valid_conf)
    assert task == mask_task
