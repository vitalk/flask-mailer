Release History
===============

0.4.0 (2015-05-14)
------------------

- Internal refactor.
- Add python 2.6 support.
- Use markdown for README.
- SMTP:
    - Emit warning on invalid credentials.

0.3.7 (2015-03-16)
------------------

- SMTP:
    - Explicitly convert mail attributes to text type on send.

0.3.6 (2015-03-16)
------------------

- Move package version into package namespace.

0.3.5 (2015-03-16)
------------------

- Rewrite PyPi project page.
- Update package metadata.

0.3.4 (2014-08-26)
------------------

- Raise `ValueError` on blank mail parameters instead of `RuntimeError`.

0.3.3 (2014-08-25)
------------------

- Mail attributes are optional.

0.3.2 (2014-08-25)
------------------

- Better unicode support.

0.3.1 (2014-08-22)
------------------

- Mail subject is optional.

0.3.0 (2014-08-22)
------------------

- Encode mail subject into RFC 2822-compliant string.

0.2.2 (2014-08-11)
------------------

- Rename PyPi package to `Flask-Mailer`.

0.2.1 (2014-08-11)
------------------

- Update test suite.

0.2.0 (2014-04-27)
------------------

- Unify mail API.
- Exclude BCC header from mail message (as per http://tools.ietf.org/html/rfc2822).

0.1.0 (2014-01-22)
------------------

Initial release.
