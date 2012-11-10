# Flask-mailer

A Flask extension for sending email messages.

Includes different mailer backends for different purposes:

* dummy mailer(useful for unittests)
* SMTP mailer(wrapper for SMTP lib)

# Usage

## Installation

```bash
pip install -e git+git://github.com/vitalk/flask-mailer.git#egg=flask-mailer
```

## Configuration

Use standard Flask config API for set available options:

* MAILER_HOST('localhost')
* MAILER_PORT(25)
* MAILER_USERNAME(None)
* MAILER_PASSWORD(None)
* MAILER_DEFAULT_SENDER('webmaster')
* MAILER_BACKEND('flaskext.mailer.backends.smtp.SMTPMailer')
* MAILER_TESTING(app.testing)

Setup mailer instance:

```python
from flask import Flask
from flaskext.mailer import Mailer

app = Flask(__name__)
mailer = Mailer(app)
```

Or on deferred way:

```python
mailer = Mailer()

app = Flask(__name__)
mailer.init_app(app)
```

## Sending emails

```python
from flaskext.mailer.mail import Email

mail = Email('hi, there', 'awesome message',
             to_addrs=['to@example.com', 'you@example.com'],
             from_addr='me@example.com')
```

If you set *DEFAULT_SENDER* on config then you don't need to set mail sender
explicitly. If *from_addr* is two-element tuple, this will be split into name
and address:

```python
mail = Email('hi, there', 'awesome message',
             to_addrs=['to@example.com', 'you@example.com'],
             from_addr=('me', 'me@example.com'))
assert mail.from_addr == 'me <me@example.com>'
```

And finally send mail:

```python
from flaskext.mailer import get_mailer

mailer = get_mailer()
mailer.send(mail)
```

If connection to your mail server fails this will raise an error. To swallow
errors use *send_quiet* method.

```python
mailer.send_quiet(mail)
```

It is possible to send mail with previously registered mailer with shortcut:

```python
from flaskext.mailer import send_email

send_email('hi', 'awesome message', 'to@example.com')
```

## Testing

Setting to your app *testing* flag automatically enable the dummy mailer
backend or you can manually set *MAILER_TESTING* to *True*.
On dummy mailer all mails on send just append to outbox list:

```python
from flaskext.mailer import get_mailer

mailer = get_mailer()
mail = Email('testing', 'awesome message', 'to@example.com', 'from@example.com')
mailer.send(mail)

assert len(mailer.outbox) == 1
assert mailer.outbox == [mail,]
```

# Thanks

The code based on some existing projects. Special thanks for it authors and
contributors.

* Flask-Mail
* django
* reddit
* plurk

# About me

My name is Vital Kudzelka <vital.kudzelka@gmail.com>. Fell free to get in touch.
