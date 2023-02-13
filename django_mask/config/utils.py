from typing import Optional, Tuple

from django_mask.error import Error


FILE_NOT_FOUND_MSG_TEMPLATE = "File not found by path: {}"


def load_conf_from_file(path: str) -> Tuple[str, Optional[Error]]:
    content = ""
    try:
        with open(path) as file:
            content = file.read()
    except FileNotFoundError as exc:
        error = Error(
            message=FILE_NOT_FOUND_MSG_TEMPLATE.format(path),
            exc=exc
        )
        return content, error
    return content, None
