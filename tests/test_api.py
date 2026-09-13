from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "enterprise-it-support-agent"


def test_password_reset_request():
    response = client.post(
        "/api/v1/support",
        json={
            "user_id": "EMP0001",
            "query": "How do I reset my password?",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["request_id"].startswith("REQ-")
    assert data["user_id"] == "EMP0001"
    assert data["intent"] == "PASSWORD_RESET"
    assert data["route"] == "RAG_TOOL"
    assert data["status"] == "RAG_COMPLETED"
    assert isinstance(data["response"], str)
    assert data["escalation_required"] is False


def test_ticket_creation_request():
    response = client.post(
        "/api/v1/support",
        json={
            "user_id": "EMP0002",
            "query": "Create a ticket because Outlook keeps crashing",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["intent"] == "CREATE_TICKET"
    assert data["route"] == "ACTION"
    assert data["status"] == "ACTION_COMPLETED"
    assert "ticket" in data["response"].lower()


def test_escalation_request():
    response = client.post(
        "/api/v1/support",
        json={
            "user_id": "EMP0003",
            "query": "Please escalate this issue to IT support",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["intent"] == "ESCALATION"
    assert data["route"] == "ESCALATION"
    assert data["status"] == "ESCALATION_REQUIRED"
    assert data["escalation_required"] is True


def test_missing_query_validation():
    response = client.post(
        "/api/v1/support",
        json={
            "user_id": "EMP0001",
        },
    )

    assert response.status_code == 422


def test_short_query_validation():
    response = client.post(
        "/api/v1/support",
        json={
            "user_id": "EMP0001",
            "query": "Hi",
        },
    )

    assert response.status_code == 422


def test_ticket_creation_request():
    response = client.post(
        "/api/v1/support",
        json={
            "user_id": "EMP0002",
            "query": (
                "Create a high priority software ticket. "
                "Outlook keeps crashing when I open it."
            ),
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["intent"] == "CREATE_TICKET"
    assert data["route"] == "ACTION"
    assert data["status"] == "ACTION_COMPLETED"
    assert "ticket" in data["response"].lower()