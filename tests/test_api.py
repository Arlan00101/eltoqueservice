import pytest
from unittest.mock import patch, Mock
from app import create_app
from app.config import Config


@pytest.fixture
def app():
    app = create_app("development")
    app.config["API_KEY"] = "test_api_key"
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_header():
    return {"X-API-Key": "test_api_key"}


class TestHealthCheck:
    def test_health_check(self, client):
        response = client.get("/v1/salud")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "ok"


class TestAuthentication:
    def test_no_api_key(self, client):
        response = client.get("/v1/tasas")
        assert response.status_code == 401
        data = response.get_json()
        assert "error" in data

    def test_invalid_api_key(self, client):
        response = client.get("/v1/tasas", headers={"X-API-Key": "wrong_key"})
        assert response.status_code == 403

    def test_missing_config(self, app, client):
        app.config.pop("API_KEY", None)
        response = client.get("/v1/tasas", headers={"X-API-Key": "any"})
        assert response.status_code == 500


class TestTasasEndpoints:
    @patch("app.services.eltoque.requests.get")
    def test_get_tasas_informal(self, mock_get, client, auth_header):
        mock_response = Mock()
        mock_response.json.return_value = {"USD": 520, "EUR": 590, "MLC": 400}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        response = client.get("/v1/tasas/informal", headers=auth_header)
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert "data" in data

    @patch("app.services.eltoque.requests.get")
    def test_get_tasas_oficial(self, mock_get, client, auth_header):
        mock_response = Mock()
        mock_response.json.return_value = {"USD": 24, "EUR": 26}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        response = client.get("/v1/tasas/oficial", headers=auth_header)
        assert response.status_code == 200

    @patch("app.services.eltoque.requests.get")
    def test_get_tasas_all(self, mock_get, client, auth_header):
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        response = client.get("/v1/tasas", headers=auth_header)
        assert response.status_code == 200


class TestHistorico:
    @patch("app.services.eltoque.requests.get")
    def test_historico_sin_fechas(self, mock_get, client, auth_header):
        response = client.get("/v1/tasas/historico", headers=auth_header)
        assert response.status_code == 400

    @patch("app.services.eltoque.requests.get")
    def test_historico_con_fechas(self, mock_get, client, auth_header):
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        response = client.get(
            "/v1/tasas/historico?date_from=2024-01-01%2000%3A00%3A00&date_to=2024-01-01%2023%3A59%3A59",
            headers=auth_header,
        )
        assert response.status_code == 200

    @patch("app.services.eltoque.requests.get")
    def test_historico_mas_de_24_horas(self, mock_get, client, auth_header):
        response = client.get(
            "/v1/tasas/historico?date_from=2024-01-01%2000%3A00%3A00&date_to=2024-01-02%2001%3A00%3A00",
            headers=auth_header,
        )
        assert response.status_code == 400
        data = response.get_json()
        assert "24 horas" in data["error"]

    @patch("app.services.eltoque.requests.get")
    def test_historico_formato_invalido(self, mock_get, client, auth_header):
        response = client.get(
            "/v1/tasas/historico?date_from=2024-01-01&date_to=2024-01-02",
            headers=auth_header,
        )
        assert response.status_code == 400
        data = response.get_json()
        assert "formato" in data["error"].lower()


class TestErrors:
    @patch("app.services.eltoque.requests.get")
    def test_api_error(self, mock_get, client, auth_header):
        import requests

        mock_get.side_effect = requests.exceptions.RequestException("Error de conexión")

        response = client.get("/v1/tasas/informal", headers=auth_header)
        assert response.status_code == 500
        data = response.get_json()
        assert data["success"] is False
