#!/usr/bin/python
# -*- coding: utf-8 -*-
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr
from email.utils import formataddr

from flaskext.mailer.compat import string_types, text_type, unicode_compatible


def to_list(el):
    """Force convert element to list."""
    if isinstance(el, string_types):
        el = [el,]
    return el


def utf8(s):
    return s.encode('utf-8') if isinstance(s, text_type) else s


def contains_nonascii_characters(raw):
    return not all(ord(c) < 128 for c in raw)


def rfc_compliant(s, encoding):
    """Encode a header string into RFC-compliant format. Do not modify
    string if is contains only ascii letters.
    """
    if contains_nonascii_characters(s):
        return Header(s, encoding).encode()
    return s


def sanitize_address(addr, encoding='utf-8'):
    """Sanitize email address into RFC 2822-compliant string.

    Adopted version from Django mail package
    (https://github.com/django/django/blob/master/django/core/mail/message.py).

    :param addr: The address to process.
    :param encoding: The character set that the address was encoded in.
    """
    if isinstance(addr, string_types):
        addr = parseaddr(addr)
    nm, addr = addr

    try:
        nm = rfc_compliant(nm, encoding)
    except UnicodeEncodeError:
        nm = rfc_compliant(nm, 'utf-8')

    try:
        addr.encode('ascii')
    except UnicodeEncodeError:
        if '@' in addr:
            localpart, domain = addr.split('@', 1)
            localpart = rfc_compliant(localpart, encoding)
            domain = domain.encode('idna').decode('ascii')
            addr = '@'.join([localpart, domain])
        else:
            addr = rfc_compliant(addr, encoding)

    return ''.join(formataddr((nm, addr)).splitlines())


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


@unicode_compatible
class SafeHeader(object):
    """A wrapper for RFC 2822-compliant header.

    >>> str(SafeHeader('Hello!'))
    'Hello!'

    Strips any newline characters to prevent header injection::

    >>> str(SafeHeader('No \n\rmore header injection!'))
    'No more header injection!'

    Encode string if it contains nonascii characters::

    >>> str(SafeHeader(u'Привет', encoding='cp1251'))
    '=?cp1251?b?z/Do4uXy?='

    :param value: The initial header value.
    :param encoding: The character set that the header was encoded in.
    """
    def __init__(self, value='', encoding='utf-8'):
        self.value = value
        self.encoding = encoding

    def __str__(self):
        if isinstance(self.value, string_types):
            return rfc_compliant(''.join(self.value.splitlines()), self.encoding)
        return text_type(self.value)

    def __nonzero__(self):
        return isinstance(self.value, string_types) and bool(self.value)


@unicode_compatible
class Address(object):
    """A wrapper for email address.

    Perform sanitizing and formating email address. Formated address
    RFC 2822-compliant and suitable to use in internationalized email headers::

    >>> str(Address(u'álice@example.com'))
    '=?utf-8?b?w6FsaWNl?=@example.com'

    If address consists of two-element list, they handled as the name, email
    address pair::

    >>> str(Address(('Alice', 'alice@example.com')))
    'Alice <alice@example.com>'

    :param address: The email address
    """

    def __init__(self, address):
        self.address = address

    def __str__(self):
        return sanitize_address(self.address)

    def __nonzero__(self):
        return bool(self.address)

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


@unicode_compatible
class Addresses(list):
    """A base class for email address list.

    Transparently converts appended values to :class:`Address` instances.
    Formated list is suitable to use in mail header::

    >>> cc = Addresses(('Alice', 'alice@example.com'))
    >>> cc.append(('Bob', 'bob@example.com'))
    >>> str(cc)
    'Alice <alice@example.com>, Bob <bob@example.com>'

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

    def __str__(self):
        return ', '.join(map(text_type, self))

    def append(self, value):
        return self.extend([value,])

    def extend(self, iterable):
        """Extend list by appending elements from the iterable.

        Convert each value to :class:`Address` instance before extend.
        """
        values = [Address(x) if not isinstance(x, Address) else x
                  for x in iterable]
        super(Addresses, self).extend(values)


@unicode_compatible
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

    subject = Proxy(SafeHeader, '_subject')
    from_addr = Proxy(Address, '_from_addr')
    reply_to = Proxy(Address, '_reply_to')
    bcc = Proxy(Addresses, '_bcc')
    to = Proxy(Addresses, '_to')
    cc = Proxy(Addresses, '_cc')

    def __init__(self,
                 subject=None,
                 text=None,
                 to=None,
                 from_addr=None,
                 cc=None,
                 bcc=None,
                 reply_to=None):
        self.text = text
        self.subject = subject
        self.from_addr = from_addr
        self.to = to
        self.cc = cc
        self.bcc = bcc
        self.reply_to = reply_to

    @property
    def send_to(self):
        """Returns list of unique recipients of the email. List includes direct
        addressees as well as Cc and Bcc entries.
        """
        to = map(text_type, self.to)
        cc = map(text_type, self.cc)
        bcc = map(text_type, self.bcc)
        uniq = set(to) | set(cc) | set(bcc)
        return Addresses(uniq)

    def to_message(self):
        """Returns the email as MIMEText object."""
        if not self.text or not self.subject or \
           not self.to or not self.from_addr:
            raise ValueError('Fill in mailing parameters first')

        msg = MIMEText(utf8(self.text))

        # really MIMEText is sucks, it does not override values on setitem,
        # it appends them. Remove some predefined fields
        del msg['Content-Type']
        del msg['Content-Transfer-Encoding']

        msg['From'] = text_type(self.from_addr)
        msg['To'] = text_type(self.to)
        msg['Subject'] = text_type(self.subject)
        msg['Content-Type'] = 'text/plain; charset=utf-8'
        msg['Content-Transfer-Encoding'] = '8bit'

        if self.cc:
            msg['Cc'] = text_type(self.cc)

        if self.reply_to:
            msg['Reply-To'] = text_type(self.reply_to)

        return msg

    def format(self, sep='\r\n'):
        """Format message into a string."""
        return sep.join(self.to_message().as_string().splitlines())

    def __str__(self):
        return self.format(sep='\n')


if __name__ == '__main__':
    import doctest
    doctest.testmod()
