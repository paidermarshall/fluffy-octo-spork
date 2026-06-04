import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


INITIAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture
def client():
    activities.clear()
    activities.update(copy.deepcopy(INITIAL_ACTIVITIES))
    return TestClient(app)
