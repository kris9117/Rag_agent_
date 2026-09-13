import pytest


@pytest.fixture
def mock_llm(monkeypatch):
    class MockLLMService:
        def understand_request(self, query):
            query_lower = query.lower()

            if "create" in query_lower and "ticket" in query_lower:
                return {
                    "intent": "CREATE_TICKET",
                    "entities": {
                        "category": "Software",
                        "priority": "medium",
                        "description": query,
                    },
                    "confidence": 0.99,
                }

            if "account" in query_lower and "locked" in query_lower:
                return {
                    "intent": "ACCOUNT_STATUS",
                    "entities": {},
                    "confidence": 0.99,
                }

            return {
                "intent": "KNOWLEDGE",
                "entities": {},
                "confidence": 0.90,
            }

        def generate_tool_response(
            self,
            query,
            intent,
            tool_results,
        ):
            result = tool_results[0]

            if result.get("success"):
                return "Mock tool response generated successfully."

            return "The requested operation failed."

        def generate_rag_response(
            self,
            query,
            retrieved_context,
        ):
            return "Mock RAG response generated successfully."

    monkeypatch.setattr(
        "app.agent.graph.LLMService",
        MockLLMService,
    )