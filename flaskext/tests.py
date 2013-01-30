#!/usr/bin/python
# -*- coding: utf-8 -*-
from attest import Tests, AssertImportHook, raises, assert_hook

# disable assert hook before load flask app, while pull-request will be
# accepted https://github.com/dag/attest/pull/136
AssertImportHook.disable()

from flask import Flask
from flaskext.mailer import get_mailer
from flaskext.mailer.mail import Email


mail = Tests()


@mail.test
def mail_init():
    mail = Email('hello', 'awesome message',
                 to_addrs=['to@you', 'you@again'],
                 from_addr='from@me')
    assert mail.text == 'awesome message'
    assert mail.subject == 'hello'
    assert mail.from_addr == 'from@me'
    assert mail.to_addrs == ['to@you', 'you@again']


@mail.test
def mail_send_to():
    mail = Email('hello', to_addrs='to@example.com',
                 cc='cc@example.com', bcc='bcc@example.com')
    assert len(mail.send_to) == 3
    mail.add_addr('cc@example.com')
    assert len(mail.send_to) == 3
    mail.add_addr('somebody@example.com')
    assert len(mail.send_to) == 4


@mail.test
def mail_to_addr_cc_bcc_as_string():
    mail = Email('hello', to_addrs='to@example.com',
                 cc='cc@example.com', bcc='bcc@example.com')
    assert mail.send_to == set(['to@example.com', 'cc@example.com', 'bcc@example.com'])


@mail.test
def mail_to_addr_cc_bcc_as_list():
    mail = Email('hello', to_addrs=['to@example.com'],
                 cc=['cc@example.com'], bcc=['bcc@example.com'])
    assert mail.send_to == set(['to@example.com', 'cc@example.com', 'bcc@example.com'])


@mail.test
def mail_unpack_from_addr():
    mail = Email('hello', from_addr=('me', 'me@example.com'))
    assert mail.from_addr == 'me <me@example.com>'


@mail.test
def mail_add_to_addrs():
    mail = Email('hello')
    assert len(mail.to_addrs) == 0
    mail.add_addr('to@example.com')
    assert len(mail.to_addrs) == 1
    assert mail.to_addrs == ['to@example.com']


@mail.test
def mail_to_message():
    mail = Email('subject', 'awesome message',
                 to_addrs=['to@example.com', 'somebody@example.com'],
                 cc='cc@example.com', bcc='bcc@example.com',
                 from_addr='me@example.com',
                 reply_to='somebodyelse@example.com')
    msg = mail.to_message()
    assert msg['From'] == 'me@example.com'
    assert msg['To'] == 'to@example.com, cc@example.com, bcc@example.com, somebody@example.com'
    assert msg['Subject'] == 'subject'
    assert msg['Content-Type'] == 'text/plain; charset=utf-8'
    assert msg['Content-Transfer-Encoding'] == '8bit'
    assert msg['Bcc'] == 'bcc@example.com'
    assert msg['Cc'] == 'cc@example.com'
    assert msg['Reply-To'] == 'somebodyelse@example.com'


@mail.test
def mail_to_message_with_blank_mailing_params():
    mail = Email('hello')
    with raises(RuntimeError) as e:
        mail.to_message()
        assert e.message == 'Fill in mailing parameters first'


base = Tests()


@base.test
def base_nonimplemented_methods():
    from flaskext.mailer.backends.base import Mailer
    mailer = Mailer()
    with raises(NotImplementedError):
        mailer.send(None)
    with raises(NotImplementedError):
        mailer.send_quiet(None)


dummy = Tests()


@dummy.context
def app_context():
    app = Flask(__name__)
    app.testing = True
    from flaskext.mailer import Mailer
    mailer = Mailer(app)

    @app.route('/send')
    def send():
        mail = Email('hi!', 'awesome message', 'to@example.com', 'me@example.com')
        mailer.send(mail)
        return 'well done'

    with app.test_request_context():
        yield app


@dummy.test
def dummy_send():
    from flaskext.mailer.backends.dummy import DummyMailer
    mailer = DummyMailer()
    mail = Email('hello')
    mailer.send(mail)
    assert len(mailer.outbox) == 1
    assert mailer.outbox == [mail,]


@dummy.test
def dummy_init(app):
    with app.test_client() as c:
        c.get('/send')
        mailer = get_mailer()
        assert len(mailer.outbox) == 1
        assert mailer.outbox[0].subject == 'hi!'


smtp = Tests()


def init_smtp_mailer(**config):
    from flaskext.mailer.backends.smtp import SMTPMailer
    return SMTPMailer(**config)


@smtp.test
def smtp_bad_auth():
    with raises(RuntimeError):
        init_smtp_mailer(username='me')
    with raises(RuntimeError):
        init_smtp_mailer(password='my')


@smtp.test
def smtp_default_init():
    mailer = init_smtp_mailer()
    assert mailer.host == 'localhost'
    assert mailer.port == 25
    assert mailer.username == None
    assert mailer.password == None
    assert mailer.default_sender == None
    assert mailer.use_tls == False


@smtp.test
def smtp_send():
    mailer = init_smtp_mailer(host='localhost', port=6666)
    mail = Email('hello', 'awesome message',
                 to_addrs=['to@you', 'you@again'],
                 from_addr='from@me')
    with raises(RuntimeError):
        mailer.send(mail)


@smtp.test
def smtp_send_quiet():
    mailer = init_smtp_mailer(host='localhost', port=6666)
    mail = Email('hello', 'awesome message',
                 to_addrs=['to@you', 'you@again'],
                 from_addr='from@me')
    mailer.send_quiet(mail)


suite = Tests(tests=(mail, base, dummy, smtp))


if __name__ == '__main__':
    suite.main()
