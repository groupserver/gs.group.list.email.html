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
from operator import attrgetter
from xml.sax.saxutils import escape
from zope.cachedescriptors.property import Lazy
from gs.group.messages.post.text.splitmessage import split_message
from .matcher import (boldMatcher, emailMatcher, wwwMatcher, uriMatcher, )


class HTMLBody(object):
    '''The HTML form of a plain-text email body.

:param str originalText: The original (plain) text'''
    HTML_ESCAPE_TABLE = {
        '"': "&quot;",
        "'": "&apos;"
    }

    def __init__(self, originalText):
        if not originalText:
            raise(ValueError('"originalText" argument required'))
        self.originalText = originalText
        self.matchers = [boldMatcher, emailMatcher, wwwMatcher, uriMatcher]
        sorted(self.matchers, key=attrgetter('weight'))

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
