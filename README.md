# agentComePython

从 Python 基础到大模型应用与 Agent 开发的学习实践仓库，包含大模型 API 调用、工具调用、Embedding、LangGraph 工作流，以及 FastAPI + MySQL 订单管理示例。

代码按主题拆分为独立脚本，适合逐个运行、阅读和修改。各模块有不同的依赖和配置要求；根目录的 `main.py` 是 IDE 生成的演示文件，没有统一启动所有功能的入口。

## 项目内容

| 模块 | 主要内容 |
| --- | --- |
| Python 基础 | 数据类型、流程控制、函数、文件操作、模块与包、面向对象、异步编程、HTTP 请求、FastAPI 入门 |
| 大模型基础 | 豆包与 DeepSeek 调用、流式输出、工具调用、思考参数、JSON 输出与修复、文件与图片输入、Responses API、联网搜索 |
| 手写 Agent | 搜索笔记、读取笔记、保存学习卡片；模型决策与工具执行循环；参数校验、执行预算、超时处理和故障实验 |
| RAG 基础 | 使用 Sentence Transformers 生成文本向量、使用 NumPy 计算向量点积 |
| LangGraph | 状态图、Reducer、条件边、循环、聊天 Agent、人工审批与中断恢复 |
| 数据库与接口 | PyMySQL 数据库操作、订单增删改查、客户名称筛选与分页 |
| 部署实践 | Docker Compose 编排 FastAPI、MySQL 与 Nginx，前端构建打包与日常运维说明 |

其中 `03_RAG` 当前演示的是向量化与向量运算，尚未实现完整的文档切分、向量库检索和问答流程。

## 目录结构

```text
agentComePython/
├── 01_python基础/          # Python 语法、异步与 FastAPI 示例
├── 02_llm基础/             # 大模型 API 与手写 Agent 示例
│   ├── demo1.py            # 带校验、预算、超时与故障实验的 Agent Runtime
│   ├── demo2.py            # 三工具 Agent 入门版，需要模型 API
│   └── workspace/          # 运行时生成的学习卡片与日志，不提交 Git
├── 03_RAG/                 # Embedding 与向量运算
├── 04_langgraph/           # 状态图与 Agent 工作流
├── 05_mysql/
│   ├── 01.py               # 数据库连接练习
│   └── demo1/              # 订单 CRUD 脚本与 FastAPI 接口
├── deploy/order-demo/      # Docker 部署、建表 SQL、打包与运维说明
├── graphic/                # 自定义 Python 包练习
├── .env.example            # 本地环境变量模板
├── .gitignore
├── main.py
├── setup.py                # graphic 包的打包配置
└── README.md
```

## 环境准备

Agent Runtime 标注的最低版本为 Python 3.10，使用 Pydantic 2。其他模块还需满足各自第三方依赖的 Python 版本要求。

克隆或下载仓库后，在项目根目录创建虚拟环境：

```bash
python -m venv .venv
```

Windows PowerShell 激活：

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS / Linux 激活：

```bash
source .venv/bin/activate
```

按需要安装对应模块的依赖，无需一次安装全部：

| 学习内容 | 安装命令 |
| --- | --- |
| 大模型调用与手写 Agent | `python -m pip install openai python-dotenv "pydantic>=2,<3" json-repair` |
| LangGraph 工作流与聊天 Agent | `python -m pip install langgraph langchain langchain-openai python-dotenv openai` |
| 文本向量与向量运算 | `python -m pip install sentence-transformers numpy` |
| FastAPI 与 MySQL | `python -m pip install fastapi uvicorn "pymysql[rsa]" python-dotenv` |
| 异步文件与 HTTP 请求示例 | `python -m pip install aiofiles requests` |
| 自定义 graphic 包 | `python -m pip install -e .` |

根目录的 `setup.py` 只配置了 `graphic` 练习包，不会安装上述全部依赖。部署后端有单独的版本清单：[backend/requirements.txt](deploy/order-demo/backend/requirements.txt)。

## 配置环境变量

在根目录复制模板，填写自己使用的配置：

```powershell
# Windows PowerShell
Copy-Item .env.example .env
```

```bash
# macOS / Linux
cp .env.example .env
```

| 变量 | 用途 |
| --- | --- |
| `ARK_API_KEY` | 豆包 / 火山方舟 API Key |
| `DEEPSEEK_API_KEY` | DeepSeek API Key |
| `AGENT_MODEL` | `demo1.py`、`demo2.py` 的模型名称，可按账号实际可用模型修改 |
| `AGENT_BASE_URL` | `demo1.py`、`demo2.py` 的模型 API 地址 |
| `MYSQL_HOST`、`MYSQL_PORT` | 本地订单示例使用的 MySQL 地址与端口 |
| `MYSQL_USER`、`MYSQL_PASSWORD`、`MYSQL_DATABASE` | MySQL 用户、密码与数据库名称 |

多数豆包示例会通过 `load_dotenv()` 加载 `.env`，并在源码中指定模型名称与 API 地址。修改 `AGENT_MODEL` 只影响读取该变量的 Agent 示例，其他脚本需修改自身配置。

`01deepseek.py`、`deepseek_agent_demo.py` 和 `19_zoom.py` 没有主动加载 `.env`，运行时需在终端或 IDE 中设置对应环境变量，例如：

```powershell
$env:DEEPSEEK_API_KEY = "你的 DeepSeek API Key"
python "02_llm基础/01deepseek.py"
```

模型调用需要有效账号和对应模型权限，可能产生 API 费用；离线 Agent 演示不需要 API Key。

## 运行示例

以下命令均从项目根目录执行。部分练习脚本包含交互输入、固定文件路径或本机地址，运行前请先阅读并按本机环境调整。

### 1. Python 基础

```bash
python "01_python基础/01_hello.py"
```

启动 FastAPI 入门示例：

```bash
python "01_python基础/23_9.5fastapi.py"
```

启动后打开 [Swagger 接口文档](http://127.0.0.1:8000/docs)。不同 FastAPI 示例使用同一端口时，应分别启动。

### 2. 大模型调用

配置 `ARK_API_KEY` 后，运行基础对话或流式输出：

```bash
python "02_llm基础/01_doubao.py"
python "02_llm基础/04_stream.py"
```

目录内还包含工具调用、结构化输出、文件输入和联网搜索等独立练习。具体参数与模型能力要求以对应脚本为准；文件示例中的素材路径需要自行配置。

### 3. 手写 Agent

先运行无需 API Key 的离线示例，观察“决策 → 调用工具 → 接收结果 → 再次决策”的过程：

```bash
python "02_llm基础/demo1.py"
```

该示例提供 `search_notes`、`read_note`、`save_report` 三个工具，从内置笔记中整理学习卡片，输出保存在 `02_llm基础/workspace/`。

运行混合故障场景、故障对比实验或内置自检：

```bash
python "02_llm基础/demo1.py" --fault mixed
python "02_llm基础/demo1.py" --experiment
python "02_llm基础/demo1.py" --self-test
```

配置模型后，可以运行入门版或启用 Runtime 的真实模型模式：

```bash
python "02_llm基础/demo2.py"
python "02_llm基础/demo1.py" --mode llm --query "整理 RAG，并保存学习卡片"
```

`demo2.py` 便于阅读基本循环；`demo1.py` 进一步实现 Pydantic 参数校验、轮数与工具调用预算、重复调用检测、工具进程超时、上下文裁剪及 JSON Lines 日志。

### 4. Embedding 与 LangGraph

```bash
python "03_RAG/01_embedding.py"
python "03_RAG/02_Similarity.py"
python "04_langgraph/01.py"
python "04_langgraph/08.py"
```

Embedding 示例首次运行会下载 `all-MiniLM-L6-v2` 模型，需要网络和本地缓存空间。`02_Similarity.py` 计算的是向量点积，没有做余弦归一化。

`04_langgraph/08.py` 演示模拟退款的人工审批：工作流先中断，命令行输入 `y` 批准后恢复执行；其他输入走拒绝分支。该示例不会发起真实退款。

### 5. MySQL 订单接口

1. 准备 MySQL，在根目录 `.env` 中填写连接配置。
2. 创建 `MYSQL_DATABASE` 指定的数据库，并为配置的用户授予相应访问权限。
3. 在该数据库中执行 [init.sql](deploy/order-demo/db/init.sql)，创建 `orders` 表。该文件只负责建表。
4. 启动接口服务：

```bash
python "05_mysql/demo1/crud.py"
```

访问 [Swagger 接口文档](http://127.0.0.1:8000/docs) 测试：

| 方法 | 路径 | 功能 | 参数 |
| --- | --- | --- | --- |
| POST | `/add_order` | 新增订单 | `customer_name`、`status`、`amount` |
| POST | `/delete_order` | 删除订单 | `order_id` |
| POST | `/edit_order` | 修改订单状态与金额 | `order_id`、`status`、`amount` |
| POST | `/select_order` | 筛选与分页查询 | `customer_name`（默认空）、`page`（默认 1）、`page_size`（默认 10） |

上述接口均通过 URL 查询参数接收数据。订单号由后端生成，金额使用 `Decimal`，SQL 使用参数绑定。

查询示例：

```bash
curl -X POST "http://127.0.0.1:8000/select_order?customer_name=&page=1&page_size=10"
```

## Docker 部署

[deploy/order-demo](deploy/order-demo/) 提供 Nginx + FastAPI + MySQL 部署配置：Nginx 提供前端静态页面，并将 `/api/` 请求转发至后端。

部署前需准备前端产物。`package.ps1` 依赖本仓库同级目录下的独立 React 项目 `reactDemoPython`，调用该项目的 `scripts/run-vite.cjs` 构建前端到 `deploy/order-demo/web/dist/`，然后复制订单后端代码并生成部署压缩包。**React 源码不在本仓库中，单独克隆本仓库不能完成前端构建。**

部署配置默认仅监听 `127.0.0.1:8080`。当前订单接口没有登录鉴权，公开使用前需补充访问控制与 HTTPS。

- [部署步骤](deploy/order-demo/README.md)
- [数据库备份、连接与代码更新](deploy/order-demo/OPERATIONS.md)

子目录中的部署文档还记录了具体环境的操作信息，复用时请替换其中的本机路径、服务器地址等配置。

## 上传 GitHub 前

仓库已提供 `.gitignore`，忽略 `.env`、虚拟环境、IDE 配置、Python 缓存、Agent 运行产物、前端构建目录与部署压缩包。提交前用 `git status` 检查实际文件列表。

`05_mysql/01.py` 含写在源码中的数据库连接配置，`02_llm基础/deepseek_agent_demo.py` 含写在源码中的 Key 回退配置。上传前请检查这些练习文件以及部署文档，确保没有填写真实密码、API Key 或不希望公开的连接信息。

`.gitignore` 不会取消追踪已提交的文件；已经被 Git 追踪的 IDE 文件或部署包需要另行从暂存索引中移除。若真实密钥曾被提交，应先撤销或轮换密钥，再处理 Git 历史。
