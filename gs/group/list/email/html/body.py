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
from zope.component import createObject
from gs.group.list.email.base import EmailMessageViewlet


class MetadataViewlet(EmailMessageViewlet):
    'The viewlet for the message metadata'

    @Lazy
    def post(self):
        retval = self.context.post
        return retval

    @Lazy
    def author(self):
        'The person who authored the post'
        retval = createObject('groupserver.UserFromId',
                              self.groupInfo.groupObj, self.post['user_id'])
        return retval

    @Lazy
    def profileImageUrl(self):
        r = '{0}{1}/gs-profile-image-square/90'
        retval = r.format(self.siteInfo.url, self.author.url)
        return retval


class BodyViewlet(EmailMessageViewlet):
    'The viewlet for the actual message body'
    HTML_ESCAPE_TABLE = {
        '"': "&quot;",
        "'": "&apos;"
    }

    @Lazy
    def post(self):
        retval = self.context.post
        return retval

    @classmethod
    def markup(cls, line):
        if line.strip() == '':
            r = '&#160;{0}'
        elif line.lstrip()[0] == '>':
            r = '<span class="line muted">{0}</span></br>'
        else:
            r = '<span class="line">{0}</span><br/>'
        l = escape(line.rstrip(), cls.HTML_ESCAPE_TABLE)
        #  <https://wiki.python.org/moin/EscapingHtml>
        retval = r.format(l)
        return retval

    def lines(self):
        lines = self.post['body'].split('\n')
        for line in lines:
            retval = self.markup(line)
            yield retval
