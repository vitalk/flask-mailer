#!/usr/bin/python
# -*- coding: utf-8 -*-
import pytest

from flask.ext.mailer import Mailer
from flask.ext.mailer.util import key

from .test_mail import mail


@pytest.fixture
def dummy(app):
    return Mailer(app)


def test_extension_register_themself_in_app(dummy, app):
    assert app.extensions['mailer'] is not None


def test_force_use_dummy_mailer_in_test_enviroment(app):
    app.config[key('testing')] = True
    app.config[key('backend')] = 'no.such.backend'
    Mailer(app)
    assert app.config[key('backend')] == 'flask.ext.mailer.backends.dummy.DummyMailer'


def test_extension_raises_error_on_invalid_backend_and_not_in_test_enviroment(app):
    app.config[key('testing')] = False
    app.config[key('backend')] = 'no.such.backend'
    with pytest.raises(RuntimeError) as exc:
        Mailer(app)
        assert 'Invalid backend' in exc.exconly()


def test_extension_raises_error_if_not_properly_initialized(app, mail):
    mailer = Mailer()
    err = 'Mailer extension does not registered ' \
          'with current application or' \
          'no application bound to current context'

    with pytest.raises(RuntimeError) as exc:
        mailer.send(mail)
        assert err in exc.exconly()

    with app.test_request_context():
        with pytest.raises(RuntimeError) as exc:
            mailer.send(mail)
            assert err in exc.exconly()


def test_extension_raises_error_if_no_application_bound_to_context(app, mail):
    mailer = Mailer()
    mailer.init_app(app)

    with pytest.raises(RuntimeError) as exc:
        mailer.send(mail)
        assert 'no application bound to current context' in exc.exconly()


def test_extension_use_the_application_bound_to_the_current_context(app, mail):
    mailer = Mailer()
    mailer.init_app(app)

    with app.test_request_context():
        mailer.send(mail)
        assert mailer.outbox == [mail,]


def test_extension_send_mail(dummy, mail):
    dummy.send(mail)
    assert dummy.outbox == [mail,]
