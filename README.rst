============================
``gs.group.list.email.html``
============================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The HTML version of the messages from a GroupServer group
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2015-07-10
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.Net`_.

.. _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

Introduction
============

The email messages that GroupServer_ sends from a group are
different from what is received. This product supplies a `message
template`_ for rendering a post in HTML. The headers are changed
when the message is being sent [#sender]_.

Message template
================

The message template itself just contains the
``groupserver.EmailHTMLMessage`` viewlet manager [#viewlet]_ —
which provides the
``gs.group.list.email.html.interfaces.IHTMLMessage`` interface.
By default, three viewlets are provided for the message. Each
viewlet contains further viewlet manager, effectively dividing
the message in three: the prologue_, the body_ and the
appendix_::

  ┌HTML message───────────────────────────────────────┐
  │┌HTML message viewlet manager─────────────────────┐│
  ││gs.group.list.email.html.interfaces.IHTMLMessage ││
  ││                                                 ││
  ││┌Pre-roll viewlet manager───────────────────────┐││
  │││gs.group.list.email.html.interfaces.IPreroll   │││
  ││└───────────────────────────────────────────────┘││
  ││                                                 ││
  ││┌Prologue viewlet manager───────────────────────┐││
  │││gs.group.list.email.html.interfaces.IPrologue  │││
  ││└───────────────────────────────────────────────┘││
  ││                                                 ││
  ││┌Body viewlet manager───────────────────────────┐││
  │││gs.group.list.email.html.interfaces.IBody      │││
  ││└───────────────────────────────────────────────┘││
  ││                                                 ││
  ││┌Appendix viewlet manager───────────────────────┐││
  │││gs.group.list.email.html.interfaces.IAppendix  │││
  ││└───────────────────────────────────────────────┘││
  │└─────────────────────────────────────────────────┘│
  └───────────────────────────────────────────────────┘

Pre-roll
--------

The pre-roll part of an HTML message is unformatted **hidden**
text that appears before the rest of the message. It is picked up
by email clients that use it for a **summary** of the message:
think of it like a second subject-line.

The *viewlet manager* ``groupserver.EmailHTMLPreroll``
(``gs.group.list.email.html.interfaces.IPreroll``) is normally
filled by the *File notice* viewlets.

The **File notice** viewlets state that there is one or more
files listed in the appendix_:

* One (``gs-group-list-email-html-preroll-file``) provides a
  short notice that there is *a* file listed in the appendix of a
  message,

* The other (``gs-group-list-email-html-preroll-files``) provides
  a short notice that there are *multiple* files listed in the
  appendix of a message.

Prologue
--------

The prologue of a message appears at the top of the message body,
but before the body_ proper.

Body
----

The *body* of the message is provided by the
``groupserver.EmailHTMLBody``
(``gs.group.list.email.html.interfaces.IBody``) viewlet manager.

The *Plan body* (``gs-group-list-email-html-body-plain``) viewlet
writes out the body of the post much as it was when it was sent
in.

Appendix
--------

The *appendix* of the message is provided by the
``groupserver.EmailHTMLAppendix``
(``gs.group.list.email.html.interfaces.IAppendix``) viewlet
manager. Two viewlets are provided as standard: a `files list`_
and a footer_.

Files list
~~~~~~~~~~

Files are large burden for a list, as they dramatically increase
the size of the message for little gain [#picture]_. Because of
this the attached files are replaced with *links* to the files on
the Web. The *Files list* viewlet
(``gs-group-list-email-html-appendix-files``) provides this list.

Footer
~~~~~~

The standard *Footer* viewlet
(``gs-group-list-email-html-appendix-footer``) provides the
following:

* The *Unsubscribe* link, which is legally required in many
  jurisdictions.

* A link to the topic on the Web.

Resources
=========

- Code repository: https://github.com/groupserver/gs.group.list.email.html
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. [#viewlet] See the ``zope.viewlet`` product
              <https://pypi.python.org/pypi/zope.viewlet/>

.. [#sender] See the ``gs.group.list.sender`` product
             <https://github.com/groupserver/gs.group.list.sender>

.. [#picture] If “a picture can speak a thousand words” then
              represent that concept with a picture. Send
              attempts that are less than 2K (the size of a
              thousand words, compressed) to
              <mpj17@onlinegroups.net>.

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17

..  LocalWords:  IAppendix viewlets groupserver EmailHTMLPrologue
