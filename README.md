# my-codex-skills

这是一个本地 Codex skills 仓库，当前包含 5 个可复用 skill，分别面向项目初始化、`.issues` 任务规范化、`.issues` 自动开发流、Excel 需求拆解，以及 YOLO 数据集转换。

## 仓库结构

```text
.
├── skills/
│   ├── init-project/
│   │   ├── SKILL.md
│   │   ├── agents/openai.yaml
│   │   └── references/stack-options.md
│   ├── issues2okf/
│   │   ├── SKILL.md
│   │   └── agents/openai.yaml
│   ├── scan-issues/
│   │   ├── SKILL.md
│   │   └── agents/openai.yaml
│   ├── xlsx2prd/
│   │   ├── SKILL.md
│   │   ├── agents/openai.yaml
│   │   ├── references/output-contract.md
│   │   └── scripts/
│   │       ├── extract_xlsx.py
│   │       └── validate_delivery.py
│   └── yolo-datasets-download/
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       ├── assets/download_ndjson_images.py
│       └── scripts/install_yolo_dataset_downloader.py
└── README.md
```

## Skill 一览

### 1. `init-project`

用途：初始化前端、后端或全栈项目脚手架。  
适用场景：用户要求创建、scaffold、bootstrap、initialize 一个新项目，并明确或暗示了技术栈、前后端目录、依赖安装、README、`.gitignore`、迁移或可运行 starter。

这个 skill 的特点：

- 默认按生产可用的项目骨架来做，不只生成空目录
- 全栈场景默认使用 `frontend/` 和 `backend/` 分离布局
- 要求补齐 `.env.example`、根目录 `.gitignore`、根目录 `README.md`
- 要求保留用户已有内容，不覆盖非空目录里的现有工作
- 要求生成一个最小可运行纵向切片，而不是只装依赖

默认栈定义在 `skills/init-project/references/stack-options.md`，当前默认包括：

- 前端：Next.js + React + TypeScript
- 样式：Tailwind CSS
- UI：Ant Design + shadcn/ui
- 后端：Python 3.13+ + FastAPI
- ORM：SQLAlchemy 2
- 迁移：Alembic
- 本地数据库：SQLite
- 生产数据库选项：PostgreSQL

### 2. `issues2okf`

用途：把 `.issues` 目录里的原始 Markdown 任务笔记，整理成统一的 TODO 文档格式。  
适用场景：仓库里已经在用 `.issues/*.md` 记需求、开发项、Bug，但格式不统一，想先标准化再继续自动化处理。

这个 skill 会：

- 扫描目标 `.issues` 目录
- 保留已经是标准格式的文件不动
- 为非标准文档补全 YAML frontmatter
- 统一关键字段：`status`、`type`、`title`、`description`、`links`、`tags`、`timestamp`
- 把原始正文保留下来，只做轻量排版清理
- 将文件名改成更可读的标题，必要时保留数字前缀

它的边界也很明确：

- 不凭空添加需求
- 不把已有标准文档重复改写
- 默认 `status` 为 `todo`，除非源文档已经清楚表达其他状态

### 3. `scan-issues`

用途：扫描 `.issues/**/*.md` 中标准化的待办文档，并逐项实现、验证、推进状态。  
适用场景：用户不是要“列出任务”，而是要代理真正开始做 `.issues` 里的开发工作。

这个 skill 的执行约束比较强：

- 必须先读仓库根目录 `AGENTS.md`
- 只处理带 YAML frontmatter、且 `status: todo` 的标准 issue 文档
- `type` 需要是 `dev`、`requirement`、`需求`、`bug`、`fixbug` 或本地等价标签
- 非标准 issue 不在这里修，应该先用 `issues2okf`
- 设计上要求“每个 issue 一个独立 subagent”
- 每做完一个 issue，都要做最小真实验证，并把状态推进到 `review` 或 `done`

如果当前执行环境没有 subagent 能力，这个 skill 按说明应当停止并报告，而不是悄悄降级成单 agent 直接做。

### 4. `xlsx2prd`

用途：把 Excel 需求/报价/字段清单工作簿转换为可追踪的 `PRD.md` 和页面模块化开发 TODO。  
适用场景：用户给出 `.xlsx` 文件，希望把表格里的需求、字段、模块、工作量、说明拆成产品文档和可开发任务。

这个 skill 的关键输出包括：

- `PRD.md`
- `todolist/README.md`
- 按页面或模块拆分的 `Epic*.md` / `Story*.md`
- 字段定义存在时的字段字典

核心原则：

- 不得静默编造业务决策
- 要把“源需求”“产品澄清”“实现建议”分开
- 每条功能都要落到稳定的 `FR-*` 需求编号
- 维护 `XLSX sheet/row -> FR-* -> Epic/Story -> TODO -> acceptance` 的追踪链

附带两个脚本：

- `skills/xlsx2prd/scripts/extract_xlsx.py`
  - 抽取工作簿内容为 `workbook.json` 和 `inventory.md`
  - 解析 sheet、单元格、合并单元格、公式和预览内容
- `skills/xlsx2prd/scripts/validate_delivery.py`
  - 校验输出目录结构
  - 检查 `PRD.md`、`todolist/README.md`
  - 检查 `FR-*` 覆盖、重复编号、Story 索引、Markdown 相对链接

输出规范写在 `skills/xlsx2prd/references/output-contract.md`。

### 5. `yolo-datasets-download`

用途：生成或更新一个 Python 脚本，把 Ultralytics 的 `.ndjson` 数据集导出转换成本地 YOLO 数据集目录。  
适用场景：用户手里有一个或多个 `.ndjson` 文件，希望落地成 `images/`、`labels/`、`dataset.yaml` 结构，并且要真实跑一次 smoke test。

这个 skill 的工作方式很直接：

- 运行 `skills/yolo-datasets-download/scripts/install_yolo_dataset_downloader.py`
- 将模板脚本安装到目标工作区根目录，默认文件名是 `download_ndjson_images.py`
- 创建或更新目标工作区根目录 `README.md`
- 要求对真实 `.ndjson` 执行一次带 `--limit` 的 smoke test

附带资源：

- `assets/download_ndjson_images.py`
  - 读取一个或多个 `.ndjson`
  - 下载图片
  - 从 `annotations.boxes` 生成 YOLO 标签
  - 保留 `train/val/test` 划分
  - 生成 `dataset.yaml`
- `scripts/install_yolo_dataset_downloader.py`
  - 把模板脚本复制到目标工作区
  - 给目标工作区根目录 `README.md` 追加使用说明

这个 skill 明确要求生成脚本尽量只用 Python 标准库。

## `agents/openai.yaml` 的作用

每个 skill 目录下都带有一个 `agents/openai.yaml`，用于声明该 skill 在界面中的展示信息，例如：

- `display_name`
- `short_description`
- `default_prompt`

这些文件不是业务逻辑本体，真正的执行规范还是各自目录下的 `SKILL.md`。

## 这个仓库的共性设计

从现有 5 个 skill 来看，这个仓库有几个一致特点：

- 都是任务导向，不是概念说明
- 都强调先读真实输入，再产出可验证结果
- 都偏向最小但可交付的结果，而不是大而全框架
- 多数 skill 都要求补齐验证步骤，而不是只生成文件
- 文档、脚本、引用规范分开放，结构比较克制

## 适合怎样继续扩展

如果后续继续往这个仓库里加 skill，当前结构已经给出一个很清楚的最小模板：

1. 一个 `SKILL.md`，写清楚触发场景、工作流、边界和验证要求
2. 一个 `agents/openai.yaml`，写展示名称和默认提示词
3. 只有在确实需要时，再补 `scripts/`、`assets/`、`references/`

这套结构的好处是简单，读者打开目录就能知道：

- 这个 skill 解决什么问题
- 什么时候该触发
- 需要哪些附带脚本或参考规范
- 交付结果如何验证
