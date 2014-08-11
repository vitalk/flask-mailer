#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Flask-Mailer
    ~~~~~~~~~~~~

    A Flask extension for sending emails with pluggable backends.

    :copyright: (c) by Vital Kudzelka
    :license: BSD
"""
import sys
import subprocess
from setuptools import setup, Command


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


setup(
    name='Flask-Mailer',
    version='0.2.2',
    license='BSD',
    author='Vital Kudzelka',
    author_email='vital.kudzelka@gmail.com',
    description='A Flask extension for sending emails with pluggable backends.',
    long_description=__doc__,
    packages=[
        'flaskext',
        'flaskext.mailer'
    ],
    namespace_packages=['flaskext'],
    install_requires=['Flask'],
    tests_require=['pytest', 'pytest-cov'],
    cmdclass={'test': pytest},
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
