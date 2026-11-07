# DEC-019 — ontology G2 模板资产：config 外置五表，新工程零代码跑通「登记主张→校验→生成图」

- 状态：confirmed
- 确认时间：2026-11-07（用户直接下达实现指令，当前会话用户消息）
- 记录时间：2026-11-07
- 来源：当前会话用户指令；实施依据为下游设计方案 §12（[DEC-022](../../../../Workspace/repo-workspace/mba-bdp-优月仓储/decisions/DEC-022.md)（下游工程）拍板 G2、实施主体上游 paper-rsi-harness）。
- 替代关系：无。
- 关联问题：[ISS-006](../issues/ISS-006-ontology-template-g2.md)

## 用户原话

> 读取设计方案，按照设计方案对当前工程进行重构。使用多agent 完成该任务，并安排一个agent 进行多轮对抗式审核，直到取得共识后完成任务，最大轮次不超过5次

（2026-11-07；「当前工程」即本上游工程，「设计方案」指下游 notes/2026-11-07-工程本体设计-结构化与非结构化数据引用-v1.md（v1.4，§12 G2 模板级改造）。）

## 设计依据

- 下游设计方案 §12（v1.4 增补）：G2 目标定级与新工程零代码改动验收判据；耦合清单 C1–C8；
  ontology.config.yaml 外置五表；init_ontology.py 自动扫描＋legacy 导出；§12.7 上游重构＋
  四步实测验收（本工程为行为零漂移回归基准）。

## 决策内容

1. 本工程新增 `ontology/` 模板资产目录：
   - `validate_claims.py`（config 驱动校验器）、`gen_graph.py`（THEMES 外置图生成器）、
     `config_loader.py`（轻量 YAML 解析，无 PyYAML）、`init_ontology.py`（init 扫描＋
     `--export-legacy` 正则提取下游五表机械转写）、`templates/`（claims/documents/config
     空骨架与口径纪律条款模板）、`test_ontology.py`（stdlib unittest）、`README.md`（L5 适配契约）。
2. config 节与耦合项一一对应：`doc_aliases`(C1)/`loc_grammar`(C2)/`summary_tables`(C3)/
   `enums`(C4，缺省=三枚举)/`governance`(C5，可选)/`index_markers`(C6，可选)/
   `summary_table_headers`(C7，可选)/`themes`(C8)。全部可选，缺失走保守默认＋warning 引导补登。
3. **行为零漂移约束**：校验逻辑、报警文案、顺序、退出码、--quiet、validation_log.md 落盘格式
   与下游硬编码版逐字对齐；known-diff 仅 4 类（注册表名提法 2 处、config 引导 stderr 提示、
   graph.md 头部来源行路径、校验器 docstring 用法说明），报警条数与实质内容不变。
   验收＝上游 test_paper.py 全过＋下游子集回归逐条一致（test_ontology.py 内置对照用例）。
4. stdlib-only、Python 3.10+、跨平台 pathlib、macOS bash 3.2 环境惯例；不引入 PyYAML。
5. 不改上游 AGENTS.md；纪律条款模板放 `ontology/templates/`，是否挂接由用户后续拍板。
6. 下游工程（/Users/yanbin/Workspace/repo-workspace/mba-bdp-优月仓储）为只读基准，禁止修改。

## 影响范围

新增 `ontology/` 全目录（7 个文件＋templates/ 4 个文件）；`README.md` 交付清单加 ontology/ 行；
`decisions/`、`issues/` 各新增登记文件。不改既有代码（paper.py、scripts/、setup 脚本、test_paper.py）。

## 时间线

- 2026-11-07：用户指令即拍板（confirmed）；同轮完成实现与测试（ontology 28/28 通过、
  上游 test_paper.py 45/45 通过）。
