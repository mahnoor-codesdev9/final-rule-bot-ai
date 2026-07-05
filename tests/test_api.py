"""
API tests for RuleBot AI.
"""

from fastapi.testclient import TestClient

from api.server import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_settings_endpoint_hides_secrets():
    response = client.get("/settings")
    data = response.json()

    assert response.status_code == 200
    assert "providers" in data
    assert "api_key" not in str(data).lower()


def test_chat_endpoint_keeps_existing_contract():
    client.delete("/history")

    response = client.post(
        "/chat",
        json={
            "message": "hello",
        },
    )
    data = response.json()

    assert response.status_code == 200
    assert data["response"]
    assert data["mode"] == "rule"


def test_ai_mode_falls_back_without_provider_keys():
    client.delete("/history")

    response = client.post(
        "/chat",
        json={
            "message": "hello",
            "mode": "ai",
        },
    )
    data = response.json()

    assert response.status_code == 200
    assert data["response"]
    assert data["mode"] == "rule"


def test_history_and_stats_endpoints():
    client.delete("/history")
    client.post(
        "/chat",
        json={
            "message": "python",
        },
    )

    history = client.get("/history").json()["history"]
    stats = client.get("/stats").json()

    assert len(history) == 2
    assert stats["total_messages"] == 2
    assert stats["rule_responses"] == 1
