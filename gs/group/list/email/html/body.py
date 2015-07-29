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
from re import compile as re_compile, I as re_I, M as re_M, U as re_U
from xml.sax.saxutils import escape
from zope.cachedescriptors.property import Lazy
from gs.group.list.email.base import EmailMessageViewlet
from gs.group.messages.post.postbody import split_message


class BodyViewlet(EmailMessageViewlet):
    'The viewlet for the actual message body'
    HTML_ESCAPE_TABLE = {
        '"': "&quot;",
        "'": "&apos;"
    }

    @Lazy
    def post(self):
        'Same as self.context.post, but with the URL of the post'
        retval = self.context.post
        retval['url'] = '{0}/r/post/{1}'.format(self.siteInfo.url, retval['post_id'])
        return retval

    bold_matcher = re_compile("(\*.*\*)")
    email_matcher = re_compile(r"(.*?)([A-Z0-9\._%+-]+@[A-Z0-9.-]+\.[A-Z]+)(.*?)",
                               re_I | re_M | re_U)
    www_matcher = re_compile("(?i)(www\..+)")
    uri_matcher = re_compile("(?i)(http://|https://)(.+?)(\&lt;|\&gt;"
                             "|\)|\]|\}|\"|\'|$|\s)")

    def markup_words(self, line):
        # --=mpj17=-- I am not proud
        words = line.split(' ')
        rwords = []
        for word in words:
            if self.bold_matcher.match(word):
                w = self.bold_matcher.sub(r'<b>\g<1></b>', word)
            elif self.email_matcher.match(word):
                print('"{}"'.format(word))
                w = self.email_matcher.sub(
                    '<a class="email" href="mailto:\g<2>">\g<1>\g<2>\g<3></a>',
                    word)
                print('"{}"'.format(w))
            elif self.www_matcher.match(word):
                w = self.www_matcher.sub('<a href="http://\g<1>">\g<1></a>',
                                         word)
            elif self.uri_matcher.match(word):
                w = self.uri_matcher.sub(
                    '<a href="\g<1>\g<2>">\g<1>\g<2></a>\g<3>', word)
            else:
                w = word
            rwords.append(w)
        retval = ' '.join(rwords)
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

    @Lazy
    def splitBody(self):
        retval = split_message(self.post['body'])
        return retval

    def lines(self):
        mainBody = self.splitBody[0]
        lines = mainBody.rstrip().split('\n')
        for line in lines:
            retval = self.markup(line)
            yield retval

    @Lazy
    def readMore(self):
        remainder = self.splitBody[1].strip()
        retval = bool(remainder)
        return retval
