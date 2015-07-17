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
from __future__ import absolute_import, unicode_literals, print_function
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from gs.content.email.base import (GroupEmail)


class HTMLMessage(GroupEmail):
    '''The actual *page* for the HTML version of a post.

:param post: The post to render
:type post: gs.group.list.email.base.interfaces.IPost
:param request: The Zope request

Mostly this class exists just to set the correct headers. The heavy-lifting
is done by the viewlets.'''
    def __init__(self, post, request):
        super(HTMLMessage, self).__init__(post, request)

    @Lazy
    def author(self):
        'The person who authored the post'
        retval = createObject('groupserver.UserFromId',
                              self.groupInfo.groupObj, self.context.post['user_id'])
        return retval
