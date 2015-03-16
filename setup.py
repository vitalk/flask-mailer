#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Flask-Mailer
============

A Flask extension for sending email messages with pluggable backends
and pythonic API.

Contributing
------------

Don't hesitate to create a `GitHub issue
<https://github.com/vitalk/flask-mailer/issues>`_ for any **bug** or
**suggestion**.

"""
import io
import os
import re
import sys
import subprocess
from setuptools import find_packages, setup, Command


def read(*parts):
    try:
        return io.open(os.path.join(*parts), 'r', encoding='utf-8').read()
    except IOError:
        return b''


def get_version():
    version_file = read('flaskext', 'mailer', '__init__.py')
    version_match = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]',
                              version_file, re.MULTILINE)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


class pytest(Command):
    user_options = [
        ('coverage', None, 'report coverage')
    ]

    def initialize_options(self):
        self.coverage = None

    def finalize_options(self):
        pass

    def run(self):
        basecmd = [sys.executable, '-m', 'pytest']
        if self.coverage:
            basecmd += ['--cov', 'flaskext/mailer']
        errno = subprocess.call(basecmd + ['tests'])
        raise SystemExit(errno)


__version__ = get_version()


setup(
    name='Flask-Mailer',
    version=__version__,
    license='BSD',
    author='Vital Kudzelka',
    author_email='vital.kudzelka@gmail.com',
    description='A Flask extension for sending emails with pluggable backends.',
    url='https://github.com/vitalk/flask-mailer',
    download_url='https://github.com/vitalk/flask-mailer/tarball/%s' % __version__,
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    namespace_packages=['flaskext'],
    install_requires=['Flask'],
    tests_require=['pytest', 'pytest-cov'],
    cmdclass={'test': pytest},
    zip_safe=False,
    platforms='any',
    keywords='flask mail smtp',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
