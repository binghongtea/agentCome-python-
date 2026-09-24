from langgraph.graph import StateGraph,START,END
from typing_extensions import TypedDict

class customState(TypedDict):
    question:str
    category:str
    answer:str

def classify_question_node(state: customState):
    """分类问题"""
    if "退款" in state["question"]:
        return {
            "category": "退款",
        }
    elif "物流" in state["question"]:
        return {
            "category": "物流",
        }
    else:
        return {
            "category": "其他问题",
            "answer": "其他问题"
        }

def handle_refund_question(state: customState):
    """处理退款问题"""
    return {
        "answer": "退款问题处理"
    }

def handle_logistics_question(state: customState):
    """处理物流问题"""
    return {
        "answer": "物流问题处理"
    }

def handle_other_question(state: customState):
    """处理其他问题"""
    return {
        "answer": "其他问题处理"
    }

def route_question(state: customState):
    """根据分类路由问题"""
    return state["category"]

workflow = StateGraph(customState)

workflow.add_node("classify",classify_question_node)
workflow.add_node("handle_refund",handle_refund_question)
workflow.add_node("handle_logistics",handle_logistics_question)
workflow.add_node("handle_other",handle_other_question)

workflow.add_edge(START,"classify")
workflow.add_conditional_edges("classify",route_question,{
    "退款": "handle_refund",
    "物流": "handle_logistics",
    "其他问题": "handle_other",
})
workflow.add_edge("handle_refund",END)
workflow.add_edge("handle_logistics",END)
workflow.add_edge("handle_other",END)

app = workflow.compile()

result = app.invoke({"question": "这东西太差了，我不要了，还我钱！","category":"","answer":""})

print(result)


