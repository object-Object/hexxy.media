import pytest
from fastapi.testclient import TestClient

from hexxy_media.api.app import app as hexxy_media_app


@pytest.fixture
def app():
    return TestClient(hexxy_media_app)
