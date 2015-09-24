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
import sys
if sys.version_info >= (3, ):  # pragma: no cover
    from urllib.parse import quote
else:  # Python 2
    from urllib import quote
from zope.cachedescriptors.property import Lazy
from gs.core import to_unicode_or_bust
from gs.group.list.base import (replyto, ReplyTo)
from .metadata import MetadataViewlet


class LinksViewlet(MetadataViewlet):
    'The viewlet for the the links'

    @Lazy
    def digestLink(self):
        b = '''Hello,

Please switch me from receiving one email per post to the daily
digest, which summarises the all the posts made each day in
{groupInfo.name}
<{groupInfo.url}>

Thank you.'''
        ub = b.format(groupInfo=self.groupInfo)
        uval = to_unicode_or_bust(ub)
        utf8val = uval.encode('utf-8')
        body = quote(utf8val)
        digestOn = quote('Digest on')
        r = 'mailto:{0}?subject={1}&body={2}'
        retval = r.format(self.email, digestOn, body)
        return retval

    @Lazy
    def replyTo(self):
        retval = replyto(self.listInfo)
        return retval

    @Lazy
    def replyLink(self):
        if self.replyTo == ReplyTo.group:
            t = 'Re: {0}'.format(self.post['subject'])
            utf8val = t.encode('utf-8')
            topic = quote(utf8val)
            r = 'mailto:{0}?subject={1}'
            retval = r.format(self.email, topic)
        else:
            retval = None
        return retval

    @Lazy
    def newLink(self):
        if self.replyTo == ReplyTo.author:
            retval = None
        else:
            retval = 'mailto:{0}'.format(self.email)
        return retval
