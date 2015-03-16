#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
from smtplib import SMTP, SMTPException

from flaskext.mailer.backends.base import Mailer
from flaskext.mailer.compat import text_type


class SMTPMailer(Mailer):
    """SMTP email backend."""
    def __init__(self,
                 host='localhost',
                 port=25,
                 username=None,
                 password=None,
                 default_sender=None,
                 use_tls=False,
                 **kwargs):
        self.host = host
        self.port = port
        self.use_tls = use_tls
        self.username = username
        self.password = password
        self.default_sender = default_sender

        auth = (username, password)
        if any(auth) and not all(auth):
            raise RuntimeError('Please setup both USERNAME and PASSWORD or neither')

    def __enter__(self):
        """Acquires the connection to SMTP server."""
        try:
            connection = self.connection = SMTP(self.host, self.port)
            if self.username and self.password:
                connection.login(self.username, self.password)
            if self.use_tls:
                connection.ehlo()
                connection.starttls()
                connection.ehlo()
        except (SMTPException, socket.error) as e:
            raise RuntimeError(str(e))
        return connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Releases the exciting connection to SMTP server."""
        try:
            try:
                self.connection.quit()
            except socket.sslerror:
                # This happens when calling quit() on a TLS connection
                # sometimes.
                self.connection.close()
            except:
                return False
        finally:
            self.connection = None
            return True

    def send(self, message):
        """Send the message."""
        with self as con:
            message.from_addr = message.from_addr or self.default_sender
            con.sendmail(text_type(message.from_addr),
                         text_type(message.send_to),
                         message.format())

    def send_quiet(self, message):
        """Send the message but swallow exceptions."""
        try:
            return self.send(message)
        except Exception:
            return


if __name__ == '__main__':
    import doctest
    doctest.testmod()
