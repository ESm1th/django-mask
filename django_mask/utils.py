from importlib import import_module

from django_mask.error import (
    file_not_found_error,
    module_has_not_attribute_error,
    import_model_error
)


def load_config_from_file(path):
    content = ""
    try:
        with open(path) as file:
            content = file.read()
    except FileNotFoundError as exc:
        error = file_not_found_error(path, exc)
        return content, error
    return content, None


def import_model(path):
    splitted = path.split(".")
    model_str = splitted[-1]
    slice_idx = splitted.index(model_str)
    module_path_str = ".".join(splitted[:slice_idx])
    try:
        module = import_module(module_path_str)
        try:
            model = getattr(module, model_str)
            return model, None
        except AttributeError as exc:
            error = module_has_not_attribute_error(module_path_str, model_str, exc)
            return None, error
    except (ImportError, ValueError) as exc:
        error = import_model_error(path, exc)
        return None, error
