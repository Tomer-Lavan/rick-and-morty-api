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


def test_get_episodes_with_most_characters(auth_header):
    response = client.get(
        "/episodes/episodes_with_most_characters", headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for item in response.json():
        assert isinstance(item, dict)
        assert "id" in item
        assert "name" in item
        assert "air_date" in item
        assert "episode" in item
        assert isinstance(item["episode"], str)
        assert "characters" in item
        assert isinstance(item["characters"], list)


def test_get_episodes_with_most_characters_custom_k(auth_header):
    response = client.get(
        "/episodes/episodes_with_most_characters?top=5", headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 5
    for item in response.json():
        assert isinstance(item, dict)
        assert "id" in item
        assert "name" in item
        assert "air_date" in item
        assert "episode" in item
        assert isinstance(item["episode"], str)
        assert "characters" in item
        assert isinstance(item["characters"], list)


def test_get_atypical_episodes(auth_header):
    response = client.get(
        "/episodes/atypical_episodes", headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
