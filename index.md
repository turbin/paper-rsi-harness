# 安装工具包索引

记录日期：2026-09-15。工程名称：paper-rsi-harness（原 mba-paper）。此处是交付清单；安装后的每个内容目录将由程序生成带 UTC 时间戳、哈希和变更历史的 index.md。

| 文件 | 用途 | 本版变更 |
|---|---|---|
| README.md | 安装、使用、架构图、边界与官方来源 | 新增 |
| DESIGN-DECISIONS.md | 当前对话的原话依据与设计决议 | 新增 |
| paper.py | 跨平台目录、索引、决议与 PM 协调器 | 新增 |
| setup.sh | 一体化安装入口（工作区 + skill），macOS/Linux | 新增 |
| setup.ps1 | 一体化安装入口（工作区 + skill），Windows | 新增 |
| skills/paper-spec-socratic/SKILL.md | 苏格拉底式论文 spec 澄清 skill | 新增 |
| test_paper.py | 自动化验证 | 新增 |
| mock_backend.py | 离线子进程测试夹具，非真实 AI | 新增 |
| VERIFICATION.md | 20项测试结果与未验证范围 | 新增 |

<!-- project-index:start -->
### 文件快照

| 文件 | 变更观察时间（UTC） | SHA-256 |
|---|---|---|
| .gitignore | 2026-09-15T04:11:09+00:00 | `b75c32e9ec84` |
| AGENTS.md | 2026-09-15T04:11:09+00:00 | `8c2f1b0f4063` |
| DESIGN-DECISIONS.md | 2026-09-15T04:11:09+00:00 | `e077e82068a7` |
| README.md | 2026-09-15T09:39:40+00:00 | `362dd8c8cf91` |
| VERIFICATION.md | 2026-09-15T04:11:09+00:00 | `13d468e5cf05` |
| mock_backend.py | 2026-09-15T04:11:09+00:00 | `f58475021f21` |
| paper.py | 2026-09-15T09:31:34+00:00 | `7cc16b996e63` |
| setup.ps1 | 2026-09-15T04:11:09+00:00 | `10cac29cf5b5` |
| setup.sh | 2026-09-15T04:11:09+00:00 | `2ded4eb6bac5` |
| test_paper.py | 2026-09-15T09:31:34+00:00 | `1a4509608e5f` |

### 子目录

- [decisions](decisions/index.md)
- [issues](issues/index.md)
- [scripts](scripts/index.md)
- [skills](skills/index.md)
- [user-stories](user-stories/index.md)

### 变更时间线
- 2026-09-15T09:50:30+00:00 · 修改 `decisions/DEC-009-workspace-issues-directory.md` · 用户确认 DEC-009~DEC-017 转为 confirmed
- 2026-09-15T09:50:30+00:00 · 修改 `decisions/DEC-010-writing-plan-structure.md` · 用户确认 DEC-009~DEC-017 转为 confirmed
- 2026-09-15T09:50:30+00:00 · 修改 `decisions/DEC-011-references-entry-structure.md` · 用户确认 DEC-009~DEC-017 转为 confirmed
- 2026-09-15T09:50:30+00:00 · 修改 `decisions/DEC-012-no-auto-web-search.md` · 用户确认 DEC-009~DEC-017 转为 confirmed
- 2026-09-15T09:50:30+00:00 · 修改 `decisions/DEC-013-formatting-guidelines-registry.md` · 用户确认 DEC-009~DEC-017 转为 confirmed
- 2026-09-15T09:50:30+00:00 · 修改 `decisions/DEC-014-guidelines-injection-to-tasks.md` · 用户确认 DEC-009~DEC-017 转为 confirmed
- 2026-09-15T09:50:30+00:00 · 修改 `decisions/DEC-015-figure-table-index.md` · 用户确认 DEC-009~DEC-017 转为 confirmed
- 2026-09-15T09:50:30+00:00 · 修改 `decisions/DEC-016-reset-topic-command.md` · 用户确认 DEC-009~DEC-017 转为 confirmed
- 2026-09-15T09:50:30+00:00 · 修改 `decisions/DEC-017-output-version-naming.md` · 用户确认 DEC-009~DEC-017 转为 confirmed
- 2026-09-15T09:39:40+00:00 · 修改 `README.md` · 修复 --guideline 文档示例并完成功能实现与两轮审阅收尾
- 2026-09-15T09:39:40+00:00 · 修改 `skills/paper-spec-socratic/SKILL.md` · 修复 --guideline 文档示例并完成功能实现与两轮审阅收尾
- 2026-09-15T09:31:34+00:00 · 修改 `paper.py` · 修复 reset-topic 清空边界、登记链路与健壮性审查问题
- 2026-09-15T09:31:34+00:00 · 修改 `test_paper.py` · 修复 reset-topic 清空边界、登记链路与健壮性审查问题
- 2026-09-15T09:24:59+00:00 · 修改 `README.md` · 修复 skill/README/DEC 文档与审查发现的一致性问题
- 2026-09-15T09:24:59+00:00 · 修改 `decisions/DEC-016-reset-topic-command.md` · 修复 skill/README/DEC 文档与审查发现的一致性问题
- 2026-09-15T09:24:59+00:00 · 修改 `skills/paper-spec-socratic/SKILL.md` · 修复 skill/README/DEC 文档与审查发现的一致性问题
- 2026-09-15T09:12:53+00:00 · 修改 `paper.py` · 按 DEC-009~DEC-017 实现 paper.py 新功能
- 2026-09-15T09:12:53+00:00 · 修改 `test_paper.py` · 按 DEC-009~DEC-017 实现 paper.py 新功能
- 2026-09-15T09:03:54+00:00 · 修改 `README.md` · 按 DEC-009~DEC-017 更新 paper-spec-socratic skill 与 README
- 2026-09-15T09:03:54+00:00 · 修改 `paper.py` · 按 DEC-009~DEC-017 更新 paper-spec-socratic skill 与 README
- 2026-09-15T09:03:54+00:00 · 修改 `skills/paper-spec-socratic/SKILL.md` · 按 DEC-009~DEC-017 更新 paper-spec-socratic skill 与 README
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
- 2026-09-15T07:17:45+00:00 · 修改 `user-stories/US-003-chapter-figures-tables.md` · 登记 US-006 与 DEC-007/DEC-008：初始状态定义、图表编号来源、版本格式规范与分支命名
- 2026-09-15T07:17:45+00:00 · 修改 `user-stories/US-005-change-writing-topic.md` · 登记 US-006 与 DEC-007/DEC-008：初始状态定义、图表编号来源、版本格式规范与分支命名
- 2026-09-15T07:17:45+00:00 · 首次纳入索引 `user-stories/US-006-output-version-format.md` · 登记 US-006 与 DEC-007/DEC-008：初始状态定义、图表编号来源、版本格式规范与分支命名
- 2026-09-15T06:57:23+00:00 · 首次纳入索引 `decisions/DEC-006-change-writing-topic.md` · 登记 US-005 与 DEC-006：更改写作主题并清空工作区重新开始写作
- 2026-09-15T06:57:23+00:00 · 首次纳入索引 `user-stories/US-005-change-writing-topic.md` · 登记 US-005 与 DEC-006：更改写作主题并清空工作区重新开始写作
- 2026-09-15T06:18:40+00:00 · 首次纳入索引 `decisions/DEC-005-formatting-guidelines.md` · 登记 US-004 与 DEC-005：确认论文规范文件并按规范排版
- 2026-09-15T06:18:40+00:00 · 首次纳入索引 `user-stories/US-004-formatting-guidelines.md` · 登记 US-004 与 DEC-005：确认论文规范文件并按规范排版
- 2026-09-15T06:15:35+00:00 · 首次纳入索引 `decisions/DEC-004-chapter-figures-tables.md` · 登记 US-003 与 DEC-004：章节表达方式、图表说明及编号索引
- 2026-09-15T06:15:35+00:00 · 首次纳入索引 `user-stories/US-003-chapter-figures-tables.md` · 登记 US-003 与 DEC-004：章节表达方式、图表说明及编号索引
- 2026-09-15T06:13:26+00:00 · 首次纳入索引 `decisions/DEC-003-writing-plan.md` · 登记 US-002 与 DEC-003：主题梳理后生成论文计划及文献贡献列表
- 2026-09-15T06:13:26+00:00 · 首次纳入索引 `user-stories/US-002-writing-plan.md` · 登记 US-002 与 DEC-003：主题梳理后生成论文计划及文献贡献列表
- 2026-09-15T05:59:23+00:00 · 首次纳入索引 `decisions/DEC-002-topic-clarification.md` · 登记 US-001 用户故事与 DEC-002：主题澄清及遗留问题登记
- 2026-09-15T05:59:23+00:00 · 首次纳入索引 `user-stories/US-001-topic-clarification.md` · 登记 US-001 用户故事与 DEC-002：主题澄清及遗留问题登记
- 2026-09-15T04:11:09+00:00 · 首次纳入索引 `.gitignore` · 依据 DEC-001 初始化源码工程管理，登记四项已有问题，建立首次文件基线
- 2026-09-15T04:11:09+00:00 · 首次纳入索引 `AGENTS.md` · 依据 DEC-001 初始化源码工程管理，登记四项已有问题，建立首次文件基线
- 2026-09-15T04:11:09+00:00 · 首次纳入索引 `DESIGN-DECISIONS.md` · 依据 DEC-001 初始化源码工程管理，登记四项已有问题，建立首次文件基线
- 2026-09-15T04:11:09+00:00 · 首次纳入索引 `README.md` · 依据 DEC-001 初始化源码工程管理，登记四项已有问题，建立首次文件基线
- 2026-09-15T04:11:09+00:00 · 首次纳入索引 `VERIFICATION.md` · 依据 DEC-001 初始化源码工程管理，登记四项已有问题，建立首次文件基线
- 2026-09-15T04:11:09+00:00 · 首次纳入索引 `decisions/DEC-001-project-records.md` · 依据 DEC-001 初始化源码工程管理，登记四项已有问题，建立首次文件基线
- 2026-09-15T04:11:09+00:00 · 首次纳入索引 `issues/ISS-001-macos-bash.md` · 依据 DEC-001 初始化源码工程管理，登记四项已有问题，建立首次文件基线
- 2026-09-15T04:11:09+00:00 · 首次纳入索引 `issues/ISS-002-path-normalization.md` · 依据 DEC-001 初始化源码工程管理，登记四项已有问题，建立首次文件基线
- 2026-09-15T04:11:09+00:00 · 首次纳入索引 `issues/ISS-003-spec-handoff.md` · 依据 DEC-001 初始化源码工程管理，登记四项已有问题，建立首次文件基线
- 2026-09-15T04:11:09+00:00 · 首次纳入索引 `issues/ISS-004-validation.md` · 依据 DEC-001 初始化源码工程管理，登记四项已有问题，建立首次文件基线
- 2026-09-15T04:11:09+00:00 · 首次纳入索引 `mock_backend.py` · 依据 DEC-001 初始化源码工程管理，登记四项已有问题，建立首次文件基线
- 2026-09-15T04:11:09+00:00 · 首次纳入索引 `paper.py` · 依据 DEC-001 初始化源码工程管理，登记四项已有问题，建立首次文件基线
- 2026-09-15T04:11:09+00:00 · 首次纳入索引 `scripts/update_indexes.py` · 依据 DEC-001 初始化源码工程管理，登记四项已有问题，建立首次文件基线
- 2026-09-15T04:11:09+00:00 · 首次纳入索引 `setup.ps1` · 依据 DEC-001 初始化源码工程管理，登记四项已有问题，建立首次文件基线
- 2026-09-15T04:11:09+00:00 · 首次纳入索引 `setup.sh` · 依据 DEC-001 初始化源码工程管理，登记四项已有问题，建立首次文件基线
- 2026-09-15T04:11:09+00:00 · 首次纳入索引 `skills/paper-spec-socratic/SKILL.md` · 依据 DEC-001 初始化源码工程管理，登记四项已有问题，建立首次文件基线
- 2026-09-15T04:11:09+00:00 · 首次纳入索引 `test_paper.py` · 依据 DEC-001 初始化源码工程管理，登记四项已有问题，建立首次文件基线
<!-- project-index:end -->
