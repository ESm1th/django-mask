import sys


FILE_NOT_FOUND_MSG_TEMPLATE = "Error: file not found by path: {}"
MODULE_HAS_NOT_ATTRIBUTE = "Error: module \"{}\" has not attribute \"{}\""
IMPORT_ERROR = "Error: cannot import by string \"{}\""
INVALID_FILE_CONTENT_FORMAT = "Error: invalid file content format"


class Error:

    def __init__(self, msg, exc=None):
        self.__msg = msg
        self.__exception = exc

    @property
    def message(self):
        return self.__msg

    def display(self):
        sys.stderr.write(self.__msg)

    def raise_exception(self):
        if isinstance(self.__exception, Exception):
            raise self.__exception


def file_not_found_error(path, exc=None):
    return Error(
        FILE_NOT_FOUND_MSG_TEMPLATE.format(path),
        exc=exc
    )


def module_has_not_attribute_error(module_path_str, model_str, exc=None):
    return Error(
        MODULE_HAS_NOT_ATTRIBUTE.format(module_path_str, model_str),
        exc=exc
    )


def import_model_error(path, exc):
    return Error(
        IMPORT_ERROR.format(path),
        exc=exc
    )


def invalid_file_content_error(exc=None):
    return Error(
        INVALID_FILE_CONTENT_FORMAT,
        exc=exc
    )
