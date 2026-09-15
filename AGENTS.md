# 源码工程协作规则

本目录是 paper-rsi-harness 源码工程。先读根 index.md、issues/index.md 和 decisions/index.md，再按任务读取代码与相关记录。

- 工程问题使用 issues/ISS-NNN-主题.md，记录状态、来源、影响、验收条件和处理时间线；修复后保留记录。
- 用户对话中的设计决策使用 decisions/DEC-NNN-主题.md，保留准确原话、来源、记录时间、确认状态及影响范围。建议不能冒充用户确认。
- 变更已确认决策时新增记录并引用被替代编号，保留原文件。历史背景见 DESIGN-DECISIONS.md。
- 每次工程变更完成后执行 `python3 scripts/update_indexes.py --reason "本轮变更原因"`（Windows 可用 `py -3`），更新所有受管理目录的 index.md。
- 索引自动区块之外可写目录说明、问题表和决议表。不要手工删除自动区块中的历史。
- 索引时间是扫描观察时间；不代表实际编辑时间。首次扫描建立基线，不追造历史。Git 保存已提交版本；索引不会自动提交。
- .git、缓存、运行态、Git 忽略目录和符号链接不纳入工程索引；user-test/ 是独立试用工作区。
