from app.main import health


def test_health_is_available() -> None:
    response = health()

    assert response.name == "geosense-api"
    assert response.status == "ok"
