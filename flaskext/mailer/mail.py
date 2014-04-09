#!/usr/bin/python
# -*- coding: utf-8 -*-
from email.mime.text import MIMEText

from flaskext.mailer.compat import string_types, text_type


def to_list(el):
    """Force convert element to list."""
    if isinstance(el, string_types):
        el = [el,]
    return el


def utf8(s):
    return s.encode('utf-8') if isinstance(s, text_type) else s


class Address(object):
    """A wrapper for email address.

    :param address: The email address
    """

    def __init__(self, address):
        self.address = address

    def format(self):
        if isinstance(self.address, (list, tuple)):
            return u'{} <{}>'.format(*self.address)
        return self.address

    def __str__(self):
        return self.format()

    def __unicode__(self):
        return utf8(str(self))


class Email(object):
    """Base class for email messages.

    >>> mail = Email('hello, there', 'awesome message',
    ...              ['to@example.com', 'you@example.com'],
    ...              'me@example.com')
    >>> msg = mail.to_message()
    >>> msg['From']
    'me@example.com'
    >>> msg['To']
    'to@example.com, you@example.com'
    >>> msg['Subject']
    'hello, there'

    """
    def __init__(self,
                 subject,
                 text='',
                 to_addrs=None,
                 from_addr=None,
                 cc=None,
                 bcc=None,
                 reply_to=None):
        self.text = text
        self.subject = u' '.join(subject.splitlines())
        self.from_addr = from_addr
        self.cc = to_list(cc)
        self.bcc = to_list(bcc)
        self.reply_to = reply_to
        self.to_addrs = []
        to_addrs = to_list(to_addrs or [])
        map(self.add_addr, to_addrs)

    @property
    def send_to(self):
        """Returns list of recipients created from cc, bcc and to_addrs
        lists.
        """
        return set(self.to_addrs) | set(self.cc or ()) | set(self.bcc or ())

    @property
    def from_addr(self):
        return self._from_addr

    @from_addr.setter
    def from_addr(self, from_addr):
        # unpack (name, address) tuple
        if isinstance(from_addr, tuple):
            from_addr = '%s <%s>' % from_addr
        self._from_addr = from_addr

    def add_addr(self, addr):
        """Add email address to the list of recipients."""
        lines = addr.splitlines()
        if len(lines) != 1:
            raise ValueError('invalid email address value')
        self.to_addrs.append(lines[0])

    def to_message(self):
        """Returns the email as MIMEText object."""
        if not self.text or not self.subject or \
           not self.to_addrs or not self.from_addr:
            raise RuntimeError('Fill in mailing parameters first')

        msg = MIMEText(utf8(self.text))

        # really MIMEText is sucks, it does not override values on setitem,
        # it appends them. Remove some predefined fields
        del msg['Content-Type']
        del msg['Content-Transfer-Encoding']

        msg['From'] = utf8(self.from_addr)
        msg['To'] = ', '.join(map(utf8, self.send_to))
        msg['Subject'] = utf8(self.subject)
        msg['Content-Type'] = 'text/plain; charset=utf-8'
        msg['Content-Transfer-Encoding'] = '8bit'

        if self.cc:
            msg['Cc'] = ', '.join(map(utf8, self.cc))

        if self.bcc:
            msg['Bcc'] = ', '.join(map(utf8, self.bcc))

        if self.reply_to:
            msg['Reply-To'] = utf8(self.reply_to)

        return msg

    def format(self, sep='\r\n'):
        """Format message into a string."""
        return sep.join(self.to_message().as_string().splitlines())


if __name__ == '__main__':
    import doctest
    doctest.testmod()
