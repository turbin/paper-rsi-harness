# ISS-002 — 重复初始化测试的路径规范化问题

- 状态：resolved
- 创建时间：2026-09-15T04:11:08+00:00
- 来源：本会话工程分析及本轮源码核对
- 关联决策：[DEC-001](../decisions/DEC-001-project-records.md)

## 依据

上一轮在本机执行 python3 -m unittest -v test_paper.py：19/20 通过，test_repeat_preserves_content 报目标位于其他 Git 仓库内。initialize() 比较 resolved 仓库路径与未 resolve 的 root，临时目录存在 /var 与 /private/var 别名。

## 影响

直接函数调用及测试会误判嵌套仓库。CLI main() 已 resolve 输入，不能据此断言普通 CLI 重复安装失败。

## 验收条件

统一路径比较；本机全部 20 项测试通过，同时保留真正嵌套仓库拒绝行为。

## 处理时间线

- 2026-09-15T04:11:08+00:00：登记待办；尚未修复或验收。
- 2026-09-23T10:20:39+00:00：`initialize()` 改为两侧路径统一 `resolve()` 后比较（Windows 8.3 短路径如 `ADMINI~1` 与 git 返回的规范长路径此前不相等）。全量测试通过，`test_nested_repository_rejected` 保留真正嵌套拒绝行为，验收条件满足，状态 resolved。修复随 ISS-005 集成轮完成。
