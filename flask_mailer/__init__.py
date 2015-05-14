#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import current_app

from flask_mailer.mail import Email
from flask_mailer.util import key
from flask_mailer.util import get_config
from flask_mailer.util import import_path


__version__ = '0.4.0'
__all__ = ('send_email', 'Mailer', 'Email')


def send_email(subject, text, to, fail_quiet=True):
    """Send an email."""
    mailer = _get_mailer()
    mail = Email(subject, text, to)
    if fail_quiet:
        return mailer.send_quiet(mail)
    return mailer.send(mail)


def _get_mailer(state=None):
    """Try to get mailer instance registered to with current application and
    raise error otherwise.
    """
    app = getattr(state, 'app', None) or current_app

    if not hasattr(app, 'extensions') or \
       'mailer' not in app.extensions:
           raise RuntimeError(
                'Mailer extension does not registered with current application'
                'or no application bound to current request'
           )

    return app.extensions['mailer']


class Mailer(object):
    """Mailer instance manages sending of email messages."""

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        config = app.config
        config.setdefault(key('testing'), app.testing)
        config.setdefault(key('host'), 'localhost')
        config.setdefault(key('port'), 25)
        config.setdefault(key('use_tls'), False)
        config.setdefault(key('username'), None)
        config.setdefault(key('password'), None)
        config.setdefault(key('default_sender'), 'webmaster')
        config.setdefault(key('backend'), 'flask_mailer.backends.smtp.SMTPMailer')

        # Use dummy mailer for testing application.
        if config[key('testing')]:
            config[key('backend')] = 'flask_mailer.backends.dummy.DummyMailer'

        state = self.init_backend(config)

        # Register extension themselves for backwards compatibility.
        app.extensions = getattr(app, 'extensions', {})
        app.extensions['mailer'] = state
        return state

    def init_backend(self, options=None):
        """Use options to create a new mailer backend."""
        options = get_config(options or {})

        backend_path = options.pop('backend', None)
        backend_class = import_path(backend_path)
        if backend_class is None:
            raise RuntimeError("Invalid backend: '%s'" % backend_path)

        return backend_class(**options)

    def __getattr__(self, name):
        return getattr(_get_mailer(self), name, None)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
