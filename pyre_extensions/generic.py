# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# pyre-ignore-all-errors
import sys
from typing import Any


# We export this metaclass because Concatenate depends on it.
class GenericMeta(type):
    def __getitem__(self, *args) -> Any:
        return self.__class__(self.__name__, self.__bases__, dict(self.__dict__))


if sys.version_info >= (3, 7):

    class Generic:
        """Pyre's variadic-supporting substitute for `typing.Generic`.

        By using `__class_getitem__`, this avoids a metaclass, which prevents
        ugly metaclass conflicts when a child class is generic and a base class
        has some metaclass."""

        def __class_getitem__(cls, *args: object) -> Any:
            return cls

else:

    class Generic(metaclass=GenericMeta):
        """Pyre's variadic-supporting substitute for `typing.Generic`."""

        pass
