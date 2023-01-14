import os
import tempfile
import pytest

from EveryRockBeatEver import create_app


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""

    # create the app with common test config
    app = create_app({"TESTING": True})

    # create the database and load test data
    with app.app_context():
        ...

    yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()
