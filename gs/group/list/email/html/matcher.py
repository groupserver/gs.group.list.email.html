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
from re import compile as re_compile, I as re_I, M as re_M, U as re_U
from string import punctuation


class Matcher(object):
    '''Match a word, by a regular expression, and make a substitution

:param str matchRE: The regular expression used to check if there was a match
                    (see :func:`re.match`)
:param str subStr: The string specifying the subsitution (see :func:`re.sub`)'''
    def __init__(self, matchRE, subStr, weight=10):
        self.matchRE = matchRE
        self.subStr = subStr
        self.weight = weight

        #: The regular expression used to make the match. The flags :const:`re.I`, :const:`re.M`,
        #: and :const:`re.U` are set.
        self.re = re_compile(self.matchRE, re_I | re_M | re_U)

    def match(self, s):
        '''Does the string match the regular expression?

:param str s: The string to evaluate
:returns: ``True`` if the string matches the regular expression, ``False`` otherwise.
:rtype: bool'''
        return self.re.match(s)

    def sub(self, s):
        '''Substitute the string in for the substitution string

:param str s: The string to process
:returns: The new string substituted in :attr:`self.subStr`
:rtype: unicode'''
        return self.re.sub(self.subStr, s)

#: Turn ``*asterisk*`` characters into bold-elements
boldMatcher = Matcher("(?P<boldText>\*.*\*)", r'<b>\g<boldText></b>', 10)

#: Turn email addresses (``person@example.com``) into clickable ``mailto:`` links
emailMatcher = Matcher(
    r"(?P<leading>.*?)(?P<address>[A-Z0-9\._%+-]+@[A-Z0-9.-]+\.[A-Z]+)(?P<trailing>.*)",
    r'<a class="email" href="mailto:\g<address>">\g<leading>\g<address>\g<trailing></a>', 20)

#: Turn site names (``www.example.com``) into clickable ``http://`` links
wwwMatcher = Matcher(r"(?P<siteName>www\..+)",
                     r'<a href="http://\g<siteName>">\g<siteName></a>', 30)


class URIMatcher(Matcher):
    '''A horrid hack for a horrid issue'''
    def __init__(self):
        super(URIMatcher, self).__init__(
            r"(?P<leading>\&lt;|\(|\[|\{|\"|\'|^)(?P<protocol>http://|https://)"
            r"(?P<host>([a-z\d][-a-z\d]*[a-z\d]\.)*[a-z][-a-z\\d]+[a-z])(?P<rest>.*?)"
            r"(?P<trailing>\&gt;|\)|\]|\}|\"|\'|$|\s)",
            r'<a href="\g<protocol>\g<host>\g<rest>">\g<leading>\g<protocol><b>\g<host></b>'
            r'\g<rest>\g<trailing></a>', 40)

    def sub(self, s):
        if len(s) <= 32:
            retval = super(URIMatcher, self).sub(s)
        else:
            retval = self.long_url_sub(s)
        return retval

    @staticmethod
    def add_zws(s):
        'Add zero-width spaces to the string'
        retval = ''
        for c in s:
            if c in punctuation:
                retval += ('&#8203;' + c)
            else:
                retval += c
        return retval

    def long_url_sub(self, s):
        m = self.re.match(s)
        gd = m.groupdict()
        brokenRest = self.add_zws(gd['rest'])
        c = '{leading}{protocol}<b>{host}</b>{rest}{trailing}'
        content = c.format(leading=gd['leading'], protocol=gd['protocol'], host=gd['host'],
                           rest=brokenRest, trailing=gd['trailing'])
        if len(s) > 64:
            r = '<a class="small" href="{0}">{1}</a>'
        else:
            r = '<a href="{0}">{1}</a>'
        url = '{0}{1}{2}'.format(gd['protocol'], gd['host'], gd['rest'])
        retval = r.format(url, content)
        return retval

#: Turn URIs (both ``http`` and ``https``) into clickable links
uriMatcher = URIMatcher()
