from langgraph.graph import StateGraph,START,END
from typing_extensions import TypedDict
from typing import Annotated
import operator
# 1.定义状态类型,这里用的reducer模式，累加
class CountState(TypedDict):
    count: Annotated[int, operator.add]
    history: Annotated[list[str], operator.add]

# 2.定义节点
def increment_node(state: CountState):
    """计数器加一"""
    new_count = state["count"] + 1
    message = f"count {state['count']} -> {new_count}"
    
    return {
        "count": new_count,
        "history": [message]
    }
    

def double_node(state: CountState):
    """计数器乘二"""
    new_count = state["count"] * 2
    message = f"count {state['count']} -> {new_count}"

    return {
        "count": new_count,
        "history": [message]
    }

def report_node(state: CountState):
    """报告当前计数"""
    message = f"最终count: {state['count']}"
    return {
        "history": [message]
    }

# 3.创建图
workflow = StateGraph(CountState)

# 4.添加节点
workflow.add_node("increment",increment_node)
workflow.add_node("double",double_node)
workflow.add_node("report",report_node)

# 5.连接节点，添加边
workflow.add_edge(START,"increment")
workflow.add_edge("increment","double")
workflow.add_edge("double","report")
workflow.add_edge("report",END)

# 6.编译
app = workflow.compile()

# 7.执行
result = app.invoke({"count": 20, "history": []})

print(result)