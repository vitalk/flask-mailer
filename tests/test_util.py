#!/usr/bin/python
# -*- coding: utf-8 -*-
import pytest

from flask.ext.mailer.util import key
from flask.ext.mailer.util import strip_prefix


def test_attach_prefix_to_key():
    assert key('host') == 'MAILER_HOST'


def test_returns_uppercased_key():
    assert key('port').isupper()


def test_strip_prefix_from_string():
    assert strip_prefix('foo', 'foobar') == 'bar'


def test_strip_prefix_from_string_only_if_it_exists():
    assert strip_prefix('baz', 'foobar') == 'foobar'
