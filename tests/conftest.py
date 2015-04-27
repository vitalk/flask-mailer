#!/usr/bin/python
# -*- coding: utf-8 -*-
import pytest

from flask import Flask
from flask_mailer.util import key


def create_app(**options):
    """Create a Flask instance. Converts option keys to upper case.

    :param **options: The additional application options.
    """
    app = Flask(__name__)

    for name, value in options.items():
        app.config[name.upper()] = value

    return app


@pytest.fixture
def app(request):
    """Use `pytest.mark` decorator to pass options to your application
    factory::

        @pytest.mark.app(static_folder='assets')
        def test_app(app):
            pass

    Set options to extension, e.g.::

        @pytest.mark.config(foo=42)
        def test_app(app):
            pass

    """
    options = dict(debug=True, testing=True, secret='secret')

    if 'app' in request.keywords:
        options.update(request.keywords['app'].kwargs)

    app = create_app(**options)

    if 'config' in request.keywords:
        for name, value in request.keywords['config'].kwargs.items():
            app.config[key(name)] = value

    return app
