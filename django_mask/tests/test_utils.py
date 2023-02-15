from django_mask.utils import import_model
from django_mask.mask_models import MaskModel
from django_mask.error import module_has_not_attribute_error


def test_import_model_valid_path():
    imported, error = import_model("django_mask.mask_models.MaskModel")
    assert error is None
    assert imported is MaskModel


def test_import_model_invalid_path():
    expected_error = module_has_not_attribute_error(
        "django_mask.mask_models",
        "FakeModel"
    )
    imported, error = import_model("django_mask.mask_models.FakeModel")
    assert imported is None
    assert error.message == expected_error.message
