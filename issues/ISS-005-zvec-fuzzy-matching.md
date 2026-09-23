# ISS-005 — 集成 zvec 模糊匹配并在初始化阶段自动安装

- 状态：resolved
- 创建时间：2026-09-23T10:20:39+00:00
- 来源：当前会话用户指令（见 [DEC-018](../decisions/DEC-018-integrate-zvec.md) 用户原话）
- 关联决策：[DEC-018](../decisions/DEC-018-integrate-zvec.md)

## 依据

用户要求工程集成 zvec（alibaba/zvec，进程内向量数据库）用于模糊匹配，并在工程初始化阶段（setup.sh / setup.ps1）自动拉取下载安装到对应路径。

## 影响

- `paper.py`：新增 `zvec_available()`、`fuzzy_rank()`、CLI 未知命令模糊建议；zvec 为可选依赖，装在 `vendor/`，不可用时降级标准库 difflib，行为不中断。
- `setup.sh` / `setup.ps1`：初始化流程新增 zvec 自动安装（已安装则跳过；失败仅告警不阻断工作区初始化）。
- `.gitignore` 新增 `vendor/`；README 更新联网安装说明。
- 附带修复：`setup.ps1` 此前为 UTF-8 无 BOM，Windows PowerShell 5.1 按 ANSI 读取导致解析失败（既有问题），已补 UTF-8 BOM。
- 附带修复：见 [ISS-002](ISS-002-path-normalization.md)（重复初始化路径规范化），本轮一并修复并通过验收。

## 验收条件

1. `bash setup.sh --no-skill <工作区>` 初始化时自动把 zvec 安装到脚本同级 `vendor/`；重复运行显示"已安装，跳过"。✅ 2026-09-23 实测
2. `setup.ps1` 同上（含真实安装分支与跳过分支）。✅ 2026-09-23 实测（修复 BOM 后）
3. zvec 可用时 `fuzzy_rank(..., backend='zvec')` 真正走 zvec 查询（有防静默降级测试）。✅
4. zvec 不可用时自动降级 difflib，CLI 建议仍可用。✅（Python 3.11 无 cp314 wheel 场景实测）
5. CLI 未知命令给出模糊建议（如 `inti` → 是否想输入 `init`），明显无关输入不建议。✅
6. 全量测试通过。✅ 45/45（py -3，Windows，2026-09-23）

## 已知边界

- zvec wheel 为 cp314 专属：当前 `vendor/` 仅 Python 3.14（`py -3`）可导入；其他解释器自动降级 difflib，不影响功能。
- 字符 bigram 对"中间删字"类短错字（如 `rn`→`run`）不敏感，此场景由 difflib 后端覆盖。
- macOS：本机无 mac 环境，setup.sh 在 mac 实机未实测。新增 zvec 代码块仅用 bash 3.2 兼容写法（`command -v`、`[ -f ]`、`if !`、`cygpath` 存在性守卫），且 zvec 官方提供 macOS ARM64/x86_64 wheel；ISS-001 已于同日修复并在**真 bash 3.2.0** 上完成四种流程验收（Linux 构建），macOS 实机仅余平台命令（python3/git）验证缺口，归 [ISS-004](ISS-004-validation.md)。

## 处理时间线

- 2026-09-23T10:20:39+00:00：登记；同轮完成实现、TDD 测试（8 个新增用例）、双脚本端到端验证与 BOM/ISS-002 附带修复，状态 resolved。
- 2026-09-23T10:45:00+00:00：应用户跨平台追问补充验证：WSL（Linux，Python 3.14）真实端到端——工作区初始化成功；无 pip 时告警降级分支 rc=0；ensurepip 后真安装分支成功，Linux wheel 导入与 zvec 查询实测通过（分数与 Windows 一致）；随后清理 Linux vendor 并恢复 Windows vendor 复验。macOS 仍为静态审查结论（见"已知边界"），ISS-001 保持 open。
