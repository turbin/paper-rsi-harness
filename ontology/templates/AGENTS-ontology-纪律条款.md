# 口径纪律条款模板（ontology G2，DEC-019）

> 用途：供 adopting 工程挂接进其 AGENTS.md（或等价协作规则文件）。本模板文本以下游
> mba-bdp-优月仓储 AGENTS.md「口径纪律」条款为母本参数化；`【】` 占位符按工程实际替换。
> 是否挂接由工程所有者拍板；挂接后本模板文件保留在 ontology/templates/ 不再维护。

## 口径纪律（本体 G2 模板，2026-11-07 上游定版）

- `knowledge/claims.yaml` 是【工程名】数字与口径主张的**单一登记处**：报告/汇报中引用关键数字前，
  先查 `knowledge/graph.md`（或直接查 claims）取 claim id 与证据定位；**不得凭记忆或从旧文档转录数字**
  （「引用即查图」）。
- 修改主张一律编辑 `knowledge/claims.yaml`（勿手改 graph.md，其为自动生成），改后运行
  `python3 ontology/gen_graph.py`；`update_indexes.py` 变更后建议重跑校验
  （`python3 ontology/validate_claims.py`），报警须在下次变更前修复。
- **登记责任**：溯源/冲突核查后由 AI 顺手补登 claim，人工仅做确认（建议不能冒充确认）；
  新增证据文件时同步登记 claim，并在摘要表 `claim_ids` 列登记该文件行（双向一致由校验器核对）。
- SHA 与语义摘要的单一事实源仍是各目录 index.md（自动区块＋手工摘要层）；claims.yaml 只存 id
  与定位符，**不重复记哈希、不复制摘要**（设计稿 §7.3/§9）。
- 证据寻址（伪路径规则）：claims.yaml 的 evidence.file 须为工程内真实相对路径，或 `unarchived:`
  显式标记的未归档来源（官网/口头口径等，locator 注明核实日期）；通配路径（`*`）已废除，
  写了报 error；引用 references/ 台账件写真实路径并附 `ref: REF-NNN`。
- used_in.doc 引用新文档时须在 `ontology/ontology.config.yaml` 的 `doc_aliases` 节注册
  （或改用 ISS/DEC 编号）；未注册为 warning，注册后目标不存在为 error。
- **报警台账规则**：校验报警每次追加写入 `knowledge/validation_log.md`（台账勿手改）；
  验收口径＝警告集合轮次间单调不增，error 须在下次变更前修复。
- 谓词词典随用随加，但不允许同义谓词并存；拼写不一致由校验器报警。
- 枚举值、定位语法、主题分组等工程语义集中在 `ontology/ontology.config.yaml` 维护，
  **不改校验器/图生成器代码**（G2 模板级契约）。
