.. _api:

API
===

Postman Object
--------------

.. autoclass:: mailthon.postman.Postman
   :members: send, deliver, connection, use

   .. attribute:: transport

      The transport class to be used. This defaults to the
      :class:`smtplib.SMTP` class, but can be any callable
      that accepts a ``host``, ``port``, and the additional
      arguments specified in the ``options`` parameter. The
      recommended way to change this is via subclassing::

          class HTTPPostman(Postman):
              transport = HTTPMailingProtocol

      Although you can change it during runtime for special
      purposes such as testing. The transport class must also
      support the ``ehlo`` and ``sendmail`` methods, and return
      objects that match the signature of those functions. For
      reference:

      - :meth:`smtplib.SMTP.sendmail`
      - :meth:`smtplib.SMTP.ehlo`

   .. attribute:: response_cls

      The response class to be used. Defaults to the
      :class:`~mailthon.response.SendmailResponse`
      class. It must be a callable which has the same
      type signature, and is recommended to be changed
      only by subclasses::

          class HTTPPostman(Postman):
              response_cls = MyResponse

Envelope Object
---------------

.. autoclass:: mailthon.envelope.Envelope
   :members:
   :inherited-members:

Enclosure Objects
-----------------

.. autoclass:: mailthon.enclosure.Enclosure
   :members:
   :inherited-members:

   .. attribute:: headers

      A :class:`~mailthon.headers.Header` instance containing
      all of the headers. Note that when the enclosure objects
      are prepared (i.e. the :meth:`~mailthon.enclosure.Enclosure.mime`
      method is called), this headers attribute has precendence
      over other headers already set in the
      :meth:`~mailthon.enclosure.Enclosure.mime_object` method.
      For example::

          e = EnclosureSubclass(
              mimetype='text/plain',
              headers={
                  'Content-Type': 'text/html',
              })
          mime = e.mime()
          assert mime['Content-Type'] == 'text/html'

      This is to ensure that the user ultimately has control
      over which headers are set in the final, prepared MIME
      object.

.. autoclass:: mailthon.enclosure.PlainText
   :members:

.. autoclass:: mailthon.enclosure.HTML
   :members:

.. autoclass:: mailthon.enclosure.Binary
   :members:

.. autoclass:: mailthon.enclosure.Attachment
   :members:

Response Objects
----------------

.. autoclass:: mailthon.response.Response
   :members:
   :inherited-members:

   .. attribute:: status_code

      The integer status code returned by the server.
      You can look up what they mean in the
      `SMTP reply codes <http://www.greenend.org.uk/rjk/tech/smtpreplies.html>`_
      page.

   .. attribute:: message

      The accompanying message returned by the server,
      as an undecoded bytes object. The message usually
      differs on a per-server basis.

.. autoclass:: mailthon.response.SendmailResponse
   :members:

   .. attribute:: rejected

      A dictionary of rejected addresses to :class:`~mailthon.response.Response`
      objects.

Middlewares
-----------

.. autoclass:: mailthon.middleware.Middleware

   .. method:: __call__(connection)
      
      To be overriden by subclasses. This method is
      called by the :class:`~mailthon.postman.Postman`
      class when a connection to the server is established
      with the transport instance, e.g. an :class:`smtplib.SMTP`
      object.

.. autoclass:: mailthon.middleware.Auth
   :members:

.. autoclass:: mailthon.middleware.TLS
   :members:

Helper Functions
----------------

.. autofunction:: mailthon.helpers.encode_address

.. autofunction:: mailthon.helpers.guess

.. autofunction:: mailthon.helpers.format_addresses

.. autofunction:: mailthon.helpers.UnicodeDict

Headers
-------

.. autoclass:: mailthon.headers.Headers
   :members:

Header Functions
****************

The following functions are the recommended way to set
the commonly used headers, instead of providing the
string values yourself. They are generator functions
and can be used like so::

    >>> from mailthon.headers import sender
    >>> dict([sender('sender')])
    {'Sender': 'sender'}

.. autofunction:: mailthon.headers.sender

.. autofunction:: mailthon.headers.to

.. autofunction:: mailthon.headers.cc

.. autofunction:: mailthon.headers.bcc

.. autofunction:: mailthon.headers.message_id

.. autofunction:: mailthon.headers.date
