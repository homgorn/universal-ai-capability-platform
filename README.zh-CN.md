# 通用 AI 能力平台

通用 AI 能力平台是一个与供应商无关的注册中心、评估器、路由器和执行运行时，面向异构 AI 资源——Hugging Face Spaces 与 Models、推理服务商、REST/OpenAPI 服务、MCP 工具、A2A 智能体以及内部 API。其规范单元是 **Capability + Contract（能力 + 契约）**，而不是 iframe。平台发现能力、校验机器可读契约、执行策略、两阶段路由、持久化执行，并生成面向大语言模型的知识维基。

🌐 **语言 / Language:** [简体中文](README.zh-CN.md) · [English](README.md) · [Русский](README.ru.md) · [Español](README.es.md) · [Deutsch](README.de.md)

## 关键事实

| 事实 | 值 |
|------|-----|
| 规范单元 | Capability + Contract |
| 核心流程 | Discovery → Registry → Contract → Evaluation → Policy → Routing → Execution → Composition → Deployment |
| 真实数据源 | PostgreSQL（本地开发用 SQLite） |
| 知识图谱 | 派生三元组投影（`kg_entity` + `kg_triple`），ADR-002 |
| LLM 接口 | `llms.txt`、`llms-full.txt`、12 个主题页 |
| 领域实体 | 18 张规范表 |
| 错误分类 | 15 个标准化错误码 |
| 健康检查 | `python scripts/health.py`（ruff + mypy + pytest） |
| 测试 | 56 项通过 |
| 许可证 | MIT |

## 差异化设计

- **Tool ≠ Capability。** 工具是可执行实现，能力是稳定的语义函数；多个工具可满足同一能力。
- **Resource ≠ Interface。** Model 可暴露 REST/SDK/MCP；Space 可暴露 UI 与 Gradio API。
- **两阶段路由。** Capability Router（语义匹配）绝不与 Provider Router（运行时端点）合并。
- **已发现 ≠ 可执行。** 外部调用前必须完成 T0–T4 信任升级与策略决策。
- **契约不可变。** 历史版本只追加；变更检测会创建新版本并阻止不兼容路由。
- **证据优先。** 每条声明标记为 MEASURED / REPORTED（URL + 日期）/ INFERRED；未知项列为 VERIFY，绝不编造。
- **浏览器不含密钥。** 服务商凭据永不下发客户端，只使用作用域会话令牌。

## 快速开始

```bash
cd backend
python -m pip install -e ".[dev]"

# 幂等初始化：表、图谱、维基
export PYTHONPATH=src          # Windows: $env:PYTHONPATH='src'
python -m uaicp.seed

# 完整校验
python scripts/health.py

# 启动 API
uvicorn uaicp.api.main:app --reload
```

本地 PostgreSQL：`docker compose up -d db`，然后设置 `DATABASE_URL`（见 `backend/.env.example`）。

## 仓库结构

```text
universal-ai-capability-platform-specs-v1/  原始规范包
.specify/                                    Spec Kit 章程、模板、脚本
specs/001-knowledge-foundation/              维基 + 存储 + 知识图谱
specs/002-contract-validation/               端口、兼容性、错误分类、CLI
specs/003-execution-gateway/                 状态机、幂等、重试、回退
backend/src/uaicp/                           实现代码
wiki/                                        生成的 LLM 知识库
```

## 文档

- [LLM 知识库索引](wiki/llms.txt)
- [完整知识库](wiki/llms-full.txt)
- [技术规范](universal-ai-capability-platform-specs-v1/universal-ai-capability-platform-specs-v1/docs/SPECS.md)
- [项目章程](.specify/memory/constitution.md)

## 方法论

遵循 [GitHub Spec Kit](https://github.com/github/spec-kit)：constitution → specify → plan → tasks → analyze → implement。每个功能都有规范、计划、任务和测试。

## 许可证

MIT — 见 [LICENSE](LICENSE)。