# DEC-016 — reset-topic 子命令与两阶段门禁

- 状态：confirmed
- 确认时间：2026-09-15T09:50:20+00:00（用户原话“我确认DEC转为confirmed”，当前会话用户消息）
- 记录时间：2026-09-15T08:53:17+00:00
- 来源：本轮用户消息；用户要求“检查用户故事，根据用户故事生成新的设计决策”，并据此调整工程。未提供消息 ID。
- 替代关系：无；落实 DEC-006、DEC-007（US-005 范围与“否”分支语义）。
- 用户故事：[US-005](../user-stories/US-005-change-writing-topic.md)

## 用户原话

> 帮我登记用户故事：1. 用户可以更改写作主题。直接与agent说：我想改一版xxx主题的内容。Agent：将当前目录下所有相关文件包括决策文件等存放到git中，然后询问用户是否需要清空当前工作区重新开始写作？如果用户回答是，那么新建新的分支并切换到该分支下。将当前目录恢复到工作区的初始状态，清空所有决策信息和issue信息以及之前版本在写作过程中产生的任何文件和信息，重新使用苏格拉底式提问流程skill帮助用户梳理工作写作思路。

## 实现取舍

1. 新子命令：`paper.py reset-topic --topic <主题摘要> [--confirm]`，两阶段门禁：不带 --confirm 只做 `git add -A && git commit`（本地备份 + 打印待执行计划）；带 --confirm 才执行 `git checkout -b feature-<slug>` 并清空工作区。
2. 只本地提交，不 push、不配置 remote。
3. 须为已初始化论文工作区；unborn HEAD（无提交历史）时以首次提交作为备份点。
4. 初始状态 = initialize() 幂等产出全集（DIRS + 文件模板 + index.md 重建）；workspace.json 的 topic、school_requirements、ai_disclosure_policy 回空字符串，formatting_guidelines 回空数组。
5. 默认保留用户后端配置（profiles/backends），仅重置主题相关字段。
6. 不触碰 materials/、.gitignore、AGENTS.md/CLAUDE.md 的用户合并内容。
7. 分支 slug 规则：小写、空白与下划线转 `-`、删除非法字符、拒绝空摘要、截断约 48 字符；默认 ASCII，中文摘要需显式 `--allow-unicode-branch`；目标分支已存在则拒绝执行。
8. 清空后命令输出指引：“请对 Agent 说帮我梳理论文主题以启动 paper-spec-socratic”。
9. 用户答“否”语义 = 按上一版本迭代，可另用 `--branch-only` 只建分支不清空。
10. reset 同时回空 formatting_guidelines（与 US-005 澄清口径一致：上一主题的规范登记不带入新主题）。
11. notes/ 根目录下用户人工整理的文献笔记默认保留（属于用户劳动成果），其余模板外产物（决策、issue、上一版本写作产物等）清除。

## 影响范围

`paper.py` 新增子命令与 git 操作；US-005 的备份、确认、分支、重置四步落地；workspace.json 重置字段范围；与 DEC-006、DEC-007 的衔接。

## 时间线

- 2026-09-15T08:53:17+00:00：按用户指令检查用户故事并登记本决策，状态 proposed，待用户确认。
- 2026-09-15T09:50:20+00:00：用户确认本决策，状态由 proposed 转为 confirmed。
