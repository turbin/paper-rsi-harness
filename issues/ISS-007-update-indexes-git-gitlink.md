# ISS-007 — update_indexes.py 在 git worktree 场景把 .git gitlink 文件纳入索引

- 状态：open
- 创建时间：2026-11-07
- 来源：ontology G2 对抗审核 R1 轮发现 F-1-3（见 issues/ISS-006 处理时间线）。

## 问题

AGENTS.md 明确「.git、缓存、运行态、Git 忽略目录和符号链接不纳入工程索引」。普通仓库中
`.git` 是目录，`update_indexes.py` 的目录排除逻辑可命中；但在 git worktree（如
`main-79be2bc4` 工作树）下 `.git` 是一个 94 字节的普通文件（gitlink，内容 `gitdir: ...`），
按文件快照规则被收录进根 index.md 文件快照表，并产生「首次纳入索引 .git」时间线行。

## 影响

- 与工程索引纪律字面冲突（快照与时间线出现 .git 条目）。
- 不影响校验器与本体机制运行（校验器按文件名读快照表，.git 行为冗余噪音）。
- 波及范围：所有以 worktree 形态使用本工具的工程。

## 验收条件

- update_indexes.py 扫描时排除名为 `.git` 的文件（无论文件还是目录形态）；
- 被污染的既有 index.md 清理后重扫不再出现 .git 条目。

## 处理时间线

- 2026-11-07：登记（open）。属上游既有工具缺陷在 worktree 场景的暴露，非 ontology 引入；
  修复安排另行排期，不阻塞 ISS-006 收尾。
