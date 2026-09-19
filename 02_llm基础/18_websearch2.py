import os
from openai import OpenAI
from datetime import datetime

from dotenv import load_dotenv

# 确保这一行在 os.getenv() 之前！
load_dotenv() 

def realize_think_while_search():

    # 1. 初始化OpenAI客户端
    client = OpenAI(
        base_url="https://ark.cn-beijing.volces.com/api/v3", 
        api_key=os.getenv("ARK_API_KEY")
    )

    # 2. 定义系统提示词（核心：规范“何时搜”“怎么搜”“怎么展示思考”）
    system_prompt = """
    你是AI个人助手，需实现“边想边搜边答”，核心规则如下：
    一、思考与搜索判断（必须实时输出思考过程）：
    1. 若问题涉及“时效性（如近3年数据）、知识盲区（如具体企业薪资）、信息不足”，必须调用web_search；
    2. 思考时需说明“是否需要搜索”“为什么搜”“搜索关键词是什么”。

    二、回答规则：
    1. 优先使用搜索到的资料，引用格式为`[1] (URL地址)`；
    2. 结构清晰（用序号、分段），多使用简单易懂的表述；
    3. 结尾需列出所有参考资料（格式：1. [资料标题](URL)）。
    """

    # 3. 构造API请求（触发思考-搜索-回答联动）
    response = client.responses.create(
        model="doubao-seed-2-1-pro-260628",  
        input=[
            # 系统提示词（指导AI行为）
            {"role": "system", "content": [{"type": "input_text", "text": system_prompt}]},
            # 用户问题（可替换为任意需边想边搜的问题）
            {"role": "user", "content": [{"type": "input_text", "text": "世界500强企业在国内所在的城市，近三年的平均工资是多少？"}]}
        ],
        tools=[
            # 配置Web Search工具参数
            {
                "type": "web_search",
                "limit": 10,  # 最多返回10条搜索结果
                "sources": ["toutiao", "douyin", "moji"],  # 优先从头条内容、抖音百科，墨迹天气搜索
                "user_location": {  # 优化地域相关搜索结果（如国内城市）
                    "type": "approximate",
                    "country": "中国",
                    "region": "浙江",
                    "city": "杭州"
                }
            }
        ],
        stream=True,  # 启用流式响应（核心：实时获取思考、搜索、回答片段）
    )

    # 4. 处理流式响应（实时展示“思考-搜索-回答”过程）
    # 状态变量：避免重复打印标题
    thinking_started = False  # AI思考过程是否已开始打印
    answering_started = False  # AI回答是否已开始打印

    print("=== 边想边搜启动 ===")
    for chunk in response:  # 遍历每一个实时返回的片段（chunk）
        chunk_type = getattr(chunk, "type", "")  # 获取片段类型（思考/搜索/回答）

        # ① 处理AI思考过程（实时打印“为什么搜、搜什么”）
        if chunk_type == "response.reasoning_summary_text.delta":
            if not thinking_started:
                print(f"\n🤔 AI思考中 [{datetime.now().strftime('%H:%M:%S')}]:")
                thinking_started = True
            # 打印思考内容（delta为实时增量文本）
            print(getattr(chunk, "delta", ""), end="", flush=True)

        # ② 处理搜索状态（开始/完成提示）
        elif "web_search_call" in chunk_type:
            if "in_progress" in chunk_type:
                print(f"\n\n🔍 开始搜索 [{datetime.now().strftime('%H:%M:%S')}]")
            elif "completed" in chunk_type:
                print(f"\n✅ 搜索完成 [{datetime.now().strftime('%H:%M:%S')}]")

        # ③ 处理搜索关键词（展示AI实际搜索的内容）
        elif (chunk_type == "response.output_item.done" 
              and hasattr(chunk, "item") 
              and str(getattr(chunk.item, "id", "")).startswith("ws_")):  # ws_为搜索结果标识
            if hasattr(chunk.item.action, "query"):
                search_keyword = chunk.item.action.query
                print(f"\n📝 本次搜索关键词：{search_keyword}")

        # ④ 处理最终回答（实时整合搜索结果并输出）
        elif chunk_type == "response.output_text.delta":
            if not answering_started:
                print(f"\n\n💬 AI回答 [{datetime.now().strftime('%H:%M:%S')}]:")
                print("-" * 50)
                answering_started = True
            # 打印回答内容（实时增量输出）
            print(getattr(chunk, "delta", ""), end="", flush=True)

    # 5. 流程结束
    print(f"\n\n=== 边想边搜完成 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ===")

# 运行函数
if __name__ == "__main__":
    realize_think_while_search()