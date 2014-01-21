#!/usr/bin/python
# -*- coding: utf-8 -*-
import pytest

from flask.ext.mailer import Mailer
from flask.ext.mailer.util import key
from flask.ext.mailer.util import get_config
from flask.ext.mailer.util import import_path
from flask.ext.mailer.util import strip_prefix

@pytest.fixture
def config(app):
    Mailer(app)
    return app.config


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


def test_get_config_convert_keys_to_lowercase(config):
    for key, value in get_config(config).items():
        assert key.islower()


def test_get_config_trim_prefixes_from_config_keys(config):
    assert get_config(config) == {
            'backend': 'flask.ext.mailer.backends.dummy.DummyMailer',
            'default_sender': 'webmaster',
            'host': 'localhost',
            'password': None,
            'port': 25,
            'testing': True,
            'use_tls': False,
            'username': None }
