============================
``gs.group.list.email.html``
============================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The HTML version of the messages from a GroupServer group
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2015-10-30
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.Net`_.

.. _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

Introduction
============

The email messages that GroupServer_ sends from a group are
different from what is received. This product supplies a message
template for rendering a post in HTML. The headers are changed
when the message is being sent [#sender]_.

Resources
=========

- Documentation:
  https://groupserver.readthedocs.org/projects/gsgrouplistemailhtml
- Code repository:
  https://github.com/groupserver/gs.group.list.email.html
- Questions and comments to
  http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. [#sender] See the ``gs.group.list.sender`` product
             <https://github.com/groupserver/gs.group.list.sender>

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17

..  LocalWords:  IAppendix viewlets groupserver EmailHTMLPrologue
