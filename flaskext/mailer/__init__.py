#!/usr/bin/python
# -*- coding: utf-8 -*-
from functools import wraps
from flask import current_app

from flaskext.mailer.mail import Email
from werkzeug.utils import import_string
# from flaskext.utils import import_module


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


def init_mailer(prefix=DEFAULT_PREFIX, config=None, backend=None):
    """Create new mailer from config."""
    config = config or {}
    path = backend or config.get('%s_%s' % (DEFAULT_PREFIX, 'BACKEND'))
    module_name, klass_name = path.rsplit('.', 1)
    module = import_string(module_name)
    klass = getattr(module, klass_name)
    return klass.from_settings(config, prefix + '_')


class Mailer(object):
    """Mailer instance manages sending of email messages."""

    def __init__(self, app=None, prefix=DEFAULT_PREFIX):
        self.app = app
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

        key = lambda suffix: '%s_%s' % (prefix, suffix)
        """Key function returns proper config key."""

        # set default settings
        config = app.config
        config.setdefault(key('TESTING'), app.testing)
        config.setdefault(key('HOST'), 'localhost')
        config.setdefault(key('PORT'), 25)
        config.setdefault(key('USE_TLS'), False)
        config.setdefault(key('USERNAME'), None)
        config.setdefault(key('PASSWORD'), None)
        config.setdefault(key('DEFAULT_SENDER'), 'webmaster')
        config.setdefault(key('BACKEND'), 'flaskext.mailer.backends.smtp.SMTPMailer')

        # use dummy mailer for testing config
        if config[key('TESTING')]:
            config[key('BACKEND')] = 'flaskext.mailer.backends.dummy.DummyMailer'

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
