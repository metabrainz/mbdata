#################
Development Guide
#################

Development Setup
=================

Clone the repository and setup virtualenv::

    git clone git@github.com:metabrainz/mbdata.git
    cd mbdata/
    virtualenv -p python3 venv
    source venv/bin/activate
    pip install poetry
    poetry install
    poetry self add 'poetry-dynamic-versioning[plugin]'

Updating SQL files and models
=============================

Run these scripts to update SQL files and rebuild SQLAlchemy models from them::

    ./scripts/update_sql.sh $desired_git_branch_or_tag
    ./scripts/update_models.sh

Release a new version
=====================

1. Add notes to ``CHANGELOG.rst``

2. Create a new Github release.

3. The publish workflow will build a new package distribution and upload it to pypi.
