from app import PORTFOLIOS, app


def setup_function():
    PORTFOLIOS.clear()


def test_health_endpoint():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_create_portfolio_success():
    client = app.test_client()
    response = client.post(
        "/api/portfolios",
        json={"name": "Hadi", "title": "Software Engineer", "bio": "Builds full stack apps"},
    )
    body = response.get_json()
    assert response.status_code == 201
    assert body["id"] == 1
    assert body["name"] == "Hadi"


def test_create_portfolio_validation_error():
    client = app.test_client()
    response = client.post("/api/portfolios", json={"name": "", "title": ""})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_get_missing_portfolio():
    client = app.test_client()
    response = client.get("/api/portfolios/99")
    assert response.status_code == 404
