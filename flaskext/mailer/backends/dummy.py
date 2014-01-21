#!/usr/bin/python
# -*- coding: utf-8 -*-
from flaskext.mailer.backends.base import Mailer


class DummyMailer(Mailer):
    """Dummy mailing instance for unittests.

    Keeps all sent messages in *oubox* list.
    """
    def __init__(self, **kwargs):
        self.outbox = []

    def send(self, message):
        """Sending a message to the dummy *outbox*."""
        self.outbox.append(message)

    def send_quiet(self, message):
        """Actually don't swallow exception."""
        self.send(message)
