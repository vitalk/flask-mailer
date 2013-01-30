#!/usr/bin/python
# -*- coding: utf-8 -*-
from flaskext.mailer import key


class Mailer(object):
    """Base email backend manager."""

    def send(self, message):
        """Send the email message."""
        raise NotImplementedError

    def send_quiet(self, message):
        """Send the message but swallow exceptions."""
        raise NotImplementedError

    @classmethod
    def from_settings(cls, settings, prefix, allowed_kwds=None):
        """Returns new mailer instance from settings dict."""
        settings = settings or {}
        allowed_kwds = allowed_kwds or []

        to_lower = lambda x: str(x).lower()
        not_suffix = len(prefix) + 1

        kwds_names = [to_lower(key(prefix, suffix)) for suffix in allowed_kwds]

        kwds = {to_lower(k[not_suffix:]): settings[k] for k in settings if
                to_lower(k) in kwds_names}

        return cls(**kwds)
