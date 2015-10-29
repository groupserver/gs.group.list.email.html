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
from unittest import TestCase
from gs.group.list.email.html.matcher import Matcher


class TestMatcher(TestCase):
    def test_match(self):
        re = '.*(fish).*'
        m = Matcher(re, None)

        r = m.match('I am a fish.')
        self.assertTrue(r)

    def test_miss(self):
        'Test when they do not match'
        re = '.*(fish).*'
        m = Matcher(re, None)

        r = m.match('I am a dog.')
        self.assertFalse(r)

    def test_sub(self):
        re = 'fish'
        sub = 'dog'
        m = Matcher(re, sub)

        r = m.sub('I am a fish.')
        self.assertEqual('I am a dog.', r)
