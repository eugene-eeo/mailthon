Foreword
========

Read this before getting started with Mailthon. It answers (hopefully)
some questions about the goals of the project and whether you should
consider using it or not.

Philosophy
----------

Mailthon's philosophy is that composability and extensibility stem
from an elegant and simple codebase. Also, one of Mailthon's aims
is to not include as much magic as practically possible, but remain
pragmatic at the same time. For example Mailthon does not have magical
HTML/plaintext inference of the content- that is left to the developer
to decide. Another value is the sanity of the API- whether something
is named intuitively, or whether something should work like it does.
The focus is on having as little surprises as possible.

Code over Configuration
-----------------------

While some minimum configuration can be done via "configuration",
most of the time Mailthon strives to encourage code-over-configuration.
This is because code is always more powerful than configuration, which
is one of the driving ideals behind middleware classes. Also, Mailthon
does not rely on any configuration files, nor does it try to parse any
files. Any configuration should be made explicit in the code.

Continue to the :ref:`installation` or the :ref:`quickstart`.
