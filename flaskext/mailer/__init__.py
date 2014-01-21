#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import current_app

from flaskext.mailer.mail import Email
from flask.ext.mailer.util import key
from flask.ext.mailer.util import import_path


__all__ = ('get_mailer', 'send_email', 'Mailer', 'Email')

DEFAULT_PREFIX = 'MAILER'


def send_email(subject, text, to_addrs, fail_quiet=True, prefix=DEFAULT_PREFIX):
    """Send an email."""
    mailer = get_mailer(prefix)
    mail = Email(subject, text, to_addrs)
    if fail_quiet:
        return mailer.send_quiet(mail)
    return mailer.send(mail)


def get_mailer(prefix=DEFAULT_PREFIX):
    """Returns mailer for current app or raise RuntimeError."""
    app = current_app

    if not hasattr(app, 'extensions') or \
       'mailer' not in app.extensions:
        raise RuntimeError('Mailer extension does not registered')

    mailer = app.extensions['mailer'].get(prefix)
    if mailer is None:
        raise RuntimeError('Mailer with prefix "%s" does not exist' % prefix)
    return mailer


def init_mailer(prefix, config=None):
    """Create new mailer from config."""
    config = config or {}
    path = config.pop(key('backend'), None)
    cls = import_path(path)
    if cls is None:
        raise RuntimeError("Invalid backend: '%s'" % path)

    return cls(**config)


class Mailer(object):
    """Mailer instance manages sending of email messages."""

    def __init__(self, app=None, prefix=DEFAULT_PREFIX):
        if app is not None:
            self.init_app(app, prefix)

    def init_app(self, app, prefix=DEFAULT_PREFIX):
        # register extension themselves for backwards compatibility
        app.extensions = getattr(app, 'extensions', {})
        app.extensions['mailer'] = getattr(app.extensions, 'mailer', {})
        if prefix in app.extensions['mailer']:
            raise RuntimeError('duplicate config prefix: "%s"' % prefix)

        self.app = app
        self.prefix = prefix


        # set default settings
        config = app.config
        config.setdefault(key('testing'), app.testing)
        config.setdefault(key('host'), 'localhost')
        config.setdefault(key('port'), 25)
        config.setdefault(key('use_tls'), False)
        config.setdefault(key('username'), None)
        config.setdefault(key('password'), None)
        config.setdefault(key('default_sender'), 'webmaster')
        config.setdefault(key('backend'), 'flask.ext.mailer.backends.smtp.SMTPMailer')

        # use dummy mailer for testing config
        if config[key('testing')]:
            config[key('backend')] = 'flask.ext.mailer.backends.dummy.DummyMailer'

        mailer = init_mailer(prefix, config)
        app.extensions['mailer'][prefix] = mailer

    def send(self, mail):
        """Send the email message."""
        get_mailer(self.prefix).send(mail)

    def send_quiet(self, mail):
        """Send the email message but swallow exceptions."""
        get_mailer(self.prefix).send_quiet(mail)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
