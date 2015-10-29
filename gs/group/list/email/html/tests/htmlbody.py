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
import codecs
from contextlib import contextmanager
import os
from pkg_resources import resource_filename
from unittest import TestCase
from gs.group.list.email.html.htmlbody import HTMLBody


class TestHTMLBody(TestCase):
    'Test the HTMLBody class'
    line = '<span class="line">{0}</span><br/>'

    @staticmethod
    @contextmanager
    def open_test_file(filename):
        testname = os.path.join('tests', filename)
        fullname = resource_filename('gs.group.list.email.html', testname)
        with codecs.open(fullname, 'r', encoding='utf-8') as infile:
            yield infile

    def assertLine(self, expected, val):
        line = self.line.format(expected)
        self.assertEqual(line, val)

    def test_br(self):
        'Test that <br> elements are substituted in for newlines'
        text = 'I am a fish.\nI like to swim in the sea.'
        hb = HTMLBody(text)

        r = unicode(hb)
        self.assertIn('fish.</span><br/>\n<span class="line">I', r)
        self.assertEqual(text.count('\n'), r.count('\n'))
        self.assertEqual(text.count('\n') + 1, r.count('<br/>'))

    def test_line_quoted(self):
        'Test that a quoted line is muted'
        text = '> I am a fish.'
        hb = HTMLBody(text)

        r = unicode(hb)
        expected = '<span class="line muted">&gt; I am a fish.</span><br/>'
        self.assertEqual(expected, r)

    def test_line_unix_from(self):
        text = '>From A. Person'
        hb = HTMLBody(text)

        r = unicode(hb)
        self.assertLine('&gt;From A. Person', r)

    def test_line_normal(self):
        text = 'I am a fish.'
        hb = HTMLBody(text)

        r = unicode(hb)
        self.assertLine(text, r)

    def test_line_blank(self):
        'Test a blank line'
        text = ' '
        hb = HTMLBody(text)

        r = unicode(hb)
        expected = '&#160;<br/>'
        self.assertEqual(expected, r)

    def test_all(self):
        'Test everything together.'
        text = '''>From A. Person <person@example.com>:

> I am a *fish.*

I like to swim in the sea.
https://sea.example.com/swim?attitude=like'''
        hb = HTMLBody(text)

        r = unicode(hb)
        with self.open_test_file('e.html') as infile:
            expected = infile.read()
        self.maxDiff = 1024
        self.assertEqual(expected.strip(), r.strip())
