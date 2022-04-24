# minipyer.lib.minipyer.py
# CodeWriter21

import os as _os

from typing import Union as _Union, TextIO as _TextIO, List as _List, Callable as _Callable


class Minipyer:
    def __init__(self, *args, code: _Union[str, bytes] = None, file: _Union[str, bytes, _os.PathLike, _TextIO] = None):
        if code is None and file is None:
            raise ValueError("Either code or file must be provided")
        if code and file:
            raise ValueError("Only one of code or file can be provided")
        if code:
            if isinstance(code, str):
                self.code = code.encode("utf-8")
            self.code = code
        else:
            if isinstance(file, (str, bytes, _os.PathLike)):
                with open(file, "rb") as f:
                    self.code = f.read()
            else:
                self.code = file.read()

    __minipyers__: _List[_Callable] = []

    def minipy(self):
        code = self.code
        for minipyer in self.__minipyers__:
            code = minipyer(code)
        return code
