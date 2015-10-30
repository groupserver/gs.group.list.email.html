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
from zope.cachedescriptors.property import Lazy
from gs.group.list.email.text.files import FilesViewlet
from gs.group.messages.base import file_size_format


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
        retval = file_size_format(bytes)
        return retval
