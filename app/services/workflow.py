from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from app.services.agents.router import intent_router
from app.services.agents.casual_agent import casual_chain
from app.services.agents.out_of_scope_agent import out_of_scope_chain
from app.services.agents.formatter import formatter_chain

from app.services.agents.company_agent import run_company_agent
from app.services.agents.user_agent import run_user_agent
from app.services.agents.vessel_agent import run_vessel_agent
from app.services.agents.defect_agent import run_defect_agent

# 1. State representing the entire flow
class AgentState(TypedDict):
    input_query: str
    intent: str
    raw_db_output: Optional[str]
    final_response: str

# 2. Nodes
async def node_router(state: AgentState):
    """Super Agent classifies intent."""
    query = state["input_query"]
    decision = await intent_router.ainvoke({"question": query})
    return {"intent": decision["intent"]}

async def node_casual(state: AgentState):
    """Replies conversationally."""
    query = state["input_query"]
    response = await casual_chain.ainvoke({"question": query})
    return {"final_response": response.content}

async def node_out_of_scope(state: AgentState):
    """Rejects irrelevant queries."""
    query = state["input_query"]
    response = await out_of_scope_chain.ainvoke({"question": query})
    return {"final_response": response.content}

async def node_company(state: AgentState):
    query = state["input_query"]
    output = await run_company_agent(query)
    return {"raw_db_output": output}

async def node_user(state: AgentState):
    query = state["input_query"]
    output = await run_user_agent(query)
    return {"raw_db_output": output}

async def node_vessel(state: AgentState):
    query = state["input_query"]
    output = await run_vessel_agent(query)
    return {"raw_db_output": output}

async def node_defect(state: AgentState):
    query = state["input_query"]
    output = await run_defect_agent(query)
    return {"raw_db_output": output}

async def node_formatter(state: AgentState):
    """Takes raw outputs and formats nicely as chatbot response."""
    query = state["input_query"]
    raw = state.get("raw_db_output", "No data retrieved.")
    final_result = await formatter_chain.ainvoke({
        "question": query,
        "raw_data": raw
    })
    return {"final_response": final_result.content}

# 3. Routing Edge
def route_domains(state: AgentState):
    intent = state.get("intent", "CASUAL")
    return intent.lower()

# 4. Orchestration Construction
builder = StateGraph(AgentState)

builder.add_node("router", node_router)
builder.add_node("casual", node_casual)
builder.add_node("out_of_scope", node_out_of_scope)
builder.add_node("company", node_company)
builder.add_node("user", node_user)
builder.add_node("vessel", node_vessel)
builder.add_node("defect", node_defect)
builder.add_node("formatter", node_formatter)

builder.set_entry_point("router")

# Super Agent dictates branch path
builder.add_conditional_edges(
    "router",
    route_domains,
    {
        "casual": "casual",
        "out_of_scope": "out_of_scope",
        "company": "company",
        "user": "user",
        "vessel": "vessel",
        "defect": "defect"
    }
)

# Casual & Out-of-Scope end immediately
builder.add_edge("casual", END)
builder.add_edge("out_of_scope", END)

# All Domain Agents converge into the Formatter
builder.add_edge("company", "formatter")
builder.add_edge("user", "formatter")
builder.add_edge("vessel", "formatter")
builder.add_edge("defect", "formatter")

# Formatter ends immediately
builder.add_edge("formatter", END)

# Compile Application
graph_app = builder.compile()
