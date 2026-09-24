from typing import TypedDict, Literal
from uuid import uuid4

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command


class RefundState(TypedDict):
    order_id: str
    amount_fen: int
    reason: str
    status: str


# 1. 模拟 Agent 生成退款建议
def propose_refund(state: RefundState):
    # 实际项目中可以在这里查询订单、调用模型。
    # 金额使用整数“分”，避免浮点数精度问题。
    return {
        "amount_fen": 29900,
        "reason": "商品损坏，建议退款",
        "status": "pending_approval",
    }


# 2. 人工审批节点
def review_refund(
    state: RefundState,
) -> Command[Literal["execute_refund", "cancel_refund"]]:

    decision = interrupt({
        "question": "是否批准本次退款？",
        "order_id": state["order_id"],
        "amount_fen": state["amount_fen"],
        "reason": state["reason"],
    })

    # 恢复之后，decision 才会获得人工提交的数据。
    # 只有明确的 True 才算批准。
    if (
        isinstance(decision, dict)
        and decision.get("approved") is True
    ):
        return Command(goto="execute_refund")

    return Command(goto="cancel_refund")


# 3. 模拟执行退款
def execute_refund(state: RefundState):
    print(
        f"[模拟退款] 订单：{state['order_id']}，"
        f"金额：{state['amount_fen'] / 100:.2f} 元"
    )
    return {"status": "refund_simulated"}


# 4. 拒绝退款
def cancel_refund(state: RefundState):
    print("主管拒绝，未执行退款")
    return {"status": "rejected"}


# 5. 构建工作流
builder = StateGraph(RefundState)

builder.add_node("propose_refund", propose_refund)
builder.add_node("review_refund", review_refund)
builder.add_node("execute_refund", execute_refund)
builder.add_node("cancel_refund", cancel_refund)

builder.add_edge(START, "propose_refund")
builder.add_edge("propose_refund", "review_refund")

# review_refund 使用 Command 动态选择下一节点，
# 因此这里不再给它添加通向执行节点的固定边。
builder.add_edge("execute_refund", END)
builder.add_edge("cancel_refund", END)

app = builder.compile(checkpointer=InMemorySaver())

config = {
    "configurable": {
        "thread_id": f"refund-{uuid4()}"
    }
}


# 6. 第一次调用：运行到人工审批处
result = app.invoke(
    {
        "order_id": "ORDER-1001",
        "amount_fen": 0,
        "reason": "",
        "status": "created",
    },
    config=config,
)

print("待审批内容：", result["__interrupt__"][0].value)


# 7. 命令行模拟主管点击审批按钮
approved = input("是否批准退款？输入 y 批准：").strip().lower() == "y"


# 8. 第二次调用：把审批结果交给工作流
final_result = app.invoke(
    Command(resume={"approved": approved}),
    config=config,
)

print("最终状态：", final_result["status"])