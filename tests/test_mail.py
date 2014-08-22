#!/usr/bin/python
# -*- coding: utf-8 -*-
import pytest

from flask.ext.mailer import Email
from flask.ext.mailer.mail import Proxy
from flask.ext.mailer.mail import Address
from flask.ext.mailer.mail import Addresses
from flask.ext.mailer.mail import SafeHeader
from flask.ext.mailer.compat import text_type


@pytest.fixture(params=[None, ''])
def falsy(request):
    return request.param


@pytest.fixture
def dummy():
    return Email('Subject', from_addr='from@example.com',
                 to='to@example.com', text='Plain text')


@pytest.fixture
def mail():
    return Email('Down the Rabbit-Hole',
                 from_addr=('Alice from Wonderland', 'alice@wonderland.com'),
                 to=['one@example.com', 'two@example.com'],
                 text='What is the use of a book '
                      'without pictures or conversation?',
                 cc='cc@example.com',
                 bcc='bcc@example.com',
                 reply_to='noreply@wonderland.com')


@pytest.fixture
def alice():
    return Address('alice@example.com')


class TestAddress:

    def test_address_init(self, alice):
        assert alice.address == 'alice@example.com'
        assert alice.format() == 'alice@example.com'
        assert unicode(alice) == u'alice@example.com'
        assert str(alice) == 'alice@example.com'

    def test_unpack_address_from_list(self):
        addr = Address(['Alice', 'alice@example.com'])
        assert addr.format() == u'Alice <alice@example.com>'

    def test_unpack_address_from_tuple(self):
        addr = Address(('Alice', 'alice@example.com'))
        assert addr.format() == u'Alice <alice@example.com>'

    def test_compare_addresses(self, alice):
        assert alice == Address('alice@example.com')

    def test_compare_address_and_unicode(self, alice):
        assert alice == u'alice@example.com'

    def test_compare_address_and_list(self):
        addr = ('Alice', 'alice@example.com')
        assert Address(addr) == addr

    def test_compare_address_and_tuple(self):
        addr = ['Alice', 'alice@example.com']
        assert Address(addr) == addr

    def test_address_is_truly_when_value_is_truly(self):
        addr = Address('alice@example.com')
        assert addr
        addr = Address(None)
        assert not addr

    def test_encode_nonascii_strings(self):
        addr = Address((u'Álice', u'alice@example.com'))
        assert addr.format() == '=?utf-8?b?w4FsaWNl?= <alice@example.com>'

    def test_strip_newlines_from_address(self):
        addr = Address(('Alice\n', 'alice\r\n@example.com\r'))
        assert addr.format() == 'Alice <alice@example.com>'


class TestAddresses(object):

    addresses = Proxy(Addresses, '_addresses')

    def setup(self):
        self.addresses = Addresses()

    def test_init(self):
        assert self.addresses == []

    def test_assign_single_address(self):
        address = 'alice@example.com'
        self.addresses = address
        assert self.addresses == [address,]
        assert self.addresses.format() == address

    def test_assign_list_of_addresses(self):
        addresses = ['alice@example.com', 'bob@example.com']
        self.addresses = addresses
        assert self.addresses == addresses
        assert self.addresses.format() == ', '.join(addresses)

    def test_assign_list_of_named_addresses(self):
        named_address = ('Alice', 'alice@example.com')
        self.addresses = [named_address,]
        assert self.addresses == [named_address,]
        assert self.addresses.format() == 'Alice <alice@example.com>'

    def test_assign_address_instance(self, alice):
        self.addresses = alice
        assert self.addresses == [alice,]
        assert self.addresses.format() == alice.format()

    def test_append_value_to_list(self):
        self.addresses.append('alice@example.com')
        assert self.addresses.format() == 'alice@example.com'

    def test_append_address_instance_to_list(self, alice):
        self.addresses.append(alice)
        assert self.addresses.format() == 'alice@example.com'

    def test_append_named_address_to_list(self):
        self.addresses.append(['Alice', 'alice@example.com'])
        assert self.addresses.format() == 'Alice <alice@example.com>'


class TestSafeHeader(object):

    subject = Proxy(SafeHeader, '_subject')

    def setup(self):
        self.subject = SafeHeader()

    def test_init(self):
        assert self.subject.value == ''
        assert self.subject.encoding == 'utf-8'

    def test_string_representation(self):
        assert text_type(self.subject) == ''
        self.subject = 'Hello'
        assert text_type(self.subject) == 'Hello'

    def test_header_is_falsy_when_value_is_falsy(self, falsy):
        self.subject = falsy
        assert not self.subject

    def test_header_is_truly_when_value_is_truly(self):
        self.subject = 'Hello'
        assert self.subject

    def test_use_encoding_to_encode_nonascii_characters(self):
        self.subject = u'Привет'
        assert text_type(self.subject) == '=?utf-8?b?0J/RgNC40LLQtdGC?='
        self.subject.encoding = 'cp1251'
        assert text_type(self.subject) == '=?cp1251?b?z/Do4uXy?='

    def test_prevent_header_injection(self):
        self.subject = 'Hello\r\n'
        assert text_type(self.subject) == 'Hello'


class TestMail:

    def test_mail_init(self, mail):
        assert text_type(mail.subject) == 'Down the Rabbit-Hole'
        assert mail.text == 'What is the use of a book without pictures or conversation?'
        assert mail.from_addr == 'Alice from Wonderland <alice@wonderland.com>'
        assert mail.to == ['one@example.com', 'two@example.com']
        assert mail.cc == ['cc@example.com']
        assert mail.bcc == ['bcc@example.com']
        assert mail.reply_to == 'noreply@wonderland.com'

    def test_from_addr(self, mail):
        mail.from_addr = 'alice@example.com'
        assert mail.from_addr == 'alice@example.com'

    def test_unpack_from_addr(self, mail):
        mail.from_addr = ['Alice', 'alice@example.com']
        assert mail.from_addr == 'Alice <alice@example.com>'

    def test_reply_to(self, mail):
        mail.reply_to = 'noreply@example.com'
        assert mail.reply_to == 'noreply@example.com'

    def test_unpack_reply_to(self, mail):
        mail.reply_to = ('Alice', 'noreply@example.com')
        assert mail.reply_to == 'Alice <noreply@example.com>'

    def test_dont_include_reply_to_in_mail_message_if_not_set(self, mail):
        mail.reply_to = None
        assert not mail.reply_to
        assert 'Reply-To:' not in mail.format()

    def test_cc(self, mail):
        assert mail.cc == ['cc@example.com']

    def test_cc_as_list(self, mail):
        mail.cc = ['cc@example.com', 'cc2@example.com']
        assert mail.cc == ['cc@example.com', 'cc2@example.com']

    def test_include_cc_in_recipients(self, mail):
        assert 'cc@example.com' in mail.send_to

    def test_empty_cc(self, dummy):
        assert dummy.cc == []

    def test_dont_include_cc_to_mail_message_if_not_set(self, dummy):
        assert 'Cc:' not in dummy.format()

    def test_bcc(self, mail):
        assert mail.bcc == ['bcc@example.com']

    def test_bcc_as_list(self, mail):
        mail.bcc = ['bcc@example.com', 'bcc2@example.com']
        assert mail.bcc == ['bcc@example.com', 'bcc2@example.com']

    def test_include_bcc_in_recipients(self, mail):
        assert 'bcc@example.com' in mail.send_to

    def test_dont_include_bcc_in_mail_message(self, mail):
        assert 'bcc@example.com' not in mail.format()

    def test_empty_bcc(self, dummy):
        assert dummy.bcc == []

    def test_recipient_list_contains_only_unique_entries(self, mail):
        mail.cc = 'cc@example.com'
        assert len(mail.send_to) == 4
        mail.cc.append('cc@example.com')
        assert len(mail.send_to) == 4

    def test_add_destination_address_to_mail(self, mail):
        mail.to.append('hatter@wonderland.com')
        assert mail.send_to == ['bcc@example.com', 'hatter@wonderland.com', 'cc@example.com', 'one@example.com', 'two@example.com']

    def test_raises_error_if_mailing_parameters_is_blank(self):
        mail = Email()
        with pytest.raises(RuntimeError) as err:
            mail.to_message()
            assert err.message == 'Fill in mailing parameters first'

    def test_mail_to_mimetext(self, mail):
        message = mail.to_message()
        assert message['From'] == 'Alice from Wonderland <alice@wonderland.com>'
        assert message['To'] == 'one@example.com, two@example.com'
        assert message['Subject'] == 'Down the Rabbit-Hole'
        assert message['Cc'] == 'cc@example.com'
        assert message['Reply-To'] == 'noreply@wonderland.com'
        assert message['Content-Type'] == 'text/plain; charset=utf-8'
        assert message['Content-Transfer-Encoding'] == '8bit'

    def test_mail_contains_nonascii_characters(self, mail):
        mail.subject = u'Привет'
        assert 'Subject: =?utf-8?b?0J/RgNC40LLQtdGC?=' in mail.format()
        mail.from_addr = (u'Álice', u'álice@example.com')
        assert 'From: =?utf-8?b?w4FsaWNl?= <=?utf-8?b?w6FsaWNl?=@example.com>' in mail.format()
        mail.cc = (u'ćć', 'cc@example.com')
        assert 'Cc: =?utf-8?b?xIfEhw==?= <cc@example.com>' in mail.format()
        mail.reply_to = (u'nóréply', 'noreply@example.com')
        assert 'Reply-To: =?utf-8?b?bsOzcsOpcGx5?= <noreply@example.com>' in mail.format()
        mail.to = ['á <a@example.com>', u'ä <aa@example.com>']
        assert 'To: =?utf-8?b?w6E=?= <a@example.com>, =?utf-8?b?w6Q=?= <aa@example.com>' in mail.format()

    def test_mail_to_string(self, mail):
        assert mail.format(sep='\n') == '''\
MIME-Version: 1.0
From: Alice from Wonderland <alice@wonderland.com>
To: one@example.com, two@example.com
Subject: Down the Rabbit-Hole
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Cc: cc@example.com
Reply-To: noreply@wonderland.com

What is the use of a book without pictures or conversation?'''
