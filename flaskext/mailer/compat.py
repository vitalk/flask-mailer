#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys


if sys.version_info[0] >= 3:
    text_type = str
    string_types = str,
    iteritems = lambda o: o.items()
    itervalues = lambda o: o.values()
else:
    text_type = unicode
    string_types = basestring,
    iteritems = lambda o: o.iteritems()
    itervalues = lambda o: o.itervalues()
