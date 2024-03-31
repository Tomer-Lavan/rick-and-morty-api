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


def test_get_most_common_species(auth_header):
    response = client.get("/insights/most_common_species", headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "most_common_species" in response.json()
    assert isinstance(response.json()["most_common_species"], list)


def test_predict_survival_chance(auth_header):
    location = "Earth (C-137)"
    gender = "Male"
    species = "Human"
    response = client.get(
        f"/insights/analysis/predict_survival_chance?location={location}&gender={gender}&species={species}", headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "predicted_survival_chance" in response.json()
    assert isinstance(response.json()["predicted_survival_chance"], float)
    assert 0 <= response.json()["predicted_survival_chance"] <= 100
