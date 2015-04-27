#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys


if sys.version_info[0] >= 3:
    text_type = str
    string_types = str,
    iteritems = lambda o: o.items()
    itervalues = lambda o: o.values()

    unicode_compatible = lambda x: x
else:
    text_type = unicode
    string_types = basestring,
    iteritems = lambda o: o.iteritems()
    itervalues = lambda o: o.itervalues()

    def unicode_compatible(cls):
        """A decorator which defines `__str__` and `__unicode__` methods in
        decorated class.
        """
        if '__str__' not in cls.__dict__:
            raise ValueError('decorator cannot be applied to %s '
                             'because it does not define __str__ method' %
                             cls.__name__)
        cls.__unicode__ = cls.__str__
        cls.__str__ = lambda x: x.__unicode__().encode('utf-8')
        return cls
