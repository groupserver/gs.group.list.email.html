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
import sys
if sys.version_info >= (3, ):  # pragma: no cover
    from urllib.parse import quote
else:  # Python 2
    from urllib import quote
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from gs.core import to_unicode_or_bust
from gs.group.list.email.base import EmailMessageViewlet


class MetadataViewlet(EmailMessageViewlet):
    'The viewlet for the the prologue'

    @Lazy
    def email(self):
        'The group email address'
        retval = self.listInfo.get_property('mailto')
        return retval

    @Lazy
    def leaveLink(self):
        b = '''Hello,

Please remove me from {groupInfo.name}
<{groupInfo.url}>

Thank you.'''
        ub = b.format(groupInfo=self.groupInfo)
        uval = to_unicode_or_bust(ub)
        utf8val = uval.encode('utf-8')
        body = quote(utf8val)
        retval = 'mailto:{0}?subject=Unsubscribe&body={1}'.format(self.email, body)
        return retval

    @Lazy
    def post(self):
        'Same as self.context.post, but with the URL of the post and topic'
        retval = self.context.post
        retval['url'] = '{0}/r/post/{1}'.format(self.siteInfo.url, retval['post_id'])
        retval['topicURL'] = '{0}/r/topic/{1}'.format(self.siteInfo.url, retval['post_id'])
        return retval

    @Lazy
    def author(self):
        'The person who authored the post'
        retval = createObject('groupserver.UserFromId',
                              self.groupInfo.groupObj, self.post['user_id'])
        return retval
