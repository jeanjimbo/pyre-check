# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from builtins import _test_sink, _test_source


def concatenate_lhs(source: str):
    return f"{source}A"


def concatenate_rhs(source: str):
    return f"A{source}"


def bad_1():
    a = concatenate_lhs(_test_source())
    _test_sink(a)


def bad_2():
    a = concatenate_rhs(_test_source())
    _test_sink(a)


def either(b: bool):
    a = concatenate_lhs(_test_source()) if b else concatenate_rhs(_test_source())
    _test_sink(a)


def maybe_lhs(b: bool):
    a = concatenate_lhs(_test_source()) if b else _test_source()
    _test_sink(a)


def maybe_rhs(b: bool):
    a = _test_source() if b else concatenate_rhs(_test_source())
    _test_sink(a)


def through_iadd():
    a = _test_source()
    b = ""
    b += a
    _test_sink(b)


def format_tito(x):
    return f"a {x}"


def format_source():
    x = _test_source()
    return f"a {x}"


def format_sink(x):
    y = f"a {x}"
    _test_sink(y)
