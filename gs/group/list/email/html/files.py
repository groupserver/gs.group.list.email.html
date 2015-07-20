# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2014, 2015 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import absolute_import, unicode_literals
from math import pow, floor, log
from zope.cachedescriptors.property import Lazy
from gs.group.list.email.text.files import FilesViewlet


class FilesListViewlet(FilesViewlet):
    'The viewlet for the the prologue when there are no files'

    @Lazy
    def post(self):
        retval = self.context.post
        return retval

    @Lazy
    def show(self):
        retval = self.n > 0
        return retval

    @staticmethod
    def file_size_format(bytes):
        """Returns a humanized string for a given amount of bytes"""
        # http://python.todaysummary.com/q_python_11123.html
        bytes = int(bytes)
        if bytes is 0:
            retval = 'empty'
        else:
            l = floor(log(bytes, 1024))
            size = bytes / pow(1024, l)
            unit = ['bytes', 'kb', 'mb', 'gb', 'tb', 'pb', 'eb', 'zb', 'yb'][int(l)]
            retval = "%.2f%s" % (size, unit)
        return retval
