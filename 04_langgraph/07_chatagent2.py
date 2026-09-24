import os
from openai import OpenAI
from dotenv import load_dotenv
from langgraph.graph import StateGraph,START,END,MessagesState
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

API_KEY = os.getenv("ARK_API_KEY")
client=OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=API_KEY,
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
# ========== 关键修复：langchain消息对象 → openai字典格式 ==========
    def lc_msg_to_dict(msg):
        if isinstance(msg, SystemMessage):
            return {"role": "system", "content": msg.content}
        elif isinstance(msg, HumanMessage):
            return {"role": "user", "content": msg.content}
        elif isinstance(msg, AIMessage):
            return {"role": "assistant", "content": msg.content}
        else:
            raise ValueError(f"不识别的消息类型：{type(msg)}")

    # 拼接system提示词 + 历史消息，全部转为字典
    openai_msg_list = [{"role":"system", "content":system_prompt}]
    for msg in state["messages"]:
        openai_msg_list.append(lc_msg_to_dict(msg))
    response = client.chat.completions.create(
        model="doubao-seed-2-1-pro-260628",
        messages=openai_msg_list,
        extra_body={"thinking": {"type": "enabled"}},
    )

    return {
        "messages": [AIMessage(content=response.choices[0].message.content)],
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
