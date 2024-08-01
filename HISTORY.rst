=======
History
=======


Unreleased
==========

* ...


2.4.0 - 2024-04-21
==================

* Ports travis.yml to GitHub Actions in #35 by @joshuadavidthomas
* Update the link to Click docs in #37 by @allen-munsch
* Update supported Python and Django versions in #41 by @philipstarkey
* Updates the linting CI task and tox config to run with the latest tox in #41 by @philipstarkey


2.3.0 - 2021-09-07
==================

* Add support for click > 8.0.
* Remove upper bounds, until we run into an upward compatibility issue.
* Drop support for Django 3.0.


2.2.0 - 2020-07-21
==================

* Add support for click > 7.1
* Require Python 3.6 or higher.
* Require Django 2.2 or higher.


2.1.1 - 2020-06-12
==================

* Ensure click is 7.0.x or lower.


2.1.0 - 2018-04-20
==================

* Add experimental support for Django 2.0


2.0.0 - 2017-06-30
==================

* Drop support for unsupported Django versions (1.4, 1.5, 1.6, and 1.7).
* Add official support for Django 1.10 and 1.11.
* Add official support for python 3.5 (all Django versions) and 3.6
  (Django 1.11 only).
* Correctly handle click errors by outputting the formatted messages instead
  of a stack trace (#4).


1.2.0 - 2016-05-19
==================

* Allow custom lookups on ``ModelInstance`` parameter types.


1.1.0 - 2016-02-04
==================

* Add a ``ModelInstance`` parameter type to automatically retrieve model
  instances by their primary key


1.0.0 – 2015-09-14
==================

* Support for command groups
* Added a ``pass_verbosity`` decorator
* Improved test suite


0.1.1 – 2015-09-11
==================

* Django 1.4, 1.5, 1.6, 1.7 and 1.8 compatibility
* Python 2.7 and 3.4 compatibility
* 100% coverage test suite


0.1.0 – 2015-09-10
==================

* Initial release
