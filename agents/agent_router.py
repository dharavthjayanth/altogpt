from langchain.agents import initialize_agent, AgentType
from langchain_community.chat_models import ChatOpenAI
from backend.backend_inference_main.agent_graph import (
    get_room_status_tool,
    calculate_power_bill_tool,
    retrieve_rag_knowledge_tool
)
import os

def get_langchain_agent():
    llm = ChatOpenAI(
        temperature=0.3,
        model="gpt-3.5-turbo",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    tools = [
        get_room_status_tool,
        calculate_power_bill_tool,
        retrieve_rag_knowledge_tool
    ]

    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True
    )
