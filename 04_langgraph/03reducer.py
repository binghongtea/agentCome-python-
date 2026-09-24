from langgraph.graph import StateGraph,START,END
from typing_extensions import TypedDict
from typing import Annotated
import operator

class GradeState(TypedDict):
    """成绩状态"""
    name: str
    grade: Annotated[int, operator.add]
    history: Annotated[list[str], operator.add]

def add_chinese_grade_node(state: GradeState):
    """添加语文成绩"""

    grade = int(input("请输入语文成绩: "))
    message = f"添加语文成绩: {grade}"
    return {
        "grade": grade,
        "history": [message]
    }

def add_math_grade_node(state: GradeState):
    """添加数学成绩"""
    grade = int(input("请输入数学成绩: "))
    message = f"添加数学成绩: {grade}"
    return {
        "grade": grade,
        "history": [message]
    }

def add_english_grade_node(state: GradeState):
    """添加英语成绩"""
    grade = int(input("请输入英语成绩: "))
    message = f"添加英语成绩: {grade}"
    return {
        "grade": grade,
        "history": [message]
    }

workflow = StateGraph(GradeState)

workflow.add_node("add_chinese_grade",add_chinese_grade_node)
workflow.add_node("add_math_grade",add_math_grade_node)
workflow.add_node("add_english_grade",add_english_grade_node)
workflow.add_edge(START,"add_chinese_grade")
workflow.add_edge("add_chinese_grade","add_math_grade")
workflow.add_edge("add_math_grade","add_english_grade")
workflow.add_edge("add_english_grade",END)

app = workflow.compile()
result = app.invoke({"name": "张三", "grade": 0, "history": []})
print(result)
    
