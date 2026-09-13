from app.services.observability import log_event
from langgraph.graph import END, START, StateGraph

from app.agent.router import determine_route
from app.agent.state import AgentState
from app.agent.tool_executor import execute_tool
from app.services.llm_service import LLMService
from app.agent.rag_node import rag_node


def understand_request(state: AgentState) -> dict:
    """Interpret the user's request using the LLM."""

    service = LLMService()
    result = service.understand_request(state["query"])

    entities = result.entities.model_dump()

    log_event(
        "request_understood",
        request_id=state.get("request_id"),
        user_id=state.get("user_id"),
        intent=result.intent,
        entity_keys=list(entities.keys()),
    )

    return {
        "intent": result.intent,
        "entities": entities,
        "status": "REQUEST_UNDERSTOOD",
    }


def route_request(state: AgentState) -> dict:
    """Map the interpreted intent and query to a controlled route."""

    route = determine_route(
        intent=state.get("intent"),
        query=state.get("query", ""),
    )

    log_event(
        "route_selected",
        request_id=state.get("request_id"),
        user_id=state.get("user_id"),
        intent=state.get("intent"),
        route=route,
    )

    return {
        "route": route,
        "status": "ROUTE_SELECTED",
    }


def tool_node(state: AgentState) -> dict:
    """Execute an approved enterprise tool for TOOL routes."""

    intent = state.get("intent")
    entities = state.get("entities", {})

    intent_to_tool = {
        "ACCOUNT_STATUS": ("ACCOUNT_STATUS", "user_id"),
        "DEVICE_STATUS": ("DEVICE_STATUS", "device_id"),
        "TICKET_LOOKUP": ("TICKET_LOOKUP", "ticket_id"),
        "PASSWORD_RESET": ("PASSWORD_RESET", "user_id"),
    }

    tool_config = intent_to_tool.get(intent)

    if tool_config is None:
        return {
            "validation_errors": [
                f"No tool mapping exists for intent: {intent}"
            ],
            "status": "TOOL_MAPPING_ERROR",
        }

    tool_name, required_entity = tool_config
    entity_value = entities.get(required_entity)

    # Use the authenticated API user_id when the LLM
    # does not extract it into the entities object.
    if not entity_value and required_entity == "user_id":
        entity_value = state.get("user_id")

    if not entity_value:
        return {
            "validation_errors": [
                f"Missing required information: {required_entity}"
            ],
            "status": "CLARIFICATION_REQUIRED",
        }

    arguments = {
        required_entity: entity_value,
    }

    result = execute_tool(
        tool_name=tool_name,
        arguments=arguments,
    )

    tool_call = {
        "tool_name": tool_name,
        "arguments": arguments,
    }

    tool_result = result

    tool_results = [tool_result]

    if not result.get("success"):
        return {
            "tool_calls": [tool_call],
            "tool_results": tool_results,
            "status": "TOOL_FAILED",
        }

    service = LLMService()

    response = service.generate_tool_response(
        query=state["query"],
        intent=intent,
        tool_results=tool_results,
   )

    return {
        "tool_calls": [tool_call],
        "tool_results": tool_results,
        "response": response,
        "status": "TOOL_COMPLETED",
    }

def select_after_tool(state: AgentState) -> str:
    """Determine what happens after tool execution."""

    status = state.get("status")

    if status == "CLARIFICATION_REQUIRED":
        return "clarification_node"

    return END


def knowledge_node(state: AgentState) -> AgentState:
    """Answer general knowledge-base questions using grounded RAG."""

    return rag_node(state)


def rag_tool_node(state: AgentState) -> AgentState:
    """Handle RAG-based troubleshooting requests."""

    return rag_node(state)


def clarification_node(state: AgentState) -> dict:
    errors = state.get("validation_errors", [])

    log_event(
        "clarification_required",
        request_id=state.get("request_id"),
        user_id=state.get("user_id"),
        intent=state.get("intent"),
        missing_fields=errors,
    )

    if errors:
        response = (
            "I need additional information to process your request. "
            + " ".join(errors)
        )
    else:
        response = (
            "I need more information to process your request."
        )

    return {
        "status": "CLARIFICATION_REQUIRED",
        "response": response,
    }


def escalation_node(state: AgentState) -> dict:
    log_event(
        "request_escalated",
        request_id=state.get("request_id"),
        user_id=state.get("user_id"),
        intent=state.get("intent"),
    )

    return {
        "status": "ESCALATION_REQUIRED",
        "escalation_required": True,
        "response": (
            "This request requires escalation to the IT support team."
        ),
    }


def action_node(state: AgentState) -> AgentState:
    """Create an IT support ticket from validated request entities."""

    entities = state.get("entities", {})

    user_id = state.get("user_id") or entities.get("user_id")
    category = entities.get("category")
    priority = entities.get("priority")
    description = entities.get("description")

    validation_errors = []

    if not user_id:
        validation_errors.append("Missing required information: user_id")

    if not category:
        validation_errors.append("Missing required information: category")

    if not priority:
        validation_errors.append("Missing required information: priority")

    if not description:
        validation_errors.append(
            "Missing required information: description"
        )

    if validation_errors:
        return {
            **state,
            "validation_errors": validation_errors,
            "status": "CLARIFICATION_REQUIRED",
            "response": (
                "I need additional information to create the ticket. "
                + " ".join(validation_errors)
            ),
        }

    # Normalize LLM-generated enum values before tool validation.
    priority = str(priority).lower().strip()
    category = str(category).strip()
    description = str(description).strip()

    if priority not in {"low", "medium", "high"}:
        return {
            **state,
            "validation_errors": [
                "Priority must be low, medium, or high."
            ],
            "status": "CLARIFICATION_REQUIRED",
            "response": (
                "Please provide a valid priority: low, medium, or high."
            ),
        }

    arguments = {
        "user_id": user_id,
        "category": category,
        "priority": priority,
        "description": description,
    }

    result = execute_tool(
        tool_name="CREATE_TICKET",
        arguments=arguments,
    )

    tool_call = {
        "tool_name": "CREATE_TICKET",
        "arguments": arguments,
    }

    tool_results = [result]

    if not result.get("success"):
        return {
            **state,
            "tool_calls": [tool_call],
            "tool_results": tool_results,
            "status": "ACTION_FAILED",
            "response": (
                "I could not create the support ticket. "
                "Please review the information and try again."
            ),
        }

    service = LLMService()

    response = service.generate_tool_response(
        query=state["query"],
        intent=state.get("intent", "CREATE_TICKET"),
        tool_results=tool_results,
    )

    return {
        **state,
        "tool_calls": [tool_call],
        "tool_results": tool_results,
        "status": "ACTION_COMPLETED",
        "response": response,
        "validation_errors": [],
    }


def select_route(state: AgentState) -> str:
    """Select the graph node corresponding to the application route."""

    route = state.get("route")

    route_to_node = {
        "KNOWLEDGE": "knowledge_node",
        "TOOL": "tool_node",
        "RAG_TOOL": "rag_tool_node",
        "ACTION": "action_node",
        "ESCALATION": "escalation_node",
        "CLARIFICATION": "clarification_node",
    }

    return route_to_node.get(
        route ,
        "clarification_node"
    )


def build_graph():
    """Build and compile the LangGraph workflow."""

    graph = StateGraph(AgentState)

    graph.add_node("understand_request", understand_request)
    graph.add_node("route_request", route_request)
    graph.add_node("knowledge_node", knowledge_node)
    graph.add_node("tool_node", tool_node)
    graph.add_node("rag_tool_node", rag_tool_node)
    graph.add_node("action_node", action_node)
    graph.add_node("escalation_node", escalation_node)
    graph.add_node("clarification_node", clarification_node)

    graph.add_edge(START, "understand_request")
    graph.add_edge("understand_request", "route_request")

    graph.add_conditional_edges(
        "route_request",
        select_route,
        {
            "knowledge_node": "knowledge_node",
            "tool_node": "tool_node",
            "rag_tool_node": "rag_tool_node",
            "action_node": "action_node",
            "escalation_node": "escalation_node",
            "clarification_node": "clarification_node",
        },
    )

    graph.add_edge("knowledge_node", END)
    graph.add_conditional_edges(
    "tool_node",
    select_after_tool,
    {
        "clarification_node": "clarification_node",
        END: END,
    },
)
    graph.add_edge("rag_tool_node", END)
    graph.add_edge("action_node", END)
    graph.add_edge("escalation_node", END)
    graph.add_edge("clarification_node", END)

    return graph.compile()


agent_graph = build_graph()
# Backward-compatible alias for existing scripts.
graph = agent_graph