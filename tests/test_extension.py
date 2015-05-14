#!/usr/bin/python
# -*- coding: utf-8 -*-
import pytest

from flask_mailer import Mailer
from flask_mailer import send_email
from flask_mailer.util import key

from .test_mail import mail


@pytest.fixture
def dummy(app):
    return Mailer(app)


def test_extension_register_themself_in_app(dummy, app):
    assert app.extensions['mailer'] is not None


@pytest.mark.config(backend='no.such.backend')
def test_force_use_dummy_mailer_in_test_enviroment(app):
    Mailer(app)
    assert app.config[key('backend')] == 'flask_mailer.backends.dummy.DummyMailer'


@pytest.mark.app(testing=False)
@pytest.mark.config(testing=True)
@pytest.mark.config(backend='wtf')
def test_extension_config_overrides_application_config(app):
    Mailer(app)
    assert app.config[key('backend')] == 'flask_mailer.backends.dummy.DummyMailer'


@pytest.mark.config(testing=False)
@pytest.mark.config(backend='no.such.backend')
def test_extension_raises_error_on_invalid_backend_and_not_in_test_enviroment(app):
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


def test_send_email_shortcut(app, dummy, mail):
    with app.test_request_context():
        send_email(mail.subject, mail.text, mail.to)

    assert len(dummy.outbox) == 1
    sent = dummy.outbox[0]
    assert sent.subject == mail.subject
    assert sent.text == mail.text
    assert sent.to == mail.to
