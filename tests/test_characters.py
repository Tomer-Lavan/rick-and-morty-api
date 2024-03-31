from fastapi.testclient import TestClient
from app.main import app
from app.services.auth import create_access_token
import pytest

client = TestClient(app)


@pytest.fixture(scope="module")
def auth_header():
    token = create_access_token(
        data={"sub": "tomer"}
    )
    return {"Authorization": f"Bearer {token}"}


def test_get_characters(auth_header):
    response = client.get("/characters", headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_characters_with_filters(auth_header):
    response = client.get(
        "/characters?name=Rick&status=Alive", headers=auth_header)
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)


def test_get_characters_groups_by_origin(auth_header):
    response = client.get("/characters/groups_by_origin",
                          headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_get_origin_inconsistencies(auth_header):
    response = client.get(
        "/characters/origin_inconsistencies", headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_character_appearances(auth_header):
    response = client.get(
        "/characters/analysis/character_appearances", headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_species_survival_rates(auth_header):
    response = client.get(
        "/characters/analysis/species_survival_rates", headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_gender_survival_rates(auth_header):
    response = client.get(
        "/characters/analysis/gender_survival_rates", headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
