===============
Release process
===============

This is the release process for leather:

1. Verify all tests pass.
2. Check test coverage: ``pytest --cov leather``.
3. Ensure any new modules have been added to setup.py's ``packages`` list.
#. Ensure any new public interfaces have been added to the documentation.
#. Make sure the example scripts still work: ``./examples.sh``.
#. Ensure ``CHANGELOG.rst`` is up to date. Add the release date and summary.
#. Create a release tag: ``git tag -a x.y.z -m "x.y.z release."``
#. Push tags upstream: ``git push --tags``
#. If this is a major release, merge ``master`` into ``stable``: ``git checkout stable; git merge master; git push``
#. Upload to `PyPI <https://pypi.python.org/pypi/leather>`_: ``python setup.py sdist bdist_wheel upload``.
#. Flag the release to build on `RTFD <https://readthedocs.org/dashboard/leather/versions/>`_.
#. Update the "default version" on `RTFD <https://readthedocs.org/dashboard/leather/versions/>`_ to the latest.
#. Rev to latest version: ``docs/conf.py``, ``setup.py`` and ``CHANGELOG.rst`` need updates.
#. Commit revision: ``git commit -am "Update to version x.y.z for development."``.
