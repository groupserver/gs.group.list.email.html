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

    def test_bold(self):
        'Test that "*this*" is marked up as bold'
        text = 'I am a *fish.*'
        hb = HTMLBody(text)

        r = unicode(hb)
        self.assertLine('I am a <b>*fish.*</b>', r)

    def test_email(self):
        'Test email markup'
        text = 'Email me at person@example.com'
        hb = HTMLBody(text)

        r = unicode(hb)
        self.assertLine(
            'Email me at <a class="email" '
            'href="mailto:person@example.com">person@example.com</a>', r)

    def test_An_Email(self):
        'Test email markup with mixed case'
        text = 'Email me at A.Person@Example.com'
        hb = HTMLBody(text)

        r = unicode(hb)
        self.assertLine(
            'Email me at <a class="email" '
            'href="mailto:A.Person@Example.com">A.Person@Example.com</a>', r)

    def test_angle_email(self):
        'Test when Michael writes an email address'
        text = 'Email me at <person@example.com>'
        hb = HTMLBody(text)

        r = unicode(hb)
        self.assertLine(
            'Email me at <a class="email" '
            'href="mailto:person@example.com">&lt;person@example.com&gt;</a>', r)

    def test_mailto_email(self):
        'Test email address written as a mailto'
        text = 'Email me at mailto:person@example.com'
        hb = HTMLBody(text)

        r = unicode(hb)
        self.assertLine(
            'Email me at <a class="email" '
            'href="mailto:person@example.com">mailto:person@example.com</a>', r)

    def test_www(self):
        'Test that www is turned into a link'
        text = 'Visit www.example.com'
        hb = HTMLBody(text)

        r = unicode(hb)
        self.assertLine(
            'Visit <a href="http://www.example.com">www.example.com</a>', r)

    def test_WWW(self):
        'Test that WWW is turned into a link'
        text = 'Visit WWW.Example.Com'
        hb = HTMLBody(text)

        r = unicode(hb)
        self.assertLine(
            'Visit <a href="http://WWW.Example.Com">WWW.Example.Com</a>', r)

    def test_http(self):
        'Test that an http-address is turned into a link'
        text = 'Visit http://example.com'
        hb = HTMLBody(text)

        r = unicode(hb)
        self.assertLine(
            'Visit <a href="http://example.com">http://<b>example.com</b></a>', r)

    def test_https(self):
        'Test that an https-address is turned into a link'
        text = 'Visit https://example.com'
        hb = HTMLBody(text)

        r = unicode(hb)
        self.assertLine(
            'Visit <a href="https://example.com">https://<b>example.com</b></a>', r)

    def test_http_path(self):
        'Test a http-address with a path'
        text = 'Visit http://example.com/people/me'
        hb = HTMLBody(text)

        r = unicode(hb)
        self.assertLine(
            'Visit <a href="http://example.com/people/me">http://<b>example.com</b>/people/me</a>',
            r)

    def test_http_query(self):
        'Test an http-address with a query string'
        text = 'Visit http://example.com/people/me?show=Stufff'
        hb = HTMLBody(text)

        r = unicode(hb)
        self.assertLine(
            'Visit <a href="http://example.com/people/me?show=Stufff">'
            'http://<b>example.com</b>&#8203;/people&#8203;/me&#8203;?show&#8203;=Stufff</a>', r)

    def test_http_angle(self):
        'Test an http-address in angle brackets'
        text = 'Visit <http://example.com/>.'
        hb = HTMLBody(text)

        r = unicode(hb)
        self.assertLine(
            'Visit <a href="http://example.com/">&lt;http://<b>example.com</b>/&gt;</a>.', r)

    def test_long_https_angle(self):
        'Test a long https-address in angle brackets'
        text = 'Visit <https://groups.example.com/people/a_very_long_user_id?show=Stufff>'
        hb = HTMLBody(text)
        self.maxDiff = None
        r = unicode(hb)
        self.assertLine(
            'Visit <a class="small" href="https://groups.example.com/people/a_very_long_user_id'
            '?show=Stufff">'
            '&lt;https://<b>groups.example.com</b>&#8203;/people&#8203;/a&#8203;_very&#8203;_long'
            '&#8203;_user&#8203;_id&#8203;?show&#8203;=Stufff&gt;</a>', r)

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
