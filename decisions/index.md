# 工程设计决策索引

此目录记录源码工程的设计决策。保留原话与出处，明确区分用户确认和实现选择。

| 编号 | 决策 | 状态 | 来源 |
|---|---|---|---|
| [DEC-001](DEC-001-project-records.md) | 建立工程问题、设计决策与目录变更时间线 | confirmed | 本轮用户消息 |
| [DEC-002](DEC-002-topic-clarification.md) | 苏格拉底式主题澄清与遗留问题登记（US-001） | confirmed | 用户故事登记消息 |
| [DEC-003](DEC-003-writing-plan.md) | 论文计划包含主题背景、问题范围、大纲及文献贡献（US-002） | confirmed | 用户故事登记消息 |
| [DEC-004](DEC-004-chapter-figures-tables.md) | 章节表达方式、图表说明与编号索引（US-003） | confirmed | 用户故事登记消息 |
| [DEC-005](DEC-005-formatting-guidelines.md) | 确认论文规范文件并按规范排版（US-004） | confirmed | 用户故事登记消息 |
| [DEC-006](DEC-006-change-writing-topic.md) | 更改写作主题并清空工作区重新开始（US-005） | confirmed | 用户故事登记消息 |
| [DEC-007](DEC-007-change-topic-refinements.md) | 初始状态定义、图表编号来源、流程编排与分支命名规范（US-003、US-005） | confirmed | 用户故事澄清消息 |
| [DEC-008](DEC-008-output-version-format.md) | 论文输出版本格式规范 vX.Y-release / vX.Y-RC（US-006） | confirmed | 用户故事登记消息 |
| [DEC-009](DEC-009-workspace-issues-directory.md) | 论文工作区遗留问题目录确认为 notes/issues/（US-001） | confirmed | 本轮用户消息（用户故事差距分析） |
| [DEC-010](DEC-010-writing-plan-structure.md) | 编写计划落盘 writing/plan/ 及固定四节结构（US-002） | confirmed | 本轮用户消息（用户故事差距分析） |
| [DEC-011](DEC-011-references-entry-structure.md) | 文献条目文件结构与核验状态分级（US-002） | confirmed | 本轮用户消息（用户故事差距分析） |
| [DEC-012](DEC-012-no-auto-web-search.md) | v0.1 不做自动联网检索，agent_retrieved 降级整理用户提供文本（US-002） | confirmed | 本轮用户消息（用户故事差距分析） |
| [DEC-013](DEC-013-formatting-guidelines-registry.md) | workspace.json 新增 formatting_guidelines 登记与 materials/guidelines/ 目录（US-004） | confirmed | 本轮用户消息（用户故事差距分析） |
| [DEC-014](DEC-014-guidelines-injection-to-tasks.md) | 规范向 PM 与 writer/reviewer 任务的三层传递机制（US-004） | confirmed | 本轮用户消息（用户故事差距分析） |
| [DEC-015](DEC-015-figure-table-index.md) | 图表索引文件 figure-table-index.md 与编号规则来源（US-003） | confirmed | 本轮用户消息（用户故事差距分析） |
| [DEC-016](DEC-016-reset-topic-command.md) | reset-topic 子命令与两阶段门禁（US-005） | confirmed | 本轮用户消息（用户故事差距分析） |
| [DEC-017](DEC-017-output-version-naming.md) | 输出版本目录命名规则 vX.Y-release / vX.Y-RC（US-006） | confirmed | 本轮用户消息（用户故事差距分析） |

前期 D01–D04 原话与决策保留在 [DESIGN-DECISIONS.md](../DESIGN-DECISIONS.md)，作为历史依据，未在本轮重新确认。

<!-- project-index:start -->
### 文件快照

| 文件 | 变更观察时间（UTC） | SHA-256 |
|---|---|---|
| DEC-001-project-records.md | 2026-09-15T04:11:09+00:00 | `fab701389d3f` |
| DEC-002-topic-clarification.md | 2026-09-15T05:59:23+00:00 | `559b0d361f72` |
| DEC-003-writing-plan.md | 2026-09-15T06:13:26+00:00 | `aa4cdf00e6ce` |
| DEC-004-chapter-figures-tables.md | 2026-09-15T06:15:35+00:00 | `afd945f585c3` |
| DEC-005-formatting-guidelines.md | 2026-09-15T06:18:40+00:00 | `fbae6a25dab8` |
| DEC-006-change-writing-topic.md | 2026-09-15T06:57:23+00:00 | `1aa96513aadb` |
| DEC-007-change-topic-refinements.md | 2026-09-15T07:17:45+00:00 | `d1045323386d` |
| DEC-008-output-version-format.md | 2026-09-15T07:17:45+00:00 | `481862280f03` |
| DEC-009-workspace-issues-directory.md | 2026-09-15T09:50:30+00:00 | `1efd35435c7b` |
| DEC-010-writing-plan-structure.md | 2026-09-15T09:50:30+00:00 | `6c0947b32302` |
| DEC-011-references-entry-structure.md | 2026-09-15T09:50:30+00:00 | `01404d480415` |
| DEC-012-no-auto-web-search.md | 2026-09-15T09:50:30+00:00 | `766a3f7bde32` |
| DEC-013-formatting-guidelines-registry.md | 2026-09-15T09:50:30+00:00 | `2f49f9ae90ff` |
| DEC-014-guidelines-injection-to-tasks.md | 2026-09-15T09:50:30+00:00 | `4ccb44e5e945` |
| DEC-015-figure-table-index.md | 2026-09-15T09:50:30+00:00 | `df6ba7fd725c` |
| DEC-016-reset-topic-command.md | 2026-09-15T09:50:30+00:00 | `9c61885e672a` |
| DEC-017-output-version-naming.md | 2026-09-15T09:50:30+00:00 | `6872f2f71e02` |
| DEC-018-integrate-zvec.md | 2026-09-23T10:21:54+00:00 | `2bfaf5eeeb1e` |

### 子目录



### 变更时间线
- 2026-09-23T10:21:54+00:00 · 首次纳入索引 `decisions/DEC-018-integrate-zvec.md` · 集成 zvec 模糊匹配与初始化自动安装（ISS-005/DEC-018），修复 ISS-002 路径规范化与 setup.ps1 BOM
- 2026-09-15T09:50:30+00:00 · 修改 `decisions/DEC-009-workspace-issues-directory.md` · 用户确认 DEC-009~DEC-017 转为 confirmed
- 2026-09-15T09:50:30+00:00 · 修改 `decisions/DEC-010-writing-plan-structure.md` · 用户确认 DEC-009~DEC-017 转为 confirmed
- 2026-09-15T09:50:30+00:00 · 修改 `decisions/DEC-011-references-entry-structure.md` · 用户确认 DEC-009~DEC-017 转为 confirmed
- 2026-09-15T09:50:30+00:00 · 修改 `decisions/DEC-012-no-auto-web-search.md` · 用户确认 DEC-009~DEC-017 转为 confirmed
- 2026-09-15T09:50:30+00:00 · 修改 `decisions/DEC-013-formatting-guidelines-registry.md` · 用户确认 DEC-009~DEC-017 转为 confirmed
- 2026-09-15T09:50:30+00:00 · 修改 `decisions/DEC-014-guidelines-injection-to-tasks.md` · 用户确认 DEC-009~DEC-017 转为 confirmed
- 2026-09-15T09:50:30+00:00 · 修改 `decisions/DEC-015-figure-table-index.md` · 用户确认 DEC-009~DEC-017 转为 confirmed
- 2026-09-15T09:50:30+00:00 · 修改 `decisions/DEC-016-reset-topic-command.md` · 用户确认 DEC-009~DEC-017 转为 confirmed
- 2026-09-15T09:50:30+00:00 · 修改 `decisions/DEC-017-output-version-naming.md` · 用户确认 DEC-009~DEC-017 转为 confirmed
- 2026-09-15T09:24:59+00:00 · 修改 `decisions/DEC-016-reset-topic-command.md` · 修复 skill/README/DEC 文档与审查发现的一致性问题
- 2026-09-15T08:56:12+00:00 · 首次纳入索引 `decisions/DEC-009-workspace-issues-directory.md` · 登记 DEC-009~DEC-017：US-001~US-006 差距分析产生的新设计决策
- 2026-09-15T08:56:12+00:00 · 首次纳入索引 `decisions/DEC-010-writing-plan-structure.md` · 登记 DEC-009~DEC-017：US-001~US-006 差距分析产生的新设计决策
- 2026-09-15T08:56:12+00:00 · 首次纳入索引 `decisions/DEC-011-references-entry-structure.md` · 登记 DEC-009~DEC-017：US-001~US-006 差距分析产生的新设计决策
- 2026-09-15T08:56:12+00:00 · 首次纳入索引 `decisions/DEC-012-no-auto-web-search.md` · 登记 DEC-009~DEC-017：US-001~US-006 差距分析产生的新设计决策
- 2026-09-15T08:56:12+00:00 · 首次纳入索引 `decisions/DEC-013-formatting-guidelines-registry.md` · 登记 DEC-009~DEC-017：US-001~US-006 差距分析产生的新设计决策
- 2026-09-15T08:56:12+00:00 · 首次纳入索引 `decisions/DEC-014-guidelines-injection-to-tasks.md` · 登记 DEC-009~DEC-017：US-001~US-006 差距分析产生的新设计决策
- 2026-09-15T08:56:12+00:00 · 首次纳入索引 `decisions/DEC-015-figure-table-index.md` · 登记 DEC-009~DEC-017：US-001~US-006 差距分析产生的新设计决策
- 2026-09-15T08:56:12+00:00 · 首次纳入索引 `decisions/DEC-016-reset-topic-command.md` · 登记 DEC-009~DEC-017：US-001~US-006 差距分析产生的新设计决策
- 2026-09-15T08:56:12+00:00 · 首次纳入索引 `decisions/DEC-017-output-version-naming.md` · 登记 DEC-009~DEC-017：US-001~US-006 差距分析产生的新设计决策
- 2026-09-15T07:17:45+00:00 · 首次纳入索引 `decisions/DEC-007-change-topic-refinements.md` · 登记 US-006 与 DEC-007/DEC-008：初始状态定义、图表编号来源、版本格式规范与分支命名
- 2026-09-15T07:17:45+00:00 · 首次纳入索引 `decisions/DEC-008-output-version-format.md` · 登记 US-006 与 DEC-007/DEC-008：初始状态定义、图表编号来源、版本格式规范与分支命名
- 2026-09-15T06:57:23+00:00 · 首次纳入索引 `decisions/DEC-006-change-writing-topic.md` · 登记 US-005 与 DEC-006：更改写作主题并清空工作区重新开始写作
- 2026-09-15T06:18:40+00:00 · 首次纳入索引 `decisions/DEC-005-formatting-guidelines.md` · 登记 US-004 与 DEC-005：确认论文规范文件并按规范排版
- 2026-09-15T06:15:35+00:00 · 首次纳入索引 `decisions/DEC-004-chapter-figures-tables.md` · 登记 US-003 与 DEC-004：章节表达方式、图表说明及编号索引
- 2026-09-15T06:13:26+00:00 · 首次纳入索引 `decisions/DEC-003-writing-plan.md` · 登记 US-002 与 DEC-003：主题梳理后生成论文计划及文献贡献列表
- 2026-09-15T05:59:23+00:00 · 首次纳入索引 `decisions/DEC-002-topic-clarification.md` · 登记 US-001 用户故事与 DEC-002：主题澄清及遗留问题登记
- 2026-09-15T04:11:09+00:00 · 首次纳入索引 `decisions/DEC-001-project-records.md` · 依据 DEC-001 初始化源码工程管理，登记四项已有问题，建立首次文件基线
<!-- project-index:end -->
