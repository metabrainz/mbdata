Version 30.0.0
==============

- Schema change 30.
- Allow selecting MBS tag or branch from which to update SQL
- Delete useless /updates SQL folder after update
- Drop support for Python 3.8, add support for 3.13
- Move the repository maintenance under MetaBrainz umbrella

Version 29.0.0
==============

- Schema change 29.

Version 27.1.0
==============

- Added `mbslave init` command.

Version 27.0.0
==============

- Schema change 27.

Version 26.0.1
==============

- Added ``Recording.tracks`` relationship to the SQLAlchemy models.

Version 26.0.0
==============

- Support for MusicBrainz database schema 26.

Version 25.0.4
==============

- Fixed reading of MusicBrainz API token from ``mbslave.conf``.

Version 25.0.3
==============

- Fixed a bug in locating ``mbslave.conf``.

Version 25.0.2
==============

- Fixed database connection in ``mbslave``.

Version 25.0.1
==============

- Added ``mbdata.__version__``.
- Fixed ``mbslave psql`` with custom PostgreSQL port number.
- By default, the ``mbslave`` script will read its config file from either
  ``$PWD/mbslave.conf`` or ``/etc/mbslave.conf``. Previously, it was only ``$PWD/mbslave.conf``.
- Documentation clarifications.

Version 25.0.0
==============

- Changed versioning with the Musicbrainz database schema as the major version.
- Support for MusicBrainz database schema 25.
- Added MusicBrainz replication (mbslave was merged into this project).
- Docker image with mbslave.
- Python 3 support.

Version 2017.06.02
==================

-  Remove old_editor_name mapping.

Version 2017.06.01
==================

-  Updated to MusicBrainz database schema 24.

Version 2017.01.18
==================

-  Added index definitions to models.
-  Support for SQLAlchemy 1.1.

Version 2016.07.17
==================

-  Updated to MusicBrainz database schema 23.
-  Python 3 support.

Version 2016.02.11
==================

-  New function ``mbdata.config.configure()`` that makes sure that the
   models have not been imported yet.
-  Support for schema re-mapping in ``mbdata.config``.
-  Enum types are now correctly assigned to the schema. Previously they
   were schema-less.
-  New module ``mbdata.sample_data`` with a tiny sample of the
   MusicBrainz database useful for testing.

Version 2015.06.20
==================

-  Added ``mbdata.config`` for configuring the SQLAlchemy base/metadata
   to be used in the models.

Version 2015.01.10
==================

-  Initial release.
