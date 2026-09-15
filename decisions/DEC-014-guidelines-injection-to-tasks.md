# DEC-014 — 规范向 PM 与 writer/reviewer 任务的三层传递机制

- 状态：confirmed
- 确认时间：2026-09-15T09:50:20+00:00（用户原话“我确认DEC转为confirmed”，当前会话用户消息）
- 记录时间：2026-09-15T08:53:17+00:00
- 来源：本轮用户消息；用户要求“检查用户故事，根据用户故事生成新的设计决策”，并据此调整工程。未提供消息 ID。
- 替代关系：无；补充 DEC-005、DEC-013。
- 用户故事：[US-004](../user-stories/US-004-formatting-guidelines.md)

## 用户原话

> 登记我描述的用户故事：4. 用户描述：帮我梳理论文主题；Agent还要在写作规划中，让用户明确论文写作的遵循的规范文件，以及要求模型要按照论文规范文件进行排版。

## 实现取舍

1. 三层传递机制：①workspace.json 登记的规范指针（路径 + sha256 + locator）注入 PM 与 writer/reviewer 的任务 payload；②规范条款摘录作为显式 --input 文本进入 context_files（现有白名单已够用，PDF 仍须人工转为文本）；③不自动全文注入。
2. 不自动全文注入的理由：上下文预算控制，受 max_context_chars 约束。
3. 规范条款摘录进入输入范围须用户 brief 显式授权，Agent 不自行扩大输入范围。
4. reviewer payload 增加规范符合性检查项，使排版要求可检查而非仅被提及。

## 影响范围

任务 payload 的构造（PM、writer、reviewer 三层）；context_files 白名单与 --input 的使用约定；reviewer 检查项清单；与 DEC-013 登记字段的衔接。

## 时间线

- 2026-09-15T08:53:17+00:00：按用户指令检查用户故事并登记本决策，状态 proposed，待用户确认。
- 2026-09-15T09:50:20+00:00：用户确认本决策，状态由 proposed 转为 confirmed。
