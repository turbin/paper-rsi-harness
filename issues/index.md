# 工程问题索引

问题状态：open / in_progress / blocked / resolved。以下问题来自工程分析，属于待核验或待处理事项，不代表用户已批准全部实施。

| 编号 | 问题 | 状态 |
|---|---|---|
| [ISS-001](ISS-001-macos-bash.md) | setup.sh 与 macOS 系统 Bash 不兼容 | open |
| [ISS-002](ISS-002-path-normalization.md) | 重复初始化测试的路径规范化问题 | open |
| [ISS-003](ISS-003-spec-handoff.md) | Skill 与 PM 的 spec 交接未明确 | open |
| [ISS-004](ISS-004-validation.md) | 跨平台、真实后端与质量验证未完成 | open |
| [ISS-006](ISS-006-ontology-template-g2.md) | ontology G2 模板资产实施（config 化校验器/图生成器/init 脚本） | resolved |
| [ISS-007](ISS-007-update-indexes-git-gitlink.md) | update_indexes.py 在 worktree 场景把 .git gitlink 文件纳入索引 | open |

<!-- project-index:start -->
### 文件快照

| 文件 | 变更观察时间（UTC） | SHA-256 |
|---|---|---|
| ISS-001-macos-bash.md | 2026-11-07T07:59:58+00:00 | `c5d57037e1f3` |
| ISS-002-path-normalization.md | 2026-11-07T07:59:58+00:00 | `55d6d7babfdb` |
| ISS-003-spec-handoff.md | 2026-11-07T07:59:58+00:00 | `65189af8deec` |
| ISS-004-validation.md | 2026-11-07T07:59:58+00:00 | `fa011807ab90` |
| ISS-005-zvec-fuzzy-matching.md | 2026-11-07T07:59:58+00:00 | `5e85e97f5e2c` |
| ISS-006-ontology-template-g2.md | 2026-11-07T09:20:14+00:00 | `5a25d22435a0` |
| ISS-007-update-indexes-git-gitlink.md | 2026-11-07T09:10:17+00:00 | `55e0fd04e897` |

### 子目录



### 变更时间线
- 2026-11-07T09:20:14+00:00 · 修改 `issues/ISS-006-ontology-template-g2.md` · ISS-006 收尾：对抗审核 R2 共识后置 resolved，补登 ISS-007 问题表行
- 2026-11-07T09:10:17+00:00 · 修改 `issues/ISS-006-ontology-template-g2.md` · R1 审核修复：ISS-006 时间线更正与影响节表述、README known-diff 落盘说明与 governance 命名对照、登记 ISS-007
- 2026-11-07T09:10:17+00:00 · 首次纳入索引 `issues/ISS-007-update-indexes-git-gitlink.md` · R1 审核修复：ISS-006 时间线更正与影响节表述、README known-diff 落盘说明与 governance 命名对照、登记 ISS-007
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `issues/ISS-001-macos-bash.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `issues/ISS-002-path-normalization.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `issues/ISS-003-spec-handoff.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `issues/ISS-004-validation.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `issues/ISS-005-zvec-fuzzy-matching.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `issues/ISS-006-ontology-template-g2.md` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-09-23T10:41:28+00:00 · 修改 `issues/ISS-001-macos-bash.md` · 修复 ISS-001 bash3.2 兼容并在真 bash 3.2.0 上完成验收
- 2026-09-23T10:41:28+00:00 · 修改 `issues/ISS-005-zvec-fuzzy-matching.md` · 修复 ISS-001 bash3.2 兼容并在真 bash 3.2.0 上完成验收
- 2026-09-23T10:31:43+00:00 · 修改 `issues/ISS-005-zvec-fuzzy-matching.md` · ISS-005 补充 Linux(WSL) 端到端验证与 macOS 跨平台边界说明
- 2026-09-23T10:21:54+00:00 · 修改 `issues/ISS-002-path-normalization.md` · 集成 zvec 模糊匹配与初始化自动安装（ISS-005/DEC-018），修复 ISS-002 路径规范化与 setup.ps1 BOM
- 2026-09-23T10:21:54+00:00 · 首次纳入索引 `issues/ISS-005-zvec-fuzzy-matching.md` · 集成 zvec 模糊匹配与初始化自动安装（ISS-005/DEC-018），修复 ISS-002 路径规范化与 setup.ps1 BOM
- 2026-09-15T04:11:09+00:00 · 首次纳入索引 `issues/ISS-001-macos-bash.md` · 依据 DEC-001 初始化源码工程管理，登记四项已有问题，建立首次文件基线
- 2026-09-15T04:11:09+00:00 · 首次纳入索引 `issues/ISS-002-path-normalization.md` · 依据 DEC-001 初始化源码工程管理，登记四项已有问题，建立首次文件基线
- 2026-09-15T04:11:09+00:00 · 首次纳入索引 `issues/ISS-003-spec-handoff.md` · 依据 DEC-001 初始化源码工程管理，登记四项已有问题，建立首次文件基线
- 2026-09-15T04:11:09+00:00 · 首次纳入索引 `issues/ISS-004-validation.md` · 依据 DEC-001 初始化源码工程管理，登记四项已有问题，建立首次文件基线
<!-- project-index:end -->
