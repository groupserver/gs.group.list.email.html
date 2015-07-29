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
    def __init__(self, matchRE, subStr):
        self.matchRE = matchRE
        self.subStr = subStr
        self.re = re_compile(self.matchRE, re_I | re_M | re_U)

    def match(self, s):
        return self.re.match(s)

    def sub(self, s):
        return self.re.sub(self.subStr, s)


class HTMLBody(object):
    HTML_ESCAPE_TABLE = {
        '"': "&quot;",
        "'": "&apos;"
    }
    boldMatcher = Matcher("(\*.*\*)", r'<b>\g<1></b>')
    emailMatcher = Matcher(r"(.*?)([A-Z0-9\._%+-]+@[A-Z0-9.-]+\.[A-Z]+)(.*?)",
                           r'<a class="email" href="mailto:\g<2>">\g<1>\g<2>\g<3></a>')
    wwwMatcher = Matcher(r"(?i)(www\..+)", r'<a href="http://\g<1>">\g<1></a>')
    uriMatcher = Matcher(r"(?i)(http://|https://)(.+?)(\&lt;|\&gt;|\)|\]|\}|\"|\'|$|\s)",
                         r'<a href="\g<1>\g<2>">\g<1>\g<2></a>\g<3>')
    matchers = [boldMatcher, emailMatcher, wwwMatcher, uriMatcher]

    def __init__(self, originalText):
        if not originalText:
            raise(ValueError('"originalText" argument required'))
        self.originalText = originalText

    def __iter__(self):
        mainBody = self.splitBody[0]
        lines = mainBody.rstrip().split('\n')
        for line in lines:
            retval = self.markup(line)
            yield retval

    def __unicode__(self):
        retval = '\n'.join(self)
        return retval

    def __str__(self):
        retval = unicode(self).encode('ascii', 'xmlcharrefreplace')
        return retval

    @Lazy
    def splitBody(self):
        retval = split_message(self.originalText)
        return retval

    def markup(self, line):
        if line.strip() == '':
            retval = '&#160;<br/>'
        else:
            cssClass = "line"
            if line.lstrip()[0] == '>':
                cssClass += " muted"
            #  <https://wiki.python.org/moin/EscapingHtml>
            escapedLine = escape(line.rstrip(), self.HTML_ESCAPE_TABLE)
            markedUpLine = self.markup_words(escapedLine)
            r = '<span class="{0}">{1}</span><br/>'
            retval = r.format(cssClass, markedUpLine)
        assert(retval)
        return retval

    def markup_words(self, line):
        words = line.split(' ')
        rwords = []
        for word in words:
            subWord = None
            for matcher in self.matchers:
                if matcher.match(word):
                    subWord = matcher.sub(word)
                    break
            rword = subWord if subWord is not None else word
            rwords.append(rword)
        retval = ' '.join(rwords)
        return retval
