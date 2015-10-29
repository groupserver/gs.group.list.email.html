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
from gs.group.list.email.html.matcher import (Matcher, boldMatcher, emailMatcher, wwwMatcher,
                                              uriMatcher)


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


class TestBoldMatcher(TestCase):
    def test_match(self):
        'Test that "*this*" is recognised as bold'
        r = boldMatcher.match("*this*")
        self.assertTrue(r)

    def test_sub(self):
        r = boldMatcher.sub('I am a *fish.*')
        self.assertEqual('I am a <b>*fish.*</b>', r)


class TestEmailMatcher(TestCase):
    def test_match(self):
        'Test that "person@example.com" is recognised as an email address'
        r = emailMatcher.match("person@example.com")
        self.assertTrue(r)

    def test_sub(self):
        'Test email substitution'
        r = emailMatcher.sub('person@example.com')
        expected = '<a class="email" href="mailto:person@example.com">person@example.com</a>'
        self.assertEqual(expected, r)

    def test_An_Email_match(self):
        'Test email markup with mixed case'
        r = emailMatcher.match('A.Person@Example.com')
        self.assertTrue(r)

    def test_An_Email_sub(self):
        'Test email substitution with mixed case'
        r = emailMatcher.sub('A.Person@Example.com')
        self.assertEqual(
            '<a class="email" href="mailto:A.Person@Example.com">A.Person@Example.com</a>', r)

    def test_angle_email_match(self):
        'Test when we match when Michael writes an email address'
        r = emailMatcher.match('<person@example.com>')
        self.assertTrue(r)

    def test_angle_email_sub(self):
        'Test when we substitute when Michael writes an email address'
        r = emailMatcher.sub('&lt;person@example.com&gt;')
        expected = '<a class="email" href="mailto:person@example.com">&lt;person@example.com&gt;'\
            '</a>'
        self.assertEqual(expected, r)

    def test_mailto_email_match(self):
        'Test email address written as a mailto-URI is matched'
        r = emailMatcher.match('mailto:person@example.com')
        self.assertTrue(r)

    def test_mailto_email_sub(self):
        'Test email address written as a mailto-URI is substituted'
        r = emailMatcher.sub('mailto:person@example.com')
        self.assertEqual(
            '<a class="email" href="mailto:person@example.com">mailto:person@example.com</a>', r)


class TestWWWMatcher(TestCase):
    def test_www_match(self):
        'Test that www is matched'
        r = wwwMatcher.match('www.example.com')
        self.assertTrue(r)

    def test_www_sub(self):
        'Test that www is turned into a link'
        r = wwwMatcher.sub('www.example.com')
        self.assertEqual('<a href="http://www.example.com">www.example.com</a>', r)

    def test_WWW_match(self):
        'Test that WWW is matched'
        r = wwwMatcher.match('WWW.Example.Com')
        self.assertTrue(r)

    def test_WWW_sub(self):
        'Test that WWW is turned into a link'
        r = wwwMatcher.sub('WWW.Example.Com')
        self.assertEqual('<a href="http://WWW.Example.Com">WWW.Example.Com</a>', r)


class TestURIMatcher(TestCase):
    def test_http_match(self):
        'Test that an http-address is matched as a URI'
        r = uriMatcher.match('http://example.com')
        self.assertTrue(r)

    def test_http_sub(self):
        'Test that an http-address is turned into a link'
        r = uriMatcher.sub('http://example.com')
        self.assertEqual('<a href="http://example.com">http://<b>example.com</b></a>', r)

    def test_https_match(self):
        'Test that an https-address is matched as a URI'
        r = uriMatcher.match('https://example.com')
        self.assertTrue(r)

    def test_https_sub(self):
        'Test that an https-address is turned into a link'
        r = uriMatcher.sub('https://example.com')
        self.assertEqual('<a href="https://example.com">https://<b>example.com</b></a>', r)

    def test_http_path_match(self):
        'Test a http-address with a path is matched'
        r = uriMatcher.match('http://example.com/people/me')
        self.assertTrue(r)

    def test_http_path_sub(self):
        'Test a http-address with a path is turned into a link'
        r = uriMatcher.sub('http://example.com/people/me')
        expected = '<a href="http://example.com/people/me">http://<b>example.com</b>/people/me</a>'
        self.assertEqual(expected, r)

    def test_http_query_match(self):
        'Test an http-address with a query string is matched'
        r = uriMatcher.match('http://example.com/people/me?show=Stufff')
        self.assertTrue(r)

    def test_http_query_sub(self):
        'Test an http-address with a query string is turned into a link'
        r = uriMatcher.sub('http://example.com/people/me?show=Stufff')
        expected = '<a href="http://example.com/people/me?show=Stufff">'\
            'http://<b>example.com</b>&#8203;/people&#8203;/me&#8203;?show&#8203;=Stufff</a>'
        self.assertEqual(expected, r)

    def test_http_angle_match(self):
        'Test an http-address in angle brackets matches'
        r = uriMatcher.match('&lt;http://example.com/&gt;')
        self.assertTrue(r)

    def test_http_angle_sub(self):
        'Test an http-address in angle brackets is turned into a link'
        r = uriMatcher.sub('&lt;http://example.com/&gt;')
        expected = '<a href="http://example.com/">&lt;http://<b>example.com</b>/&gt;</a>'
        self.assertEqual(expected, r)

    def test_long_https_angle_match(self):
        'Test a long https-address in angle brackets is matched'
        text = '&lt;https://groups.example.com/people/a_very_long_user_id?show=Stufff&gt;'
        r = uriMatcher.match(text)
        self.assertTrue(r)

    def test_long_https_angle_sub(self):
        'Test a long https-address in angle brackets is turned into a link'
        text = '&lt;https://groups.example.com/people/a_very_long_user_id?show=Stufff&gt;'
        r = uriMatcher.sub(text)
        expected = '<a class="small" href="https://groups.example.com/people/'\
            'a_very_long_user_id?show=Stufff">&lt;https://<b>groups.example.com</b>&#8203;/people'\
            '&#8203;/a&#8203;_very&#8203;_long&#8203;_user&#8203;_id&#8203;?show&#8203;=Stufff&gt;'\
            '</a>'
        self.assertEqual(expected, r)
