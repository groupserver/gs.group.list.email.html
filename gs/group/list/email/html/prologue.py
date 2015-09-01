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
from .metadata import MetadataViewlet


class PrologueViewlet(MetadataViewlet):
    'The viewlet for the the prologue'
    IMG_SIZE = 60

    @Lazy
    def profileImageUrl(self):
        r = '{0}{1}/gs-profile-image-square/{2}'
        retval = r.format(self.siteInfo.url, self.author.url, self.IMG_SIZE)
        return retval
