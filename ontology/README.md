# ontology/——工程本体 G2 模板资产（DEC-019；设计依据：下游设计方案 §12，DEC-022 拍板）

模板级通用化：新工程**零代码改动**跑通「登记主张 → 校验 → 生成图」。行为与下游硬编码版
（mba-bdp-优月仓储/knowledge/validate_claims.py、gen_graph.py）零漂移——校验逻辑、报警文案、
退出码、落盘格式逐字对齐，仅把五张硬编码注册表外置为 config（耦合清单 C1–C8 处置见
设计方案 §12.3）。

stdlib-only、Python 3.10+、无 PyYAML、跨平台 pathlib。

## 文件清单

| 文件 | 职责 |
|---|---|
| `validate_claims.py` | 校验器（config 驱动）；校验项、报警文案、退出码、validation_log.md 落盘与下游逐字一致 |
| `gen_graph.py` | 从 claims.yaml 生成 knowledge/graph.md；THEMES 从 config `themes` 节读取 |
| `init_ontology.py` | `init` 子命令＝可发现项自动扫描写 config；`--export-legacy`＝正则提取下游硬编码五表机械转写 config |
| `config_loader.py` | 轻量 YAML 解析与 OntologyConfig 加载（保守默认＋warning） |
| `templates/claims.yaml` | 主张库空骨架（头注书写规范＋1 条注释示例） |
| `templates/documents.yaml` | 文档版本边空骨架 |
| `templates/ontology.config.yaml` | config 全节注释示例 |
| `templates/AGENTS-ontology-纪律条款.md` | 口径纪律条款模板（挂接与否由工程所有者拍板） |
| `test_ontology.py` | stdlib unittest 回归（含对下游真实文件的零漂移对照） |

## L5 适配契约：ontology.config.yaml 全节说明

config 是唯一的工程适配点（**config 文件即 L5 适配契约**，设计稿 §12.4）。顶层节全部可选，
缺失走保守默认并由校验器在 stderr 打 `提示:` 引导补登。两种放置位置均可：`ontology/ontology.config.yaml`
（推荐）或 `knowledge/ontology.config.yaml`；命令行 `--config 路径` 优先。

| 节 | 耦合项 | 形态 | 缺省行为 |
|---|---|---|---|
| `doc_aliases` | C1 | 映射：别名 → 工程内路径（文件或目录） | 空表；used_in.doc 非 ISS/DEC 编号一律 warning「未注册（加入 config doc_aliases…）」 |
| `loc_grammar` | C2 | 映射：别名 → 正则片段列表（单引号串保反斜杠） | 空表；loc 语法校验自动关闭 |
| `summary_tables` | C3 | 映射：目录 → 该目录 index.md（须含「## 文件摘要表」） | 空表；claim_ids 双写校验自动关闭 |
| `enums` | C4 | 映射：属性名 → 值列表（属性名领域无关不改） | 缺省三枚举（caliber 6 值/status 5 值/verify_depth 4 值）＋warning |
| `governance` | C5 | `issues_dir`/`decisions_dir`/`issue_glob`/`dec_glob`（对应设计稿 §12.3 C5「governance_dirs」，命名收敛为 `governance`） | `issues`/`decisions`/`ISS-*`/`DEC-*` |
| `index_markers` | C6 | `start`/`end` 标记字符串 | `<!-- project-index:start -->` / `<!-- project-index:end -->` |
| `summary_table_headers` | C7 | `table_title`/`file_col`/`claim_col`/`summary_col`/`sensitivity_col` | 中文缺省表头（文件摘要表/文件/claim_ids/一句话摘要/敏感度） |
| `themes` | C8 | 列表：`[主题名, [谓词...]]` | 空列表；graph.md 全部落「其他」组 |

示例片段（完整注释示例见 `templates/ontology.config.yaml`）：

```yaml
doc_aliases:
  '建议书v3.1': 'output/项目建议书-20261102-v3.1.md'
loc_grammar:
  '建议书v3.1':
    - '^附录C第\d+条(④)?$'
summary_tables:
  'materials/company/需求资料-2026-10': 'materials/company/需求资料-2026-10/index.md'
enums:
  caliber: [written, self, disclosed, planned, visit, official]
governance:
  issues_dir: issues
  issue_glob: 'ISS-*'
index_markers:
  start: '<!-- project-index:start -->'
summary_table_headers:
  claim_col: claim_ids
themes:
  - ['资产与资质', ['罐容', '许可介质']]
```

书写限制（轻量解析器，无 PyYAML）：扁平 `key: value`、两级嵌套映射、列表行（`- 项`）、
行内 flow（`[...]`/`{...}`，支持一层嵌套子列表）、`#` 注释行、单双引号值。不支持多行块标量、
>2 级嵌套、锚点/别名。`summary_tables` 推荐嵌套映射写法；正则值用**单引号**（反斜杠免转义）。

## 迁移三步（新工程接入）

1. **拷贝**：`ontology/` 整目录拷入新工程；把 `templates/claims.yaml`、`templates/documents.yaml`
   拷为 `knowledge/claims.yaml`、`knowledge/documents.yaml`（空骨架）。
2. **init 生成 config**：`python3 ontology/init_ontology.py init`——自动扫描 issues/、decisions/
   目录与编号 glob、index.md 自动区块标记、含「## 文件摘要表」的 index.md 写入 config；
   语义项（doc_aliases/loc_grammar/themes）为空骨架＋注释示例。已存在 config 不覆盖（`--force` 才覆盖）。
   从下游硬编码版迁移时改用：`python3 ontology/init_ontology.py --export-legacy
   --legacy-dir <下游knowledge目录>`——正则提取五张字面量表机械转写，输出逐条对照报告。
3. **首跑校验**：登记 3 条真实主张后 `python3 ontology/validate_claims.py` 确认全绿；
   `python3 ontology/gen_graph.py` 生成图。

## 机制假设清单（依赖的外部惯例）

校验器假设 adopting 工程存在以下机制；无此惯例的节留空即关闭对应校验：

1. **治理目录惯例**：`issues/`、`decisions/` 目录内 `ISS-NNN-*.md` / `DEC-NNN-*.md` 文件
   （tracked_by/used_in 编号存在性检查按此；可经 `governance` 节改）。
2. **project-index 区块**：各目录 index.md 内 `<!-- project-index:start -->`…`end` 自动区块、
   文件快照表 `| 文件 | 时间 | SHA |` 行（registered_in 收录检查；可经 `index_markers` 节改标记）。
3. **摘要表 Markdown 表格式**：index.md 手工区含 `## 文件摘要表` 二级标题、`|` 表格、
   表头含「文件/一句话摘要/敏感度/claim_ids」列（双写一致性与 described_by 锚点校验；
   可经 `summary_tables`/`summary_table_headers` 节改）。
4. claims.yaml/documents.yaml 的书写规范：见 `templates/claims.yaml` 头注（2/4/6/8 空格缩进层级、
   used_in 单行 flow、禁行内注释）；校验器对解析到 0 条报 error。

## known-diff（相对下游硬编码版的全部有意差异，共 4 类）

1. **注册表名提法**：报警文案中 2 处「DOC_ALIASES」「LOC_GRAMMAR」字样改为「config doc_aliases」「loc_grammar」
   （校验项 6 与校验项 9 的未注册/不匹配文案）；报警条数、顺序、实质内容不变。
   **注意**：该 2 处差异同样进入落盘 knowledge/validation_log.md 的对应行（台账字节不等的唯一来源）。
2. **config 引导提示**：config 缺失/缺节时 stderr 打 `提示:` 行（自动生成骨架、enums 缺省引导）；
   下游无此输出。不进入 warnings 列表、不落盘、不影响报警条数与退出码。
3. **graph.md 头部来源行**：`由 knowledge/gen_graph.py` → `由 ontology/gen_graph.py`
   （路径随脚本位置；其余内容字节级一致）。
4. **校验器头注/用法文档**：docstring 增加 --config/--root 用法说明与 G2 出处；不影响运行时行为。

## 不做清单（G3 边界，维持设计方案 §8/§12.1）

- 不做独立打包（pip 包/依赖声明）、不做它工程自动化实证（G2 验收＝新工程人工四步 ≤30 分钟）。
- 不做 used_in.loc 位置级校验、described_by 行锚点独立校验、冲突边单向自动展开、
  文档层 derived_from 边（维持下游 v2/v3 分期）。
- 不改上游 AGENTS.md（纪律条款模板在 templates/，挂接由用户拍板）。
- 不引入 PyYAML/OWL/RDF 等任何依赖；不上图数据库。
