#!/usr/bin/python
# -*- coding: utf-8 -*-
import pytest

from flask.ext.mailer.util import key


def test_attach_prefix_to_key():
    assert key('host') == 'MAILER_HOST'


def test_returns_uppercased_key():
    assert key('port').isupper()
