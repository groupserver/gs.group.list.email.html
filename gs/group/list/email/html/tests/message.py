# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2015 OnlineGroups.net and Contributors.
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
from __future__ import absolute_import, unicode_literals, print_function
from mock import MagicMock
from unittest import TestCase
from gs.group.list.email.html.message import HTMLMessagePart


class TestMessage(TestCase):
    @staticmethod
    def get_config(localReturn, globalReturn):
        retval = MagicMock(spec=['DivisionConfiguration', 'GlobalConfiguration'])
        retval.DivisionConfiguration.getProperty.return_value = localReturn
        retval.GlobalConfiguration.getProperty.return_value = globalReturn
        return retval

    def test_show_local(self):
        'Test showing when set in the site config'
        context = self.get_config(False, None)
        part = HTMLMessagePart(context, None)

        r = part.show

        self.assertFalse(r)

    def test_show_global(self):
        'Test showing when set in the global config'
        context = self.get_config(None, False)
        part = HTMLMessagePart(context, None)

        r = part.show

        self.assertFalse(r)

    def test_show_default(self):
        'Test showing when the default is used'
        context = self.get_config(None, None)
        part = HTMLMessagePart(context, None)

        r = part.show

        self.assertTrue(r)

    def test_show_override(self):
        'Test showing when overriding the global config'
        context = self.get_config(True, False)
        part = HTMLMessagePart(context, None)

        r = part.show

        self.assertTrue(r)
