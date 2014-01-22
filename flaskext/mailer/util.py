#!/usr/bin/python
# -*- config coding: utf-8 -*-
from werkzeug.utils import import_string

from flask.ext.mailer.compat import iteritems


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


def get_config(config):
    """Returns the config without the annoying prefix and with lowercase keys.

    :param config: The config dictionary to inspect.
    """
    prefix = 'MAILER_'
    return {strip_prefix(prefix, name).lower(): value
            for name, value in iteritems(config) if name.startswith(prefix) }


def import_path(path):
    """"Imports a dotted module path and returns the attribute/class designated
    by the last name in the path.

    :param path: The dotted module path to import.
    """
    if not path:
        return

    module_name, class_name = path.rsplit('.', 1)
    module = import_string(module_name, silent=True)
    return getattr(module, class_name, None)
