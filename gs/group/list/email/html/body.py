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

    @classmethod
    def markup(cls, line):
        if line.strip() == '':
            retval = '&#160;<br/>'
        else:
            cssClass = "line"
            if line.lstrip()[0] == '>':
                cssClass += " muted"
            #  <https://wiki.python.org/moin/EscapingHtml>
            escapedLine = escape(line.rstrip(), cls.HTML_ESCAPE_TABLE)
            r = '<span class="{0}">{1}</span><br/>'
            retval = r.format(cssClass, escapedLine)
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
