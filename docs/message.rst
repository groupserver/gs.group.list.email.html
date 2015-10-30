.. _msg:

Message template
================

The HTML form of the message is formatted using the standard
HTML-email templates [#template]_. The content is provided by two
viewlet managers [#viewlet]_: one for the `pre-roll`_ and one for
the main `html message`_.

.. code-block:: none

  ┌─HTML message─────────────────────────────────────────┐
  │                                                      │
  │  ┌─Pre-roll viewlet manager────────────────────────┐ │
  │  │ gs.group.list.email.html.interfaces.IPreroll    │ │
  │  └─────────────────────────────────────────────────┘ │
  │                                                      │
  │ ┌─HTML message viewlet manager─────────────────────┐ │
  │ │ gs.group.list.email.html.interfaces.IHTMLMessage │ │
  │ │                                                  │ │
  │ │ ┌─Prologue viewlet─────────────────────────────┐ │ │
  │ │ │ gs-group-list-email-html-prologue            │ │ │
  │ │ └──────────────────────────────────────────────┘ │ │
  │ │                                                  │ │
  │ │ ┌─Body viewlet─────────────────────────────────┐ │ │
  │ │ │ gs-group-list-email-html-body                │ │ │
  │ │ └──────────────────────────────────────────────┘ │ │
  │ │                                                  │ │
  │ │ ┌─Files viewlet────────────────────────────────┐ │ │
  │ │ │ gs-group-list-email-html-files               │ │ │
  │ │ └──────────────────────────────────────────────┘ │ │
  │ │                                                  │ │
  │ └──────────────────────────────────────────────────┘ │
  │                                                      │
  │ ┌─Links viewlet────────────────────────────────────┐ │
  │ │ gs-group-list-email-html-links                   │ │
  │ └──────────────────────────────────────────────────┘ │
  │                                                      │
  └──────────────────────────────────────────────────────┘

Pre-roll
--------

The pre-roll part of an HTML message is unformatted **hidden**
text that is slotted before the rest of the message. It is picked
up by email clients that use it for a **summary** (or preview) of
the message: think of it like a second subject-line.

The *viewlet manager* ``groupserver.EmailHTMLPreroll``
(:class:`gs.group.list.email.html.interfaces.IPreroll`) is
normally filled by the *File notice* viewlets.

The **File notice** viewlets state that there is one or more
files listed in the files_ viewlet:

* One (``gs-group-list-email-html-preroll-file``) provides a
  short notice that there is *a* file listed in the appendix of a
  message,

* The other (``gs-group-list-email-html-preroll-files``) provides
  a short notice that there are *multiple* files listed in the
  appendix of a message.

There is also a summary provided when there are no files present
(``gs-group-list-email-html-preroll-nofile``). It just spells out
the origin of the message (the site and group names).

HTML message
------------

The HTML message viewlet manager ``groupserver.EmailHTML``
(:class:`gs.group.list.email.html.interfaces.IHTMLMessage`)
provides the bulk of what people see in the message. There are
three viewlets shipped by default: a prologue_, the body_ proper,
and the files_.

Prologue
~~~~~~~~

The prologue of a message appears at the top of the message body,
before the body_ proper. The prologue contains the metadata for
the post:

* Who made the post (name and photo),
* The group the post was made to, and
* The topic the group was made to.

It also provides many links to the profile, group, and topic
respectively.

Body
~~~~

The *Plan body* (``gs-group-list-email-html-body-plain``) viewlet
writes out the body of the post much as it was when it was sent
in. It is currently the **text** version of the message, with
newlines replaced with ``<br />`` elements. Like the post on the
web, bottom-quoting is removed (replaced with a link to the
post).

Files
~~~~~

Files are large burden for a list, as they dramatically increase
the size of the message for little gain. Because of this the
attached files are replaced with *links* to the files on the
Web. The *Files list* viewlet
(``gs-group-list-email-html-files``) provides this list.

Links
-----

The *Links* (``gs-group-list-email-html-links``) are a group of
HTTP and ``mailto`` links to perform some common functions. The
first three links are rendered as buttons, while the last two are
rendered as normal links.

Reply:
    The *Reply* link provides a ``mailto`` URI to send an email
    to the group with a nice tidy :mailheader:`Subject`
    header. The link is mostly there to stop the *New topic* link
    from being confusing: without the *Reply* it looks as if you
    can only start topics. The link is only shown if the reply-to
    setting for a group is *group* (the default).

New topic:
    Most people are happy replying to a group using the
    :guilabel:`Reply` button in their email client. However, many
    are unaware that they can start topics. To combat this the
    *New topic* link provides a ``mailto`` URI to email the
    group. (Unusually for a GroupServer ``mailto`` URI the
    :mailheader:`Subject` is blank.) The *New topic* link is
    hidden if the reply-to setting for a group is *author*.

Topic:
    The *Topic* link is an HTTP-link to the topic page, just like
    the topic-title in the Prologue_.

Unsubscribe:
    As required by legislation, the *Unsubscribe* link removes a
    person from a group. The link contains a ``mailto`` URI that
    sends a message to the group, with the the
    :mailheader:`Subject` header set to ``Unsubscribe``. A
    ``mailto`` URI is used — rather than sending the person to
    the *Leave* page — so passwords do not have to be used.

    The *Unsubscribe* email command is processed by
    `gs.group.member.leave.command`_

Daily digest:
    A handy link copied from our friends at `E-Democracy.org`_,
    the *Digest* a ``mailto`` URI that points to the group with
    the :mailheader:`Subject` header set to ``Digest on``.

    The *Digest on* command is processed by
    `gs.group.member.email.settings`_.

.. [#template] See the ``gs.content.email.layout`` product
              <https://github.com/groupserver/gs.content.email.layout>

.. [#viewlet] See the ``zope.viewlet`` product
              <https://pypi.python.org/pypi/zope.viewlet/>

.. _E-Democracy.org: http://E-Democracy.org/

.. _gs.group.member.leave.command:
   https://github.com/groupserver/gs.group.member.leave.command

.. _gs.group.member.email.settings:
   https://github.com/groupserver/gs.group.member.email.settings
