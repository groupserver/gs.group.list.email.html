Adaptor
=======

.. currentmodule:: gs.group.list.email.html

The :class:`message.HTMLMessagePart` class adapts a post (as the
context) and a browser request, and provides the
:class:`gs.group.list.email.base.interfaces.IMessagePart`
interface.

The :attr:`message.HTMLMessagePart.show` property returns
``True`` if the HTML-form of a message should be shown. It looks
up the ``htmlEmail`` property in the ``DivisionConfiguration``
and the ``GlobalConfiguration`` objects, with the setting in the
former overriding the latter. If the ``htmlEmail`` property is
absent then the default action is taken: show HTML email.

The :meth:`message.HTMLMessagePart.as_email` method returns an
instance of the standard :class:`email.mime.text.MIMEText` class,
with the MIME-type set to :mimetype:`text/html`. The UTF-8
character-encoding is set.
