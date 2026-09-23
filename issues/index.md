# 工程问题索引

问题状态：open / in_progress / blocked / resolved。以下问题来自工程分析，属于待核验或待处理事项，不代表用户已批准全部实施。

| 编号 | 问题 | 状态 |
|---|---|---|
| [ISS-001](ISS-001-macos-bash.md) | setup.sh 与 macOS 系统 Bash 不兼容 | open |
| [ISS-002](ISS-002-path-normalization.md) | 重复初始化测试的路径规范化问题 | open |
| [ISS-003](ISS-003-spec-handoff.md) | Skill 与 PM 的 spec 交接未明确 | open |
| [ISS-004](ISS-004-validation.md) | 跨平台、真实后端与质量验证未完成 | open |

<!-- project-index:start -->
### 文件快照

| 文件 | 变更观察时间（UTC） | SHA-256 |
|---|---|---|
| ISS-001-macos-bash.md | 2026-09-23T10:41:28+00:00 | `c5d57037e1f3` |
| ISS-002-path-normalization.md | 2026-09-23T10:21:54+00:00 | `55d6d7babfdb` |
| ISS-003-spec-handoff.md | 2026-09-15T04:11:09+00:00 | `65189af8deec` |
| ISS-004-validation.md | 2026-09-15T04:11:09+00:00 | `fa011807ab90` |
| ISS-005-zvec-fuzzy-matching.md | 2026-09-23T10:41:28+00:00 | `5e85e97f5e2c` |

### 子目录



### 变更时间线
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
