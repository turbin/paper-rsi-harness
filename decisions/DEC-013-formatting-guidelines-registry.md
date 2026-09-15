# DEC-013 — 论文规范结构化登记字段与 materials/guidelines/ 目录

- 状态：proposed
- 记录时间：2026-09-15T08:53:17+00:00
- 来源：本轮用户消息；用户要求“检查用户故事，根据用户故事生成新的设计决策”，并据此调整工程。未提供消息 ID。
- 替代关系：无；补充 DEC-005。
- 用户故事：[US-004](../user-stories/US-004-formatting-guidelines.md)

## 用户原话

> 登记我描述的用户故事：4. 用户描述：帮我梳理论文主题；Agent还要在写作规划中，让用户明确论文写作的遵循的规范文件，以及要求模型要按照论文规范文件进行排版。

## 实现取舍

1. workspace.json 新增 `formatting_guidelines` 数组，元素为 {file, title, version_or_date, locator}；file 为工作区内相对路径并经 safe() 校验，locator 存章节/页码/条款定位。
2. 规范原件放新增目录 `materials/guidelines/`（属用户添加材料，Agent 不修改该目录内容）。
3. 规范清单的登记与变更走 `paper.py decision`（不加 --confirm 为 proposed），保证可追溯。
4. 保留 workspace.json 的 school_requirements 自由文本字段作摘要；结构化登记另起 formatting_guidelines 字段，不替代原字段。
5. 重复安装不升级原则不变：已存在工作区的格式化登记不因重复 init/decision 被覆盖升级。

## 影响范围

workspace.json 数据结构（新增字段与 materials/guidelines/ 目录）；`paper.py decision` 子命令的登记范围；DEC-005 与 US-004 规范确认环节的落盘方式。

## 时间线

- 2026-09-15T08:53:17+00:00：按用户指令检查用户故事并登记本决策，状态 proposed，待用户确认。
