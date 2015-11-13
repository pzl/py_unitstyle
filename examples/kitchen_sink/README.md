Kitchen Sink
============

This should demonstrate most of the features and outputs of `unitstyle`.

The "project" code itself is kept simple, and mostly irrelevant here. The tests are set up to have most displayable cases occur:

- passing
- failing
- skipped
- Exception (not expected)
- expected Exceptions
- slow test
- etc...

So run `python test.py` and you will see how all of those are represented.

---

In addition to showing all the various test results, `test.py` will accept an argument to use a particular output format. By default, it will display 'dots'. But pass in any other format (e.g. `python test.py spec`) to get that output. Now you can see all test results in any format.

Like the other examples, `unitstyle.py` is only symlinked here to make the relative import easier. Ina  real project, this file would not be here. `unitstyle` would be installed globally on your system (or in a virtualenv) and you can just `import unitstyle` all the same.
