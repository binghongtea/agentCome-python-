from langgraph.graph import StateGraph,START,END
from typing_extensions import TypedDict
from typing import Annotated
import operator

class LoopState(TypedDict):
    question: str
    answer: str
    quality_score: float
    iteration: Annotated[int, operator.add]
    max_iteration: int

def GenerateAndImproveAnswer_node(state: LoopState):
    """生成和改进答案"""
    if state["iteration"] == 0:
        return {
            "answer": "初始答案",
            "quality_score": 0.5,
            "iteration": 1,
        }
    elif state["iteration"] == 1:
        return {
            "answer": "改进答案",
            "quality_score": 0.8,
            "iteration": 1,
        }
    else:
        return {
            "answer": "最终答案",
            "quality_score": 1,
            "iteration": 1,
        }

def CheckAnswer(state: LoopState):
    """检查答案"""
    if state["quality_score"] >= 0.9:
        return "over"
    elif state["iteration"] >= state["max_iteration"]:
        return "over"
    else:
        return "continueGenerate"

workflow = StateGraph(LoopState)
workflow.add_node("GenerateAndImproveAnswer",GenerateAndImproveAnswer_node)
    
workflow.add_edge(START,"GenerateAndImproveAnswer")
workflow.add_conditional_edges("GenerateAndImproveAnswer",CheckAnswer,{
    "continueGenerate": "GenerateAndImproveAnswer",
    "over": END,
    "error": END,
   })

app = workflow.compile()
result = app.invoke({"question": "你好", "answer": "", "quality_score": 0, "iteration": 0, "max_iteration": 3})
print(result)
    