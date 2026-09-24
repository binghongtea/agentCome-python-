import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph,START,END,MessagesState
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("ARK_API_KEY")
llm=ChatOpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=API_KEY,
    model="doubao-seed-2-1-pro-260628",
    temperature=0,
)

agent = create_agent(
    model=llm
)
class ChatState(MessagesState):
    user_name: str
    conversation_count: int

def chatbot_node(state: ChatState):
    """聊天节点"""
    system_prompt = f"""你是一个友好的AI助手,
    用户名：{state.get("user_name",'用户')}
    对话次数：{state.get("conversation_count",0)}
    """
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = agent.invoke(
        {"messages": messages}
    )

    return {
        "messages":[AIMessage(content=response["messages"][-1].content)],
        "conversation_count": state.get("conversation_count",0) + 1,
    }

workflow = StateGraph(ChatState)
workflow.add_node("chatbot",chatbot_node)
workflow.add_edge(START,"chatbot")
workflow.add_edge("chatbot",END)

app = workflow.compile()

state = {"messages": [], "user_name": "麻袋", "conversation_count": 0}

conversations = [
    "你好，我是麻袋",
    "我刚才说我叫什么？",
    "帮我推荐一本python书"
]

for user_input in conversations:
    print(f"用户：{user_input}")
    state["messages"].append(HumanMessage(content=user_input))
    result = app.invoke(state)
    state = result
    print(f"助手：{result['messages'][-1].content}\n")
