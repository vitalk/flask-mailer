#!/usr/bin/python
# -*- config coding: utf-8 -*-


def key(name): return ('MAILER_%s' % name).upper()
"""Returns uppercased config key for extension."""


def strip_prefix(prefix, string):
    """Strip prefix from a string if it exists.

    :param prefix: The prefix to strip.
    :param string: The string to process.
    """
    if string.startswith(prefix):
        return string[len(prefix):]
    return string
