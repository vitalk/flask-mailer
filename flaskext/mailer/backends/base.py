#!/usr/bin/python
# -*- coding: utf-8 -*-


class Mailer(object):
    """Base email backend manager."""
    def __init__(self, fail_quiet=False, **kwds):
        self.fail_quiet = fail_quiet

    def send(self, message):
        """Send the email message."""
        raise NotImplementedError

    def send_quiet(self, message):
        """Send the message but swallow exceptions."""
        raise NotImplementedError

    @classmethod
    def from_settings(cls, settings, prefix='MAILER_', allowed_kwds=None):
        """Returns new mailer instance from settings dict."""
        settings = settings or {}
        allowed_kwds = allowed_kwds or []

        to_lower = lambda x: str(x).lower()
        size = len(prefix)

        kwds_names = [to_lower(prefix + suffix) for suffix in allowed_kwds]

        kwds = {to_lower(k[size:]): settings[k] for k in settings if
                to_lower(k) in kwds_names}

        return cls(**kwds)
