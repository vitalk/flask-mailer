#!/usr/bin/python
# -*- coding: utf-8 -*-
import pytest

from flask_mailer.mail import Proxy


class Foo(object):
    def __init__(self, value):
        self.value = value

class Bar(object):
    foo = Proxy(Foo, '_foo')


@pytest.fixture
def bar():
    return Bar()


class TestProxy:

    def test_get(self, bar):
        assert bar.foo is None

    def test_set(self, bar):
        bar.foo = 42
        assert isinstance(bar.foo, Foo)
        assert bar.foo.value == 42

        bar.foo = Foo(1)
        assert bar.foo.value == 1

    def test_delete(self, bar):
        bar.foo = 42
        del bar.foo
        assert bar.foo is None
