Flask-Mailer
============

A Flask extension for sending email messages. Includes different mailer
backends for different purposes:

- Dummy backend (useful for tests)
- SMTP backend (SMTP lib wrapper)


Installation
------------

Install from PyPi via `pip`:

```sh
pip install Flask-Mailer
```


Configuration
-------------

| Option                  | Description                                                            |
| ----------------------- | ---------------------------------------------------------------------- |
| `MAILER_BACKEND`        | Path to mailer backend, e.g. `flask_mailer.backends.smpt.SMTPMailer`   |
| `MAILER_TESTING`        | Enable dummy backend for testing                                       |
| `MAILER_HOST`           | Hostname for SMTP backend, e.g. `localhost`                            |
| `MAILER_PORT`           | Port for SMTP backend, e.g. `25`                                       |
| `MAILER_USERNAME`       | Username for SMTP backend                                              |
| `MAILER_PASSWORD`       | Password for SMTP backend                                              |
| `MAILER_DEFAULT_SENDER` | Default mail sender, e.g. `webmaster`                                  |


Usage
-----

```python
from flask import Flask
from flask_mailer import Mailer, Email

app = Flask(__name__)
smtp = Mailer(app)

mail = Email('hi, there', 'awesome message',
             to=['to@example.com', 'you@example.com'],
             from_addr='me@example.com')
smtp.send(mail)
```


Testing
-------

Setting to your app `testing` flag automatically enable the dummy mailer
backend or you can manually set `MAILER_TESTING` to `True`. On dummy mailer
all mails on send just append to outbox list:

```python
smtp.send(mail)

assert len(smtp.outbox) == 1
assert smtp.outbox == [mail,]
```


Thanks
------

The extension inspired and partially reuse the code of the some awesome
projects, such as:

- Flask-Mail
- Django
- plurk
- reddit

Special thanks to their authors and contributors.


License
-------

Licensed under the BSD license.
