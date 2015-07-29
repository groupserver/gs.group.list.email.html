HTML body
=========

The body of the email message is marked up as HTML, rather than
sent through as plain text.

* The characters that would cause issues with the XML are
  escaped. This includes ``"`` and ``'`` characters.
* Each line is placed within a ``<span>`` element, with the CSS
  class set to ``line``.
* Lines that start with ``>`` but not ``>From`` are considered
  quotes, and given the additional CSS class ``muted``.
* The words of the line are given one of the following markup:

  + Words in ``*asterisk*`` characters are made bold.
  + Email addresses are made clickable.
  + Site names starting with ``www`` are made clickable.
  + URLs (``http`` and ``https``) are made clickable.

API
---

.. autoclass:: gs.group.list.email.html.htmlbody.HTMLBody
   :member-order: bysource
   :members:
   :special-members: __iter__, __str__, __unicode__

.. autoclass:: gs.group.list.email.html.htmlbody.Matcher
   :member-order: bysource
   :members:
