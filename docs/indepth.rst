.. _indepth:

In Depth Guide
==============

This document describes the API in a stage-by-stage basis.
It is useful as a book-like, gentle technical introduction
to the higher and lower level APIs. Before reading this
guide it is recommended that you browse through the :ref:`quickstart`
as it will give a very high level introduction to Maithon.
If you want to look for some method or class, go to the
:ref:`api` section.

Envelopes and MIMEs
-------------------

The :class:`~mailthon.envelope.Envelope` class actually
wraps around multipart MIME objects. This means they can
be composed of multiple other MIME objects, e.g. plaintext
MIMEs, MIMEs containing HTML data, images, etc, which provides
the perfect building block for a composable class. Envelopes
are made of two parts- like a real life envelope, a "stamp",
or headers, and an enclosure, made of other mime objects::
 
    from mailthon.envelope import Envelope
    from mailthon.enclosure import PlainText

    e = Envelope(
        headers={'X-Key': 'Value'},
        enclosure=[PlainText('something')],
    )

An interesting thing to take note of is that envelopes can
be enclosed within envelopes. Concretely speaking, Envelopes
consist of the :class:`~mailthon.headers.Headers` class and
a list of :class:`~mailthon.enclosure.Enclosure` objects::

    >>> e.headers
    {'X-Key': u'Value'}
    >>> e.enclosure
    [<mailthon.enclosure.PlainText object at 0x...>]

You might have noticed that the ``Value`` string that was
set was changed to a Unicode value. Why is that so? This
is because internally the :class:`~mailthon.headers.Headers`
class decodes bytes values that we throw at it into Unicode
objects, freeing the developer from any headaches about
encoding. You can read more about these design decisions
at the :ref:`design` section.

Now that we've looked at the higher level API of the
:class:`~mailthon.envelope.Envelope` class, let's plunge
deeper into madness and look into how it generates MIME
objects with the :meth:`~mailthon.envelope.Envelope.mime`
method::

    >>> e.mime()
    <email.mime.multipart.MIMEMultipart object at 0x...>

1. Generates a :class:`~email.mime.multipart.MIMEMultipart`
   instance and attaches each of the enclosures with the
   :meth:`~email.message.Message.attach` method. Conceptually
   this is what you'd do with a real envelope- put each of
   the content into the enclosure of the envelope.
2. Puts a stamp on the envelope- sets the headers onto
   the envelope object. This is done via the
   :meth:`~mailthon.headers.Headers.prepare` method
   of the headers object, which handles setting the
   appropriate headers- e.g. it ignores the Bcc headers
   to save you from embarassment and also to make
   Mailthon compliant with :rfc:`2822`.

Disecting Enclosures
--------------------

Conceptually the :class:`~mailthon.envelope.Envelope` and
:class:`~mailthon.enclosure.Enclosure` classes are the
same- they are both made out of headers and some content.
API-wise, they are also nearly identical- they both
provide the same :meth:`~mailthon.enclosure.Enclosure.mime`
method. And you are right! Here we see that the enclosure
objects do in fact have almost the same attributes::

    >>> plaintext = PlainText('content')
    >>> plaintext.headers
    {}
    >>> plaintext.mime()
    <email.mime.text.MIMEText object at 0x...>

However, speaking from a responsibility perspecitive,
here is where they differ. Envelopes have the concept
of senders and receivers- and must keep track of them.
Enclosures however, are like a superset of envelopes-
an envelope can be an enclosure, but not the other
way round, (at least, without some tricks).

All Enclosures have a :attr:`~Enclosure.content`
attribute that represents the content of the enclosure.
This is once again something that the envelope
object doesn't have::

    >>> plaintext.content
    'content'

The role as a MIME-preparing class is the same. As
mentioned earlier, both classes have the
:meth:`~mailthon.enclosure.Enclosure.mime` method
which prepares a MIME object- needless to say
different subclasses of the :class:`~mailthon.enclosure.Enclosure`
class handle different mimetypes, e.g.
:class:`~mailthon.enclosure.PlainText` handles
``text/plain`` content. Similarly this is what
an enclosure class does when it's :meth:`~mailthon.enclosure.Enclosure.mime`
method is called:

1. Prepare the MIME object. For :class:`~mailthon.enclosure.PlainText`
   enclosures this returns a :class:`~email.mime.text.MIMEText`
   object. For :class:`~mailthon.enclosure.Binary`
   enclosures the method returns a :class:`~email.mime.base.MIMEBase`
   object which is a lower level but more configurable
   and flexible version of the ``MIMEText`` class.
2. Apply the headers. Conceptually this is where the
   envelope analogy breaks down- you don't usually
   have stamps inside enclosures, but let's pretend
   that didn't happen. The Enclosure object is designed
   in such a way such that the subclasses will not need
   to worry about applying the user's headers. Essentially
   what the :meth:`~mailthon.enclosure.Enclosure.mime`
   method looks like is::

       def mime(self):
           mime = self.mime_object()
           self.headers.prepare(mime)
           return mime

   Which means that you usually do not have to worry
   about any headers that you've set not being applied
   to the generated MIME objects. So if you were to
   subclass the enclosure class::

       class Cat(Enclosure):
           def mime_object(self):
               return make_mime(self.cat_name)

   Which prevents you from shooting yourself in the
   foot. Or other parts of your body. Also it makes
   sure that, most of the time, you get the benefit
   of having the Mailthon infrastructure supporting
   your back- the main example being free of having
   to worry about encoding.

Few Sips of SMTP
----------------

How in the world, you ask, do you have tricks to make
the :class:`~mailthon.enclosure.Enclosure` class to
behave like an envelope? The Oracle answers, via
the runtime modification of attributes which may
cause headaches in production; but hey, let's try
them anyways::

    enclosure = PlainText('something')
    enclosure.mail_from = u'sender@mail.com'
    enclosure.receivers = [u'rcv1@mail.com', u'rcv2@mail.com']
    
    def string(self):
        return self.mime().as_string()

    enclosure.string = string

Note that the ``mail_from`` and ``receivers``
attributes having Unicode values is absolutely
necessary, and we'll see why when we talk about
then later when we explore the :class:`~mailthon.postman.Postman`
object. For now, assume that they will be properly
encoded by Mailthon. When we pass the enclosure
we've mutated to a :class:`~mailthon.postman.Postman`
instance, it'll happily send it off::

    >>> r = postman.send(enclosure)
    >>> assert r.ok

Questioning our identity
########################

Notice the ``mail_from`` attribute- it is not
named something like ``sender``. Why is that so?
It is named such that it is synonymous with the
SMTP ``MAIL FROM`` command. This is what is sent
by a vanila (without any middleware) Postman
instance in a typical SMTP session:

.. code-block:: text
   :emphasize-lines: 2

    HELO relay.example.org
    MAIL FROM:<sender@mail.com>
    RCPT TO:<rcv1@mail.com>
    RCPT TO:<rcv2@mail.com>
    DATA
    <mime data>
    QUIT

Note the highlighted line- the address passed to the
``MAIL FROM`` command is the 'true' sender. For example
you begin your letter with something along the lines of
"From XXX". The postman doesn't care about whatever you
wrote in there. He may, however write down your name
somewhere for bookeeping reasons. The address passed
to the ``MAIL FROM`` command is, essentially, your
'true' name. More info about this can be obtained
by reading :rfc:`2821`.

Usually you are doing the sane thing- you are sending
from the same email address that you are claiming to
send from (i.e. the one you set in the `headers`
argument to the :class:`~mailthon.envelope.Envelope`
class). But if you wish to do so, you can change the
'real' address. There are two ways to do it::

    from mailthon.headers import sender

    envelope = Envelope(
        headers=[sender('Fake <fake@mail.com>')],
        enclosure=[],
        mail_from=u'email_address@mail.com',
    )
    envelope.mail_from = u'other@mail.com'

However if you want the inferred sender (the one
that was obtained from the headers) you can still
do so via the :attr:`~mailthon.envelope.Envelope.sender`
attribute.

The headless MIME
#################

In an ideal world, the SMTP protocol speaks Unicode
and we can all throw poop emojis around at each other
while pretending to get our work done. But that is
sadly not the case. SMTP is a protocol which only
understands bytes, and was invented way back in
`1982 <http://tools.ietf.org/html/rfc821>`_ when
(only?) ASCII was the dominant encoding and nobody
cared about characters outside the English alphabet.

As a result, the simple ASCII encoding stuck and
was used as the de-facto standard for emails and
most other protocols. However, SMTP, given that it
does only operate in bytes, does allow you to simply do::

    Subject: 哈咯 (Hello)

But some clients will not be able to read it if they
are expected something encoded in ASCII, and suddenly
get some UTF-8 value, and is likely to end up with
`Mojibake <http://en.wikipedia.org/wiki/Mojibake>`_.

Instead, we must specify the encoding, and then
rewrite all of the code points of the string so that
it is ASCII-encoded. So your beautiful characters
end up looking like::

    >>> from email.header import Header
    >>> Header(u'哈咯 (Hello)', 'utf-8').encode()
    '=?utf-8?b?5ZOI5ZKvIChIZWxsbyk=?='

Not very nice, nor human readable. So rather
than having you manually encode everything,
Mailthon insists on having everything in
Unicode. This makes everything a lot easier-
extracting and encoding addresses, equality
comparisions, etc. So the job of the :class:`~mailthon.headers.Headers`
class (specifically, the :class:`~mailthon.helpers.UnicodeDict`
class) is to handle all this for you::

    >>> from email.message import Message
    >>> from mailthon.headers import Headers
    >>> headers = Headers({
    ...    'Subject': u'∂y is not exact',
    ... })
    ...
    >>> mime = Message()
    >>> headers.prepare(mime)
    >>> mime.as_string()
    'Subject: =?utf-8?q?=E2=88=82y_is_not_exact?=\n\n'

For the record, it's actually the :class:`~email.message.Message`
class that does all the heavy lifting-
Mailthon simply supplies it with the right
things and does the right transformations.
