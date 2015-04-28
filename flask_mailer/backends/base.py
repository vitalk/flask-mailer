#!/usr/bin/python
# -*- coding: utf-8 -*-


class Mailer(object):
    """Base email backend manager."""

    def __init__(self, **kwargs):
        pass

    def send(self, message):
        """Send the email message."""
        raise NotImplementedError

    def send_quiet(self, message):
        """Send the message but swallow exceptions."""
        raise NotImplementedError
