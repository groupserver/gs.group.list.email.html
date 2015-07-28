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
  └──────────────────────────────────────────────────────┘

Pre-roll
--------

The pre-roll part of an HTML message is unformatted **hidden**
text that appears before the rest of the message. It is picked up
by email clients that use it for a **summary** of the message:
think of it like a second subject-line.

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

It also provides many links to the group, profile, and topic (and
to leave the group).

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

.. [#template] See the ``gs.content.email.layout`` product
              <https://github.com/groupserver/gs.content.email.layout>

.. [#viewlet] See the ``zope.viewlet`` product
              <https://pypi.python.org/pypi/zope.viewlet/>
