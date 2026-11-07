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
| ontology/ | 工程本体 G2 模板资产（新版本 G2 模板级改造）：config 外置五表＋校验器/图生成器/init 脚本，新工程零代码跑通「登记主张→校验→生成图」 | 新增（DEC-019/ISS-006，2026-11-07） |

<!-- project-index:start -->
### 文件快照

| 文件 | 变更观察时间（UTC） | SHA-256 |
|---|---|---|
| .git | 2026-11-07T07:59:58+00:00 | `045fc6971259` |
| .gitignore | 2026-11-07T07:59:58+00:00 | `725b4eb78097` |
| AGENTS.md | 2026-11-07T07:59:58+00:00 | `8c2f1b0f4063` |
| DESIGN-DECISIONS.md | 2026-11-07T07:59:58+00:00 | `e077e82068a7` |
| README.md | 2026-11-07T07:59:58+00:00 | `074a375cb715` |
| VERIFICATION.md | 2026-11-07T07:59:58+00:00 | `13d468e5cf05` |
| mock_backend.py | 2026-11-07T07:59:58+00:00 | `f58475021f21` |
| paper.py | 2026-11-07T07:59:58+00:00 | `da1d29c2603e` |
| setup.ps1 | 2026-11-07T07:59:58+00:00 | `b2d436d48ffc` |
| setup.sh | 2026-11-07T07:59:58+00:00 | `69c6ee6962c6` |
| test_paper.py | 2026-11-07T07:59:58+00:00 | `1ac552cb0cb3` |

### 子目录

- [decisions](decisions/index.md)
- [issues](issues/index.md)
- [ontology](ontology/index.md)
- [scripts](scripts/index.md)
- [skills](skills/index.md)
- [user-stories](user-stories/index.md)

### 变更时间线
- 2026-11-07T09:20:14+00:00 · 修改 `issues/ISS-006-ontology-template-g2.md` · ISS-006 收尾：对抗审核 R2 共识后置 resolved，补登 ISS-007 问题表行
- 2026-11-07T09:10:17+00:00 · 修改 `issues/ISS-006-ontology-template-g2.md` · R1 审核修复：ISS-006 时间线更正与影响节表述、README known-diff 落盘说明与 governance 命名对照、登记 ISS-007
- 2026-11-07T09:10:17+00:00 · 首次纳入索引 `issues/ISS-007-update-indexes-git-gitlink.md` · R1 审核修复：ISS-006 时间线更正与影响节表述、README known-diff 落盘说明与 governance 命名对照、登记 ISS-007
- 2026-11-07T09:10:17+00:00 · 修改 `ontology/README.md` · R1 审核修复：ISS-006 时间线更正与影响节表述、README known-diff 落盘说明与 governance 命名对照、登记 ISS-007
- 2026-11-07T08:34:25+00:00 · 修改 `ontology/validate_claims.py` · 修复验证轮 P1：loc_grammar 非法正则兜底（error 而非 traceback）与页数锚文案 ISS-017 对齐
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `.git` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `.gitignore` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `AGENTS.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `DESIGN-DECISIONS.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `README.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `VERIFICATION.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `decisions/DEC-001-project-records.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `decisions/DEC-002-topic-clarification.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `decisions/DEC-003-writing-plan.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `decisions/DEC-004-chapter-figures-tables.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `decisions/DEC-005-formatting-guidelines.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `decisions/DEC-006-change-writing-topic.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `decisions/DEC-007-change-topic-refinements.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `decisions/DEC-008-output-version-format.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `decisions/DEC-009-workspace-issues-directory.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `decisions/DEC-010-writing-plan-structure.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `decisions/DEC-011-references-entry-structure.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `decisions/DEC-012-no-auto-web-search.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `decisions/DEC-013-formatting-guidelines-registry.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `decisions/DEC-014-guidelines-injection-to-tasks.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `decisions/DEC-015-figure-table-index.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `decisions/DEC-016-reset-topic-command.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `decisions/DEC-017-output-version-naming.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `decisions/DEC-018-integrate-zvec.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `decisions/DEC-019-ontology-template-g2.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `issues/ISS-001-macos-bash.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `issues/ISS-002-path-normalization.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `issues/ISS-003-spec-handoff.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `issues/ISS-004-validation.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `issues/ISS-005-zvec-fuzzy-matching.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `issues/ISS-006-ontology-template-g2.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `mock_backend.py` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `ontology/README.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `ontology/config_loader.py` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `ontology/gen_graph.py` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `ontology/init_ontology.py` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `ontology/templates/AGENTS-ontology-纪律条款.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `ontology/templates/claims.yaml` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `ontology/templates/documents.yaml` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `ontology/templates/ontology.config.yaml` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `ontology/test_ontology.py` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `ontology/validate_claims.py` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `paper.py` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `scripts/update_indexes.py` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `setup.ps1` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `setup.sh` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `skills/paper-spec-socratic/SKILL.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `test_paper.py` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `user-stories/US-001-topic-clarification.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `user-stories/US-002-writing-plan.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `user-stories/US-003-chapter-figures-tables.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `user-stories/US-004-formatting-guidelines.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `user-stories/US-005-change-writing-topic.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `user-stories/US-006-output-version-format.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-09-23T10:41:28+00:00 · 修改 `issues/ISS-001-macos-bash.md` · 修复 ISS-001 bash3.2 兼容并在真 bash 3.2.0 上完成验收
- 2026-09-23T10:41:28+00:00 · 修改 `issues/ISS-005-zvec-fuzzy-matching.md` · 修复 ISS-001 bash3.2 兼容并在真 bash 3.2.0 上完成验收
- 2026-09-23T10:41:28+00:00 · 修改 `setup.sh` · 修复 ISS-001 bash3.2 兼容并在真 bash 3.2.0 上完成验收
- 2026-09-23T10:31:43+00:00 · 修改 `issues/ISS-005-zvec-fuzzy-matching.md` · ISS-005 补充 Linux(WSL) 端到端验证与 macOS 跨平台边界说明
- 2026-09-23T10:21:54+00:00 · 首次纳入索引 `.DS_Store` · 集成 zvec 模糊匹配与初始化自动安装（ISS-005/DEC-018），修复 ISS-002 路径规范化与 setup.ps1 BOM
- 2026-09-23T10:21:54+00:00 · 修改 `.gitignore` · 集成 zvec 模糊匹配与初始化自动安装（ISS-005/DEC-018），修复 ISS-002 路径规范化与 setup.ps1 BOM
- 2026-09-23T10:21:54+00:00 · 修改 `README.md` · 集成 zvec 模糊匹配与初始化自动安装（ISS-005/DEC-018），修复 ISS-002 路径规范化与 setup.ps1 BOM
- 2026-09-23T10:21:54+00:00 · 首次纳入索引 `decisions/DEC-018-integrate-zvec.md` · 集成 zvec 模糊匹配与初始化自动安装（ISS-005/DEC-018），修复 ISS-002 路径规范化与 setup.ps1 BOM
- 2026-09-23T10:21:54+00:00 · 修改 `issues/ISS-002-path-normalization.md` · 集成 zvec 模糊匹配与初始化自动安装（ISS-005/DEC-018），修复 ISS-002 路径规范化与 setup.ps1 BOM
- 2026-09-23T10:21:54+00:00 · 首次纳入索引 `issues/ISS-005-zvec-fuzzy-matching.md` · 集成 zvec 模糊匹配与初始化自动安装（ISS-005/DEC-018），修复 ISS-002 路径规范化与 setup.ps1 BOM
- 2026-09-23T10:21:54+00:00 · 修改 `paper.py` · 集成 zvec 模糊匹配与初始化自动安装（ISS-005/DEC-018），修复 ISS-002 路径规范化与 setup.ps1 BOM
- 2026-09-23T10:21:54+00:00 · 修改 `setup.ps1` · 集成 zvec 模糊匹配与初始化自动安装（ISS-005/DEC-018），修复 ISS-002 路径规范化与 setup.ps1 BOM
- 2026-09-23T10:21:54+00:00 · 修改 `setup.sh` · 集成 zvec 模糊匹配与初始化自动安装（ISS-005/DEC-018），修复 ISS-002 路径规范化与 setup.ps1 BOM
- 2026-09-23T10:21:54+00:00 · 修改 `test_paper.py` · 集成 zvec 模糊匹配与初始化自动安装（ISS-005/DEC-018），修复 ISS-002 路径规范化与 setup.ps1 BOM
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
