---
name: paper-spec-socratic
description: 当用户开始或继续梳理论文写作思路、希望通过对话澄清并生成论文编写 spec 时使用；或当前工作区 notes/issues/ 下存在 open 状态的遗留问题、需要在继续工作前先向用户索取答案时使用。不适用于直接代写章节或全自动生成内容。
---

# 苏格拉底式论文 spec 澄清

## 核心原则

一次只问一个问题。用户的每个回答都是后续提问的依据，不是待勾选的问卷项。无法澄清的问题必须落盘，绝不让它消失在对话里。

## 启动协议（每次开始工作必须先执行）

1. 检查当前工作区（当前目录）是否存在 `notes/issues/index.md`。
2. 若存在，列出其中所有 `open` 状态的 issue，**在继续任何新工作之前**逐个向用户提问索取答案。
3. 用户给出答案后，更新对应 issue 文件：状态改为 `resolved`，补记答案与日期；更新 `notes/issues/index.md` 中的状态与摘要；然后从清单移除，继续问下一个。
4. 用户说"跳过"或仍无法回答时，该 issue 保持 `open`，继续问下一个，不要纠缠。
5. 全部处理完后才进入澄清对话。

## 对话规则

- **一轮一问**：每条消息只问一个问题，等用户回答后再问下一个。即使用户口音模糊，也基于回答追问，而不是一次性抛出多个问题。
- 提问顺序按五个维度推进：①论文主题信息 → ②论文背景信息 → ③要解决的问题及问题范围 → ④论文大纲框架 → ⑤每个章节的编写结构要求。前一层未基本澄清不进入下一层，但用户主动跳层时跟随用户。第④⑤维（大纲与章节结构）阶段同步进行论文规范文件确认，见「确认论文规范文件与图表索引」节。
- 提问前先查看工作区已有信息（workspace.json 的 topic/school_requirements、notes/、decisions/），已明确的内容不重复提问，只做确认。
- 用户暂时答不上、说"以后再说"、或答案依赖尚不存在的信息（如"等导师回复"）时：**立即停止追问该点**，把它记入 issues（见下），然后回到当前维度继续问其他问题。

## 记录无法澄清的问题（issue）

为每个未澄清问题创建一个文件 `notes/issues/ISS-<三位编号>-<英文或拼音短横线 slug>.md`：

```markdown
---
id: ISS-001
status: open
dimension: 问题范围
created: <YYYY-MM-DD>
resolved: 
---

# <问题一句话描述>

## 提问时的上下文
<当时问的是什么、用户怎么回答的，原话摘录>

## 待澄清内容
<具体缺什么信息>
```

同时维护 `notes/issues/index.md`，表格列：编号 | 问题摘要 | 维度 | 状态 | 提出日期 | 解决日期。新建或关闭 issue 时更新该表。

## 产出 spec

五个维度都有内容（或明确标注"待澄清"并关联 issue 编号）后，写入 `writing/spec/paper-spec.md`：

```markdown
# <论文题目或暂定题目> 编写 Spec
生成日期：<YYYY-MM-DD> · 状态：草案/已确认

## 1. 论文主题信息
<主题、研究对象、论文类型；待澄清处标注（见 ISS-xxx）>

## 2. 论文背景信息
<行业/企业背景、研究动机>

## 3. 问题定义与范围
<核心管理问题、范围边界（含/不含什么）、范围外内容>

## 4. 大纲框架
<章节列表与每章一句话职责>

## 5. 章节编写结构要求
<每章：小节划分、篇幅要求、证据与引用要求、验收标准>

## 附：遗留问题
<open 状态 issue 编号与摘要清单>
```

spec 草案生成后必须请用户逐节确认；用户确认的内容若涉及题目、研究问题、方法、研究对象等实质变更，提醒用户按工作区规则用 `.paper-ai/paper.py decision` 登记确认决议。全部确认后把 spec 状态改为「已确认」。

## 生成编写计划

仅当 spec 状态为「已确认」后，生成 `writing/plan/paper-plan.md`，固定四节：

1. **主题背景、问题定义与范围**：标注来源 spec 的对应章节。
2. **大纲框架及每章内容概述**：章节列表、每章内容概述与呈现方式（文字/图例/表格，见「确认论文规范文件与图表索引」）。
3. **文献列表**：逐项指向 references/ 下文献条目（见「汇集文献」），含每篇对论文的贡献。
4. **遗留问题与信息缺口**：关联 ISS 编号。

计划草案逐节请用户确认，不一次性视为定稿。

## 汇集文献

每篇文献一个文件 `references/REF-<三位编号>-<slug>.md`：

```markdown
---
id: REF-001
title:
authors:
year:
source_type: local | user_specified | agent_retrieved
source_detail:
verification:
  status: unverified | source_verified | passage_checked
  basis:
related_issues: []
---

# <文献题名>

## 可引用段落定位
| 位置 | 摘要 | 与论文问题的关系 |
|---|---|---|

## 对整篇研究的贡献
<该文献对论文整体研究的作用>
```

规则：

- `source_verified`（确认文献存在）≠ `passage_checked`（可引用段落已核对）；缺全文或段落无法核对时 verification 保持非 passage_checked，并关联待办 ISS；禁止虚构段落位置、摘要或贡献。
- v0.1 不自动联网检索：`agent_retrieved` 仅指整理用户提供的检索结果文本，basis 必须记录出处文本位置，无出处文本不得登记为该来源类型。
- 维护 `references/index.md` 摘要表：编号 | 题名 | 来源类型 | 核验状态 | 关联 issue。

## 确认论文规范文件与图表索引

在第④⑤维（大纲框架与章节结构）阶段执行：

1. 确认 `workspace.json` 的 `formatting_guidelines` 登记：引导用户把规范原件放入 `materials/guidelines/`（Agent 不修改该目录），用 `.paper-ai/paper.py decision` 一步完成留痕与写入：
   `python3 .paper-ai/paper.py decision --root . --subject formatting-guidelines --guideline file=<相对路径>,title=<规范标题>,version=<版本或日期>,locator=<章节/页码定位> --text "<用户确认原话>" --evidence notes/user-quote.txt --source-ref "<用户会话出处>" --confirm`
   该命令经 `--guideline` 把登记项写入 workspace.json，`--confirm` 才生效。若用户暂不确认，则去掉 `--confirm`，仅留下 proposed 决议，不写入 workspace.json。
2. 规范条款摘录进入任务输入须用户 brief 显式授权，不自动全文注入；reviewer 任务含规范符合性检查。
3. 规范未明确图表编号格式时，登记 `notes/issues/` 待澄清，禁止默认采用「图 1-1」式编号。
4. 大纲定稿时生成 `writing/outline/figure-table-index.md`（Markdown 表：图/表号 | 名称 | 所在章节 | 说明位置 | 构建/结构说明摘要）。每个图给构建说明（节点连线、坐标轴与指标等），每个表给结构与口径说明；编号唯一性由本 skill 生成索引时人工核对。

## 更改写作主题

触发语：用户说「我想改一版xxx主题的内容」。Agent 按以下编排执行，不替用户跳过确认：

1. 提示用户先运行 `python3 .paper-ai/paper.py reset-topic --root . --topic "<主题摘要>"`（不带 `--confirm`）：该命令只做本地备份提交（git add -A && git commit）并打印待执行计划，用户核对后再决定。
2. 询问用户是否清空当前工作区重新开始。用户确认后，加 `--confirm` 重新执行：建立 feature-<slug> 分支并切换到该分支，把工作区恢复到初始状态（回空 topic/school_requirements/ai_disclosure_policy/formatting_guidelines 等主题字段，清空决策、issue 与上一版本写作产物；详见 DEC-016）。
3. 清空完成后，启动本 skill 重新走苏格拉底式梳理流程。
4. 用户答「否」（不清空）：按上一版本迭代继续；也可改用 `--branch-only` 只建分支不清空。

提醒：reset-topic 只做本地 git 操作，不 push、不配置 remote；清空前的备份提交保留在旧分支上，需要时可从旧分支找回上一版本内容。

## 结束与续接

用户要求暂停或结束时：确认 issues 和 index 已落盘，告知用户"下次开始时会先接着问 open 的问题"，并简述当前进度（哪些维度已定、哪些待澄清）。不要假装对话能自己恢复——续接依赖 issues 目录。

## 常见错误

| 错误 | 纠正 |
|---|---|
| 一条消息问三个问题 | 每轮只问一个，下一个问题依赖上一个答案 |
| 用户答不上来就反复追问 | 记 issue，换话题，下次启动再问 |
| 未澄清问题只留在聊天记录里 | 必须写入 notes/issues/ 并更新索引 |
| spec 写到任意位置/任意文件名 | 固定 writing/spec/paper-spec.md |
| 用户说"按常规来"就直接定稿 | 作为草案默认值，仍需用户确认后才算定稿 |
| 把未核对段落标为可引用（passage_checked） | 缺全文或段落无法核对时保持非 passage_checked，关联待办 ISS |
| 联网检索补文献 | v0.1 不自动联网检索；agent_retrieved 仅限整理用户提供的检索结果文本并记录出处位置 |
| 规范未明确编号格式时自定「图 1-1」式编号 | 登记 notes/issues/ 待澄清，以用户登记的规范为准 |
| 把 source_verified 当 passage_checked | 确认文献存在不等于段落已核对，两者核验等级分开记录 |
