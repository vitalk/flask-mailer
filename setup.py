#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
flask-mailer
------------------------------------------------------------------

A Flask extension for sending emails.
"""
from setuptools import setup


setup(
    name='flask-mailer',
    version='0.1',
    license='BSD',
    author='Vital Kudzelka',
    author_email='vital.kudzelka@gmail.com',
    description='A Flask extension for sending emails',
    long_description=__doc__,
    packages=[
        'flaskext',
        'flaskext.mailer'
    ],
    namespace_packages=['flaskext'],
    install_requires=['Flask'],
    tests_require=['Attest'],
    test_loader='attest:auto_reporter.test_loader',
    test_suite='tests.suite',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
        'Framework :: Flask'
    ]
)
