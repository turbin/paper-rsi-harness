# ISS-001 — setup.sh 与 macOS 系统 Bash 不兼容

- 状态：open
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
