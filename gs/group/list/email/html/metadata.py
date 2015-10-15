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
from zope.component import createObject
from gs.core import mailto
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
        body = b.format(groupInfo=self.groupInfo)
        retval = mailto(self.email, 'Unsubscribe', body)
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
