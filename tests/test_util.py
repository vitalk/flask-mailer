#!/usr/bin/python
# -*- coding: utf-8 -*-
import pytest

from flask.ext.mailer.util import key
from flask.ext.mailer.util import import_path
from flask.ext.mailer.util import strip_prefix


def test_attach_prefix_to_key():
    assert key('host') == 'MAILER_HOST'


def test_returns_uppercased_key():
    assert key('port').isupper()


def test_strip_prefix_from_string():
    assert strip_prefix('foo', 'foobar') == 'bar'


def test_strip_prefix_from_string_only_if_it_exists():
    assert strip_prefix('baz', 'foobar') == 'foobar'


def test_import_path_returns_none_if_path_is_empty():
    assert import_path('') is None


def test_import_path_swallow_import_errors():
    assert import_path('no.such.path') is None


def test_import_path_returns_the_last_name_in_path():
    assert import_path('flask.ext.mailer.util.import_path') is import_path
