import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

app_module = importlib.import_module("app")


def test_health_endpoint():
    client = app_module.app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "OK"


def test_investigate_endpoint_requires_topic():
    client = app_module.app.test_client()
    response = client.post("/api/investigate", json={})
    assert response.status_code == 400
    assert "required" in response.get_json()["error"].lower()


def test_verify_credibility_route_returns_structured_result(monkeypatch):
    def fake_search_topic(topic):
        return {"topic": topic, "sources": [{"title": "Example", "url": "https://example.com", "snippet": "Example snippet"}]}

    def fake_investigate(topic, sources):
        return "This claim appears credible and supported by the available evidence."

    import routes

    monkeypatch.setattr(routes, "search_topic", fake_search_topic)
    monkeypatch.setattr(routes, "investigate", fake_investigate)

    client = app_module.app.test_client()
    response = client.post("/api/verify-credibility", json={"topic": "Test claim"})
    assert response.status_code == 200
    body = response.get_json()
    assert body["verdict"] == "Highly Credible"
    assert body["sources"][0]["name"] == "Example"
