#!/usr/bin/python
# -*- coding: utf-8 -*-
import pytest

from flask_mailer.compat import text_type
from flask_mailer.backends.base import Mailer
from flask_mailer.backends.smtp import SMTPMailer
from flask_mailer.backends.dummy import DummyMailer

from .test_mail import mail


@pytest.fixture
def smtp():
    return SMTPMailer()


@pytest.fixture
def dummy():
    return DummyMailer()


@pytest.fixture
def base():
    return Mailer()


def test_base_mailer_does_not_implement_send_method(base):
    with pytest.raises(NotImplementedError):
        base.send(None)


def test_base_mailer_does_not_implement_send_quiet_method(base):
    with pytest.raises(NotImplementedError):
        base.send_quiet(None)


def test_dummy_mailer_push_send_messages_into_outbox(dummy, mail):
    dummy.send(mail)
    assert dummy.outbox == [mail,]


def test_smtp_missed_password(recwarn):
    smtp = SMTPMailer(username='me')
    w = recwarn.pop()
    assert text_type(w.message) == (
        'Invalid credentials. Please setup both username and '
        'password or neither.'
    )
    assert smtp.username is None


def test_smtp_missed_password(recwarn):
    smtp = SMTPMailer(password='pass')
    w = recwarn.pop()
    assert text_type(w.message) == (
        'Invalid credentials. Please setup both username and '
        'password or neither.'
    )
    assert smtp.password is None


def test_smtp_default_options(smtp):
    assert smtp.host == 'localhost'
    assert smtp.port == 25
    assert not smtp.use_tls
    assert smtp.username is None
    assert smtp.password is None
    assert smtp.default_sender is None


def test_smtp_raises_error_on_send_if_no_smtp_server_is_available(smtp, mail):
    with pytest.raises(RuntimeError):
        smtp.send(mail)


def test_smtp_swallow_errors_on_send_quiet(smtp, mail):
    smtp.send_quiet(mail)
