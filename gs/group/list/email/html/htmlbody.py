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
from __future__ import absolute_import, unicode_literals
from re import compile as re_compile, I as re_I, M as re_M, U as re_U
from xml.sax.saxutils import escape
from zope.cachedescriptors.property import Lazy
from gs.group.messages.post.postbody import split_message


class Matcher(object):
    '''Match a word, by a regular expression, and make a substitution

:param str matchRE: The regular expression used to check if there was a match
                    (see :func:`re.match`)
:param str subStr: The string specifying the subsitution (see :func:`re.sub`)'''
    def __init__(self, matchRE, subStr):
        self.matchRE = matchRE
        self.subStr = subStr

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


class HTMLBody(object):
    '''The HTML form of a plain-text email body.

:param str originalText: The original (plain) text'''
    HTML_ESCAPE_TABLE = {
        '"': "&quot;",
        "'": "&apos;"
    }

    #: Turn ``*asterisk*`` characters into bold-elements
    boldMatcher = Matcher("(?P<boldText>\*.*\*)", r'<b>\g<boldText></b>')

    #: Turn email addresses (``person@example.com``) into clickable ``mailto:`` links
    emailMatcher = Matcher(
        r"(?P<leading>.*?)(?P<address>[A-Z0-9\._%+-]+@[A-Z0-9.-]+\.[A-Z]+)(?P<trailing>.*)",
        r'<a class="email" href="mailto:\g<address>">\g<leading>\g<address>\g<trailing></a>')

    #: Turn site names (``www.example.com``) into clickable ``http://`` links
    wwwMatcher = Matcher(r"(?P<siteName>www\..+)",
                         r'<a href="http://\g<siteName>">\g<siteName></a>')

    #: Turn URIs (both ``http`` and ``https``) into clickable links
    uriMatcher = Matcher(
        r"(?P<leading>\&lt;|\(|\[|\{|\"|\'|^)(?P<protocol>http://|https://)(?P<rest>.+?)"
        r"(?P<trailing>\&gt;|\)|\]|\}|\"|\'|$|\s)",
        r'<a href="\g<protocol>\g<rest>">\g<leading>\g<protocol>\g<rest>\g<trailing></a>')

    def __init__(self, originalText):
        if not originalText:
            raise(ValueError('"originalText" argument required'))
        self.originalText = originalText
        self.matchers = [self.boldMatcher, self.emailMatcher, self.wwwMatcher, self.uriMatcher]

    def __iter__(self):
        '''The marked-up lines in the main body'''
        mainBody = self.splitBody[0]
        lines = mainBody.rstrip().split('\n')
        for line in lines:
            retval = self.markup(line)
            yield retval

    def __unicode__(self):
        '''The main part of the HTML body, as a Unicode string'''
        retval = '\n'.join(self)
        return retval

    def __str__(self):
        '''The main part of the HTML body, as an ASCII string. Non-ASCII characters are replaced
with XML entities.'''
        retval = unicode(self).encode('ascii', 'xmlcharrefreplace')
        return retval

    @Lazy
    def splitBody(self):
        '''The body as a 2-tuple: main body, and remainder'''
        retval = split_message(self.originalText)
        return retval

    def markup(self, line):
        '''Markup the line, and the words in the line

:param str line: The line to mark up.
:returns: An HTML form of the line: the characters escaped, the words marked up, and surrounded
          in a ``<span>`` element.
:rtype: str'''
        if line.strip() == '':
            retval = '&#160;<br/>'
        else:
            cssClass = "line"
            # The ">From" is a Unix from, so the line is not a quote
            if ((line.lstrip()[0] == '>') and (line.lstrip()[:5] != '>From')):
                cssClass += " muted"
            #  <https://wiki.python.org/moin/EscapingHtml>
            escapedLine = escape(line.rstrip(), self.HTML_ESCAPE_TABLE)
            markedUpLine = self.markup_words(escapedLine)
            r = '<span class="{0}">{1}</span><br/>'
            retval = r.format(cssClass, markedUpLine)
        assert(retval)
        return retval

    def markup_words(self, line):
        '''Mark up the words on the line

:param str line: The line to mark up
:returns: The line with the words marked up
:rtype: str'''
        rwords = []
        for word in line.split(' '):
            subWord = None  # Word that will be substituted for the current word
            # Short-circut if the word is ''. It will be turned back in ' ' when we ``' '.join``
            if word:
                for matcher in self.matchers:
                    if matcher.match(word):
                        subWord = matcher.sub(word)
                        break
            rword = subWord if subWord is not None else word
            rwords.append(rword)
        retval = ' '.join(rwords)
        return retval
