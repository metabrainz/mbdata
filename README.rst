#############################
MusicBrainz SQLAlchemy Models
#############################

|pypi badge|

.. |pypi badge| image:: https://badge.fury.io/py/mbdata.svg
    :target: https://badge.fury.io/py/mbdata

If you are developing a Python application that needs access to the
`MusicBrainz <https://musicbrainz.org/>`__
`data <https://musicbrainz.org/doc/MusicBrainz_Database>`__, you can use
the ``mbdata.models`` module to get
`SQLAlchemy <http://www.sqlalchemy.org/>`__ models mapped to the
MusicBrainz database tables.

All tables from the MusicBrainz database are mapped, all foreign keys
have one-way relationships set up and some models, where it's essential
to access their related models, have two-way relationships (collections)
set up.

In order to work with the relationships efficiently, you should use the
appropriate kind of `eager
loading <http://docs.sqlalchemy.org/en/latest/orm/loading_relationships.html>`__.

Example usage of the models:

.. code:: python

    >>> from sqlalchemy import create_engine
    >>> from sqlalchemy.orm import sessionmaker
    >>> from mbdata.models import Artist
    >>> engine = create_engine('postgresql://musicbrainz:musicbrainz@127.0.0.1/musicbrainz', echo=True)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()
    >>> artist = session.query(Artist).filter_by(gid='8970d868-0723-483b-a75b-51088913d3d4').first()
    >>> print artist.name

If you use the models in your own application and want to define foreign
keys from your own models to the MusicBrainz schema, you will need to
let ``mbdata`` know which metadata object to add the MusicBrainz tables
to:

.. code:: python

    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()

    # this should be the first place where you import anything from mbdata
    import mbdata.config
    mbdata.config.configure(base_class=Base)

    # now you can import and use the mbdata models
    import mbdata.models

You can also use ``mbdata.config`` to re-map the MusicBrainz schema
names, if your database doesn't follow the original structure:

.. code:: python

    import mbdata.config
    mbdata.config.configure(schema='my_own_mb_schema')

If you need sample MusicBrainz data for your tests, you can use
``mbdata.sample_data``:

.. code:: python

    from mbdata.sample_data import create_sample_data
    create_sample_data(session)

***********
Development
***********

Normally you should work against a regular PostgreSQL database with
MusicBrainz data, but for testing purposes, you can use a SQLite
database with small data sub-set used in unit tests. You can create the
database using:

.. code:: sh

    ./bin/create_sample_db.py sample.db

Then you can change your configuration:

.. code:: sh

    DATABASE_URI = 'sqlite:///sample.db'

Running tests:

.. code:: sh

    pytest -v

If you want to see the SQL queries from a failed test, you can use the
following:

.. code:: sh

    MBDATA_DATABASE_ECHO=1 pytest -v

GitHub Actions workflow that automatically runs the tests after each commit is
`here <https://github.com/metabrainz/mbdata/actions/workflows/test.yml>`__.
