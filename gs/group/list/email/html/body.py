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
from zope.cachedescriptors.property import Lazy
from gs.group.list.email.base import EmailMessageViewlet
from gs.group.messages.text import HTMLBody


class BodyViewlet(EmailMessageViewlet):
    'The viewlet for the actual message body'

    @Lazy
    def post(self):
        'Same as self.context.post, but with the URL of the post'
        retval = self.context.post
        retval['url'] = '{0}/r/post/{1}'.format(self.siteInfo.url, retval['post_id'])
        return retval

    @Lazy
    def htmlBody(self):
        retval = HTMLBody(self.post['body'])
        return retval

    @Lazy
    def readMore(self):
        remainder = self.htmlBody.splitBody[1]
        retval = bool(remainder.strip())
        return retval
