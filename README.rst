unitstyle
=========

``unitstyle`` is a python module that adds several output format options
for Python's standard ``unittest`` library (unittest2). Specifically, it
adds many of the output options offered by
`mocha <https://mochajs.org/#reporters>`__, a javascript unit testing
framework. This package was created to port those outputs to Python.

Installation
------------

``unitstyle`` is available on PyPI. You should be able to install it
with ``pip install unitstyle``.

Usage
-----

The ``unitstyle`` package provides itself as a ``unittest`` TestRunner,
and should be used as such.

simple example:

.. code:: python


    import unittest
    import unitstyle

    suite = unittest.TestLoader().discover()
    unitstyle.TestRunner().run(suite)

Supported arguments to ``unitstyle``'s TestRunner are:

Output Formats
--------------

-  `list <https://mochajs.org/#list>`__
-  `dots <https://mochajs.org/#dot-matrix>`__
-  `jsstream <https://mochajs.org/#json-stream>`__ - a JSON stream
-  `JSON <https://mochajs.org/#json>`__
-  `progress <https://mochajs.org/#progress>`__ (bar)
-  `min <https://mochajs.org/#min>`__
-  `tap <https://mochajs.org/#tap>`__ - the `Test Anything
   Protocol <http://en.wikipedia.org/wiki/Test_Anything_Protocol>`__
-  `spec <https://mochajs.org/#spec>`__

Feel free to open an issue to request more, or pull requests!

License
-------

This project and code is licensed under the MIT License. See the
``LICENSE`` file for more.

Copyright (c) 2015 Dan Panzarella
