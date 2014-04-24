#!/usr/bin/python
# -*- coding: utf-8 -*-
import pytest

from flask.ext.mailer import Email
from flask.ext.mailer.mail import Proxy
from flask.ext.mailer.mail import Address
from flask.ext.mailer.mail import Addresses


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


class TestMail:

    def test_mail_init(self, mail):
        assert mail.subject == 'Down the Rabbit-Hole'
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

    def test_cc(self, mail):
        assert mail.cc == ['cc@example.com']

    def test_cc_as_list(self, mail):
        mail.cc = ['cc@example.com', 'cc2@example.com']
        assert mail.cc == ['cc@example.com', 'cc2@example.com']

    def test_include_cc_in_recipients(self, mail):
        assert 'cc@example.com' in mail.send_to

    def test_bcc(self, mail):
        assert mail.bcc == ['bcc@example.com']

    def test_bcc_as_list(self, mail):
        mail.bcc = ['bcc@example.com', 'bcc2@example.com']
        assert mail.bcc == ['bcc@example.com', 'bcc2@example.com']

    def test_include_bcc_in_recipients(self, mail):
        assert 'bcc@example.com' in mail.send_to

    def test_dont_include_bcc_in_mail_message(self, mail):
        assert 'bcc@example.com' not in mail.format()

    def test_recipient_list_contains_only_unique_entries(self, mail):
        mail.cc = 'cc@example.com'
        assert len(mail.send_to) == 4
        mail.cc.append('cc@example.com')
        assert len(mail.send_to) == 4

    def test_add_destination_address_to_mail(self, mail):
        mail.to.append('hatter@wonderland.com')
        assert mail.send_to == ['bcc@example.com', 'hatter@wonderland.com', 'cc@example.com', 'one@example.com', 'two@example.com']

    def test_raises_error_if_mailing_parameters_is_blank(self):
        mail = Email('Dummy mail')
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
