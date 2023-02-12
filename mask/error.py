import sys
from typing import Optional


class Error:

    def __init__(self, msg: str, exc: Optional[Exception] = None) -> None:
        self.__msg = msg
        self.__exception = exc

    def display(self) -> None:
        sys.stderr.write(self.__msg)

    def raise_exception(self):
        if isinstance(self.__exception, Exception):
            raise self.__exception
