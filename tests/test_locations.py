from fastapi.testclient import TestClient
from app.main import app
from app.services.auth import create_access_token
import pytest
from typing import List, Any, Dict, Union


client = TestClient(app)


@pytest.fixture(scope="module")
def auth_header():
    token = create_access_token(
        data={"sub": "tomer"}
    )
    return {"Authorization": f"Bearer {token}"}


def test_get_locations_with_resident_counts(auth_header):
    response = client.get("/locations/resident_counts", headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for item in response.json():
        assert isinstance(item, dict)
        assert "location" in item
        assert isinstance(item["location"], str)
        assert "resident_count" in item
        assert isinstance(item["resident_count"], int)


def test_get_locations_with_resident_counts_specific(auth_header):
    response = client.get(
        "/locations/resident_counts?[1,2,3]", headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for item in response.json():
        assert isinstance(item, dict)
        assert "location" in item
        assert isinstance(item["location"], str)
        assert "resident_count" in item
        assert isinstance(item["resident_count"], int)

    assert len(response.json()) == 3


def test_location_survival_rate(auth_header):
    response = client.get(
        "/locations/analysis/location_survival_rates", headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
