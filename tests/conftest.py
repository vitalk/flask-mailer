#!/usr/bin/python
# -*- coding: utf-8 -*-
import pytest

from flask import Flask


def create_app(**options):
    """Create a Flask instance.

    :param **options: The additional application options.
    """
    app = Flask(__name__)
    app.config.update(options)
    return app


@pytest.fixture
def app():
    return create_app(TESTING=True)
