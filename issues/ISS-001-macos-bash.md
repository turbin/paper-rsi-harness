# ISS-001 — setup.sh 与 macOS 系统 Bash 不兼容

- 状态：resolved
- 创建时间：2026-09-15T04:11:08+00:00
- 来源：本会话工程分析及本轮源码核对
- 关联决策：[DEC-001](../decisions/DEC-001-project-records.md)

## 依据

此前 install-skill.sh 在 /bin/bash 3.2 执行 --list 时报 kimi: unbound variable。当前入口已合并为 setup.sh，代码仍使用 declare -A 关联数组，待对当前入口复验。

## 影响

macOS 默认安装路径可能在执行参数处理前失败，包括 --no-skill。

## 验收条件

改用 Bash 3.2 支持的写法或提供明确可用的运行方式；验证 --list、--no-skill、指定 agent 及中文/空格路径。

## 处理时间线

- 2026-09-15T04:11:08+00:00：登记待办；尚未修复或验收。
- 2026-09-23T11:10:00+00:00：`setup.sh` 重写为 Bash 3.2 兼容写法（删除 `declare -A`/`${!DIRS[@]}`/数组切片，改为 case 函数 `agent_cmd`/`agent_dir` + 空格字符串 `detected`），随 ISS-001 一并完成。在 WSL 从 GNU 源码构建的**真 bash 3.2.0(3)-release** 上验收全部通过：`--list`（原崩溃点）rc=0、`--no-skill` 中文+空格路径 rc=0、`--agent kimi` rc=0、未知 agent rc=2 明确报错、未知参数 rc=2；Git Bash（bash 5）同步回归通过。macOS 实机未测（本机无 mac），但阻塞点为 bash 语法本身，bash 3.2 实机已证；平台相关命令（python3/git 存在性）仍属 ISS-004 跨平台验证范围。状态 resolved。
