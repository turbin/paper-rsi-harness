# DEC-011 — 文献条目文件结构与核验状态分级

- 状态：proposed
- 记录时间：2026-09-15T08:53:17+00:00
- 来源：本轮用户消息；用户要求“检查用户故事，根据用户故事生成新的设计决策”，并据此调整工程。未提供消息 ID。
- 替代关系：无；补充 DEC-003。
- 用户故事：[US-002](../user-stories/US-002-writing-plan.md)

## 用户原话

> 登记我描述的用户故事：2. 用户：帮我梳理论文主题；Agent：在梳理完成主题内容后并登记代办issue后，根据主题内容生成论文编写计划。论文计划中需要包含：a. 论文主题内容背景包含，定义论文所要解决的问题内容，以及问题范围。b. 论文写作大纲：定义论文写作大纲框架，规定论文中每个章节描述的内容概述。c. 文献列表：罗列本地用户已经下好的或者指定好的，或者由Agent自己通过多数据源搜索和查找并验证来源的文献，以及文献的对于这篇论文的贡献信息，包括：文献中对于用户论文问题的可引用的段落位置以及段落内容的摘要。该文献对于整篇论文研究的贡献。

## 实现取舍

1. 每篇文献一个文件：`references/REF-<三位编号>-<slug>.md`。
2. frontmatter 字段：id、title、authors、year、source_type（local | user_specified | agent_retrieved）、source_detail、verification{status: unverified | source_verified | passage_checked, basis}、related_issues[]。
3. 正文两节：①可引用段落定位表（位置 + 摘要 + 与论文问题的关系）；②该文献对整篇研究的贡献。
4. 维护 `references/index.md` 摘要表（编号 / 题名 / 来源类型 / 核验状态 / 关联 issue）。
5. 核验状态分级：source_verified（确认文献存在）≠ passage_checked（可引用段落已核对）；确认文献存在不能代替段落核对。
6. 缺全文或段落无法核对时，verification 保持非 passage_checked，并关联待办 ISS；禁止虚构段落位置、摘要或贡献依据。

## 影响范围

references/ 目录的条目模板与索引；US-002 文献列表与逐篇贡献信息的落盘格式；与 DEC-010 计划第三节的衔接。

## 时间线

- 2026-09-15T08:53:17+00:00：按用户指令检查用户故事并登记本决策，状态 proposed，待用户确认。
