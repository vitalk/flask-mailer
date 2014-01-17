#!/usr/bin/python
# -*- coding: utf-8 -*-
import pytest

from flask.ext.mailer import Email


@pytest.fixture
def mail():
    return Email('Down the Rabbit-Hole',
                 from_addr=('Alice from Wonderland', 'alice@wonderland.com'),
                 to_addrs=['one@example.com', 'two@example.com'],
                 text='What is the use of a book '
                      'without pictures or conversation?',
                 cc='cc@example.com',
                 bcc='bcc@example.com',
                 reply_to='noreply@wonderland.com')


def test_mail_init(mail):
    assert mail.subject == 'Down the Rabbit-Hole'
    assert mail.text == 'What is the use of a book without pictures or conversation?'
    assert mail.from_addr == 'Alice from Wonderland <alice@wonderland.com>'
    assert mail.to_addrs == ['one@example.com', 'two@example.com']
    assert mail.cc == ['cc@example.com']
    assert mail.bcc == ['bcc@example.com']
    assert mail.reply_to == 'noreply@wonderland.com'


def test_send_mail_to_cc_bcc_addresses(mail):
    assert mail.send_to == set(['bcc@example.com', 'cc@example.com', 'one@example.com', 'two@example.com'])
    mail.add_addr('somebody@example.com')
    assert mail.send_to == set(['bcc@example.com', 'cc@example.com', 'one@example.com', 'two@example.com', 'somebody@example.com'])


def test_no_duplicate_entries_in_recipients_list(mail):
    assert len(mail.send_to) == 4
    assert 'cc@example.com' in mail.send_to
    mail.add_addr('cc@example.com')
    assert len(mail.send_to) == 4


def test_mail_to_addr_cc_bcc_as_string():
    mail = Email('hello', to_addrs='to@example.com',
                 cc='cc@example.com', bcc='bcc@example.com')
    assert mail.send_to == set(['to@example.com', 'cc@example.com', 'bcc@example.com'])


def test_mail_to_addr_cc_bcc_as_list():
    mail = Email('hello', to_addrs=['to@example.com'],
                 cc=['cc@example.com'], bcc=['bcc@example.com'])
    assert mail.send_to == set(['to@example.com', 'cc@example.com', 'bcc@example.com'])


def test_mail_unpack_from_addr():
    mail = Email('hello', from_addr=('me', 'me@example.com'))
    assert mail.from_addr == 'me <me@example.com>'


def test_add_destination_address_to_mail(mail):
    mail.add_addr('hatter@wonderland.com')
    assert 'hatter@wonderland.com' in mail.to_addrs


def test_mail_raises_error_if_mailing_parameters_is_blank():
    mail = Email('Dummy mail')
    with pytest.raises(RuntimeError) as err:
        mail.to_message()
        assert err.message == 'Fill in mailing parameters first'


def test_mail_to_mimetext(mail):
    message = mail.to_message()
    assert message['From'] == 'Alice from Wonderland <alice@wonderland.com>'
    assert message['To'] == 'bcc@example.com, cc@example.com, one@example.com, two@example.com'
    assert message['Subject'] == 'Down the Rabbit-Hole'
    assert message['Cc'] == 'cc@example.com'
    assert message['Bcc'] == 'bcc@example.com'
    assert message['Reply-To'] == 'noreply@wonderland.com'
    assert message['Content-Type'] == 'text/plain; charset=utf-8'
    assert message['Content-Transfer-Encoding'] == '8bit'


def test_mail_to_string(mail):
    assert mail.format(sep='\n') == '''MIME-Version: 1.0
From: Alice from Wonderland <alice@wonderland.com>
To: bcc@example.com, cc@example.com, one@example.com, two@example.com
Subject: Down the Rabbit-Hole
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Cc: cc@example.com
Bcc: bcc@example.com
Reply-To: noreply@wonderland.com

What is the use of a book without pictures or conversation?'''
