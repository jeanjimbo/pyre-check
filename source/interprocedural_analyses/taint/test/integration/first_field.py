# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# flake8: noqa

from builtins import _test_sink, _test_source


def alternate_fields():
    d = {"a": _test_source(), "b": _test_source()}
    x = d["a"] if 1 > 2 else d["b"]
    _test_sink(x)
    return x


def local_fields():
    d = alternate_fields()
    return d["c"] if 1 > 2 else d["d"]


def local_fields_hop():
    d = local_fields()
    return d["e"] if 1 > 2 else d["f"]
