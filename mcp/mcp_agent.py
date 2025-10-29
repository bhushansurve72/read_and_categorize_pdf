from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
import requests

# ------------------------------------------------
# Tools (connected to mock MCP APIs)
# ------------------------------------------------
@tool("activate_card", return_direct=True)
def activate_card_tool(card_number: str):
    """Activate a customer's card."""
    response = requests.post(
        "http://localhost:8000/activate_card",
        json={"card_number": card_number}
    )
    return response.json()["message"]

@tool("update_address", return_direct=True)
def update_address_tool(account_id: str, new_address: str):
    """Update a customer's mailing address."""
    response = requests.post(
        "http://localhost:8000/update_address",
        json={"account_id": account_id, "new_address": new_address}
    )
    return response.json()["message"]

@tool("close_account", return_direct=True)
def close_account_tool(account_id: str):
    """Close a customer's account."""
    response = requests.post(
        "http://localhost:8000/close_account",
        json={"account_id": account_id}
    )
    return response.json()["message"]

# ------------------------------------------------
# Build LangGraph agent
# ------------------------------------------------
tools = [activate_card_tool, update_address_tool, close_account_tool]
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
memory = MemorySaver()
agent_graph = create_react_agent(llm, tools=tools, checkpointer=memory)

def run_agent(user_input: str):
    """Invokes the LangGraph agent with user input."""
    result = agent_graph.invoke(
        {"input": user_input},
        config={"configurable": {"thread_id": "ui-session"}},
    )
    return result["output"]

if __name__ == "__main__":
    print(run_agent("Activate card number 1234-5678-9999-0001"))
