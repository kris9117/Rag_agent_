from app.agent.rag_node import response_requires_escalation


def test_normal_vpn_setup_does_not_escalate():
    query = "How do I connect to the company VPN?"
    response = (
        "Contact IT support if the VPN client continues to fail."
    )

    assert response_requires_escalation(query, response) is False


def test_repeated_vpn_failure_escalates():
    query = "My VPN authentication keeps failing repeatedly."
    response = "Contact IT support."

    assert response_requires_escalation(query, response) is True


def test_explicit_escalation_request():
    query = "Please escalate my unresolved VPN issue."
    response = "The issue should be escalated."

    assert response_requires_escalation(query, response) is True


def test_generic_support_guidance_does_not_escalate():
    query = "How do I reset my password?"
    response = (
        "Follow the password reset process. "
        "Contact IT support if needed."
    )

    assert response_requires_escalation(query, response) is False


def test_security_issue_escalates():
    query = "I noticed suspicious activity on my account."
    response = "This should be reported to the security team."

    assert response_requires_escalation(query, response) is True