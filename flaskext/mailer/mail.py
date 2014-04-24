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


class Proxy(object):
    """Create a proxy descriptor.

    Descriptor uses to transparently converts value to given type.

    :param type: The type to converts to
    :param attribute_name: The name of the attribute to store the converted value
    """

    def __init__(self, type, attribute_name):
        self.type = type
        self.attribute_name = attribute_name

    def __get__(self, instance, owner):
        return getattr(instance, self.attribute_name, None)

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            value = self.type(value)
        setattr(instance, self.attribute_name, value)

    def __delete__(self, instance):
        setattr(instance, self.attribute_name, None)


class Address(object):
    """A wrapper for email address.

    If address consists of two-element list, they handled as the name, email
    address pair::

    >>> Address(('Alice', 'alice@example.com')).format()
    'Alice <alice@example.com>'

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

    def __eq__(self, obj):
        if isinstance(obj, Address):
            return text_type(self) == text_type(obj)
        elif isinstance(obj, string_types):
            return text_type(self) == obj
        elif isinstance(obj, (list, tuple)):
            return text_type(self) == Address(obj)
        raise NotImplementedError('Unable to compare Address instance '
                                  'against {} instance'.format(type(obj)))

    def __ne__(self, obj):
        return not self == obj

    def __len__(self):
        return len(text_type(self))


class Addresses(list):
    """A base class for email address list.

    Transparently converts appended values to :class:`Address` instances.
    Formated list is suitable to use in mail header::

    >>> cc = Addresses(('Alice', 'alice@example.com'))
    >>> cc.append(('Bob', 'bob@example.com'))
    >>> cc.format()
    u'Alice <alice@example.com>, Bob <bob@example.com>'

    """

    def __init__(self, values=None):
        super(Addresses, self).__init__()

        if values is None:
            return
        elif isinstance(values, tuple):
            self.append(values)
            return
        elif isinstance(values, string_types):
            values = values,
        elif isinstance(values, Address):
            values = values,

        self.extend(values)

    def format(self):
        """Returns string suitable to use in mail header."""
        return ', '.join(map(text_type, self))

    def __str__(self):
        return self.format()

    def __unicode__(self):
        return utf8(str(self))

    def append(self, value):
        return self.extend([value,])

    def extend(self, iterable):
        """Extend list by appending elements from the iterable.

        Convert each value to :class:`Address` instance before extend.
        """
        values = [Address(x) if not isinstance(x, Address) else x
                  for x in iterable]
        super(Addresses, self).extend(values)


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

    from_addr = Proxy(Address, '_from_addr')
    reply_to = Proxy(Address, '_reply_to')
    bcc = Proxy(Addresses, '_bcc')
    to = Proxy(Addresses, '_to')
    cc = Proxy(Addresses, '_cc')

    def __init__(self,
                 subject,
                 text='',
                 to=None,
                 from_addr=None,
                 cc=None,
                 bcc=None,
                 reply_to=None):
        self.text = text
        self.subject = u' '.join(subject.splitlines())
        self.from_addr = from_addr
        self.to = to or []
        self.cc = cc
        self.bcc = bcc
        self.reply_to = reply_to

    @property
    def send_to(self):
        """Returns list of unique recipients of the email. List includes direct
        addressees as well as Cc and Bcc entries.
        """
        to = map(text_type, self.to)
        cc = map(text_type, self.cc or ())
        bcc = map(text_type, self.bcc or ())
        uniq = set(to) | set(cc) | set(bcc)
        return Addresses(uniq)

    def to_message(self):
        """Returns the email as MIMEText object."""
        if not self.text or not self.subject or \
           not self.to or not self.from_addr:
            raise RuntimeError('Fill in mailing parameters first')

        msg = MIMEText(utf8(self.text))

        # really MIMEText is sucks, it does not override values on setitem,
        # it appends them. Remove some predefined fields
        del msg['Content-Type']
        del msg['Content-Transfer-Encoding']

        msg['From'] = text_type(self.from_addr)
        msg['To'] = self.to.format()
        msg['Subject'] = utf8(self.subject)
        msg['Content-Type'] = 'text/plain; charset=utf-8'
        msg['Content-Transfer-Encoding'] = '8bit'

        if self.cc:
            msg['Cc'] = self.cc.format()

        if self.bcc:
            msg['Bcc'] = self.bcc.format()

        if self.reply_to:
            msg['Reply-To'] = text_type(self.reply_to)

        return msg

    def format(self, sep='\r\n'):
        """Format message into a string."""
        return sep.join(self.to_message().as_string().splitlines())


if __name__ == '__main__':
    import doctest
    doctest.testmod()
