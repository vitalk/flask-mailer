#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import current_app

from flaskext.mailer.mail import Email
from flask.ext.mailer.util import key
from flask.ext.mailer.util import get_config
from flask.ext.mailer.util import import_path


__version__ = '0.3.7'
__all__ = ('get_mailer', 'send_email', 'Mailer', 'Email')


def send_email(subject, text, to, fail_quiet=True):
    """Send an email."""
    mailer = get_mailer(None)
    mail = Email(subject, text, to)
    if fail_quiet:
        return mailer.send_quiet(mail)
    return mailer.send(mail)


def get_mailer(state):
    """Returns mailer for current app or raise RuntimeError."""
    app = getattr(state, 'app', None) or current_app

    if not hasattr(app, 'extensions') or \
       'mailer' not in app.extensions:
        raise RuntimeError('Mailer extension does not registered '
                           'with current application or no application bound '
                           'to current context')

    return app.extensions['mailer']


def init_mailer(options=None):
    """Create a new mailer from options."""
    options = get_config(options or {})

    path = options.pop('backend', None)
    backend_class = import_path(path)
    if backend_class is None:
        raise RuntimeError("Invalid backend: '%s'" % path)

    return backend_class(**options)


class Mailer(object):
    """Mailer instance manages sending of email messages."""

    def __init__(self, app=None):
        self.app = app
        self.state = None if app is None else self.init_app(app)

    def init_app(self, app):
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

        state = init_mailer(config)

        # register extension themselves for backwards compatibility
        app.extensions = getattr(app, 'extensions', {})
        app.extensions['mailer'] = state
        return state

    def __getattr__(self, name):
        return getattr(get_mailer(self), name, None)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
