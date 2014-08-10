#!/usr/bin/python
# -*- coding: utf-8 -*-
import pytest

from flask import Flask


def create_app(**options):
    """Create a Flask instance. Converts option keys to upper case.

    :param **options: The additional application options.
    """
    app = Flask(__name__)

    for name, value in options.items():
        app.config[name.upper()] = value

    return app


@pytest.fixture
def app():
    return create_app(testing=True)
