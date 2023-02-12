from mask.handlers import mask_name


def test_mask_name():
    name = "Albert"
    assert mask_name(name) == name
