#!/usr/bin/env python3
"""claims.yaml 校验器（本体建模 v1.3.1 的 G2 config 化重构，DEC-019 / 设计稿 §12）

行为与下游硬编码版（mba-bdp-优月仓储/knowledge/validate_claims.py）零漂移：
校验逻辑、报警文案、顺序、退出码、--quiet、validation_log.md 落盘格式逐字对齐，
仅把五张硬编码注册表（DOC_ALIASES/LOC_GRAMMAR/SUMMARY_TABLES/ENUMS/THEMES）
改为从 ontology.config.yaml 读取（C1–C8 处置见设计稿 §12.3/§12.4）。

config 定位顺序：命令行 --config 优先；否则 ontology/ontology.config.yaml；
再否则 knowledge/ontology.config.yaml；均缺失时在工程根按保守默认生成
knowledge/ontology.config.yaml 并 warning 引导补登（§12.4）。

校验项（设计稿 v1.3 §3/§6/§7.4）：
  1. 结构校验：YAML 可解析、id 唯一、必填属性齐全、枚举值合法
  2. 冲突边一致性：conflicts_with 双向存在性检查（单向声明为警告，不自动展开）
  3. 证据文件存在性：evidence.file 必须是真实路径或 unarchived: 显式标记
     （v1.3.1：硬编码前缀豁免已废除；通配 `*` 静默跳过通道关闭，改为 error）
  4. SHA 同源校验：不在本文件算哈希——检查 evidence.file 是否被某目录 index.md 快照收录（registered_in）
  5. tracked_by / supersedes 引用的编号是否存在（DEC/ISS 文件在盘）
  6. used_in 文档级存在性（v1.3.1）：doc 须为 ISS/DEC 编号或 doc_aliases 已注册别名
  7. claim_ids 双写一致性（v1.3.1）：摘要表 claim_ids 列 ↔ claims.yaml evidence 双向核对
  8. 报警落盘（v1.3.1）：全部警告追加写入 knowledge/validation_log.md；
     验收口径＝警告集合轮次间单调不增（设计稿 §6 报警闭环）
  9. used_in.loc 定位语法校验（v2 高优批，ISS-19#1）：按文档类型 loc_grammar 注册语法，
     不匹配片段为警告（loc 属人工维护的半自由锚点）
  10. described_by 摘要行锚点校验（v2 高优批，ISS-19#2）：摘要表行「一句话摘要/敏感度」
      关键列非空，空缺即警告（文件改版后摘要未同步的探测点）
  11. 文档版本边校验（v2 高优批，ISS-19#4）：knowledge/documents.yaml 的 derived_from/
      supersedes 指向存在性；pptx 成品页数锚 pages_expected 对照（ISS-017 结构漂移防复发）
用法：
  python3 ontology/validate_claims.py                 # 全量校验（--root 指定工程根）
  python3 ontology/validate_claims.py --quiet         # 仅报错
  python3 ontology/validate_claims.py --config 路径   # 显式指定 config
退出码：0=全部通过；1=存在 error
"""
import argparse
import datetime
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config_loader import OntologyConfig, parse_config  # noqa: E402

# used_in.doc 文档别名注册表（v1.3.1）：别名 → 工程内目标（文件或目录）。
# 新增文档引用时在 ontology.config.yaml 的 doc_aliases 节登记；ISS/DEC 编号无需注册
# （按 issues/decisions 文件存在性检查）。缺该节时保守默认=空表并 warning 引导补登。
DOC_ALIASES = {}

# used_in.loc 定位语法注册表（v2 高优批）：别名 → 片段正则列表。
# loc 为「/」分隔的锚点片段序列；每片段须命中该文档的正则之一，未命中为警告。
# 特殊片段（语境/对照项等修饰语）允许跟随在合法锚点后，用 LOC_FREE_TAIL 放行。
LOC_GRAMMAR = {}

# claim_ids 双写一致性检查范围（v1.3.1）：目录 → 摘要表所在 index.md。
# 表头须含 claim_ids 列（列序不敏感，按文件名匹配行，抗行序变化）。
SUMMARY_TABLES = {}

REQUIRED = ["id", "predicate", "value", "caliber", "status", "subject", "verify_depth", "evidence", "used_in"]

LOC_FREE_TAIL = re.compile(r"^（[^）]*）$")   # 整段为修饰语（独立片段）
LOC_TAIL_STRIP = re.compile(r"（[^）]*）$")   # 片段尾部修饰语剥离（非锚定）

DEFAULT_ISSUES_DIR = "issues"
DEFAULT_DECISIONS_DIR = "decisions"
DEFAULT_ISS_GLOB = "ISS-*"
DEFAULT_DEC_GLOB = "DEC-*"


class Context:
    """一次校验的运行上下文：工程根、config、各注册表。"""

    def __init__(self, root, config, source_desc):
        self.root = root
        self.config = config
        self.source_desc = source_desc
        cfg = config.data if config else {}
        self.table_headers = config.table_headers if config else None
        # doc_aliases（C1）
        self.doc_aliases = {}
        if config and config.doc_aliases:
            self.doc_aliases = {str(k): str(v) for k, v in config.doc_aliases.items()}
        # loc_grammar（C2）
        self.loc_grammar = {}
        if config and config.loc_grammar:
            for k, v in config.loc_grammar.items():
                if isinstance(v, list):
                    self.loc_grammar[str(k)] = [str(x) for x in v]
        # summary_tables（C3，已归一 {目录: index路径}）
        self.summary_tables = {}
        if config and config.summary_tables:
            self.summary_tables = dict(config.summary_tables)
        # enums（C4）
        enums_raw = config.enums if config else None
        self.enums = {}
        if isinstance(enums_raw, dict):
            for k, v in enums_raw.items():
                if isinstance(v, list):
                    self.enums[str(k)] = set(str(x) for x in v)
                elif isinstance(v, dict) and "values" in v:
                    self.enums[str(k)] = set(str(x) for x in v["values"])
        # governance（C5，可选）
        gov = cfg.get("governance") if isinstance(cfg.get("governance"), dict) else None
        gov = gov or {}
        self.issues_dir = str(gov.get("issues_dir", DEFAULT_ISSUES_DIR))
        self.decisions_dir = str(gov.get("decisions_dir", DEFAULT_DECISIONS_DIR))
        self.issue_glob = str(gov.get("issue_glob", DEFAULT_ISS_GLOB))
        self.dec_glob = str(gov.get("dec_glob", DEFAULT_DEC_GLOB))
        # index_markers（C6）
        self.index_start = config.index_start if config else "<!-- project-index:start -->"
        self.index_end = config.index_end if config else "<!-- project-index:end -->"


def locate_config(root, explicit):
    """config 定位三级顺序（§12.4）：--config > ontology/ontology.config.yaml > knowledge/ontology.config.yaml。
    返回 (config_path 或 None)。"""
    if explicit:
        p = Path(explicit)
        if not p.is_absolute():
            p = root / p
        return p
    for rel in ("ontology/ontology.config.yaml", "knowledge/ontology.config.yaml"):
        p = root / rel
        if p.exists():
            return p
    return None


def generate_default_config(root, path):
    """找不到 config 时在工程根按保守默认生成 knowledge/ontology.config.yaml（§12.4 闭环）。
    返回 (是否生成, 提示消息列表)。"""
    target = Path(path)
    text = """# ontology.config.yaml——本体五表注册表（G2 模板级，DEC-019/设计稿 §12.4）
# 本文件由 validate_claims.py 在找不到 config 时按保守默认自动生成（空骨架）。
# 请按工程实际补登各节；每节含义见 ontology/README.md（L5 适配契约）。

# C1 文档别名：used_in.doc 别名 → 工程内路径（文件或目录）
doc_aliases: {}

# C2 used_in.loc 定位语法：别名 → 正则片段列表
loc_grammar: {}

# C3 摘要表 claim_ids 双写检查范围：目录 → 该目录 index.md（含「## 文件摘要表」）
summary_tables: {}

# C4 枚举（缺省即下列三枚举；属性名 id/predicate/value/caliber/status/subject/
#     verify_depth/evidence/used_in 领域无关、不得改动）
enums:
  caliber: [written, self, disclosed, planned, visit, official]
  status: [verified, self-reported, pending-cert, conflict, retired]
  verify_depth: [transcribed, source_verified, passage_checked, value_recalculated]

# C5 治理目录与编号 glob（可选；缺省即下列值）
governance:
  issues_dir: issues
  decisions_dir: decisions
  issue_glob: "ISS-*"
  dec_glob: "DEC-*"

# C6 索引自动区块标记（可选；缺省即下列值）
index_markers:
  start: "<!-- project-index:start -->"
  end: "<!-- project-index:end -->"

# C7 摘要表表头（可选；缺省即下列值）
summary_table_headers:
  table_title: 文件摘要表
  file_col: 文件
  claim_col: claim_ids
  summary_col: 一句话摘要
  sensitivity_col: 敏感度

# C8 图主题分组：[主题名, [谓词...]]（gen_graph.py 用；空 = 全部落「其他」组）
themes: []
"""
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    msg = [
        f"未找到 ontology 配置，已按保守默认生成骨架: {target.relative_to(root) if target.is_absolute() and root in target.parents else target}",
        "请编辑该 config 补登 doc_aliases / loc_grammar / summary_tables / themes（各节含义见 ontology/README.md）",
    ]
    return msg


def load_index_snapshots(ctx):
    """收集所有目录 index.md 自动区块中的文件路径（registered_in 检查用）。"""
    indexed = set()
    for idx in ctx.root.rglob("index.md"):
        if ".git" in idx.parts or "node_modules" in idx.parts:
            continue
        try:
            text = idx.read_text(encoding="utf-8")
        except Exception:
            continue
        m = re.search(re.escape(ctx.index_start) + r"(.*?)" + re.escape(ctx.index_end), text, re.S)
        if not m:
            continue
        rel_base = idx.parent
        for row in re.findall(r"^\| (.+?) \| \d{4}-", m.group(1), re.M):
            name = row.strip().replace("&#124;", "|").strip("`")
            if name in ("文件", "文件快照", "---"):
                continue
            rel = (rel_base / name).resolve()
            indexed.add(str(rel))
    return indexed


def load_summary_claims_map(ctx):
    """解析摘要表 claim_ids 列 → {目录 key: {has_column, rows:{文件名:[CLM-xxx]}}}
    按文件名匹配行（不依赖行号，抗行序变化）；表无该列时 has_column=False。"""
    tables = {}
    hdr = ctx.table_headers
    table_title = hdr["table_title"] if hdr else "文件摘要表"
    file_col = hdr["file_col"] if hdr else "文件"
    claim_col_name = hdr["claim_col"] if hdr else "claim_ids"
    for key, idx in ctx.summary_tables.items():
        p = ctx.root / idx
        if not p.exists():
            tables[key] = None
            continue
        text = p.read_text(encoding="utf-8")
        m = re.search(r"## " + re.escape(table_title) + r"(.*?)(?=\n## |\n<!-- project-index)", text, re.S)
        mapping = {}
        claim_col = None
        if m:
            for row in m.group(1).splitlines():
                s = row.strip()
                if not s.startswith("|"):
                    continue
                cells = [x.strip() for x in s.strip("|").split("|")]
                if cells and cells[0] == file_col:
                    claim_col = next((i for i, c in enumerate(cells) if c == claim_col_name), None)
                    continue
                if all(set(x) <= set("-: ") for x in cells):
                    continue
                if claim_col is None or claim_col >= len(cells):
                    continue
                ids = re.findall(r"CLM-\d+", cells[claim_col])
                if ids:
                    mapping[cells[0]] = ids
        tables[key] = {"has_column": claim_col is not None, "rows": mapping}
    return tables


def parse_claims(text):
    """轻量 YAML 解析（避免 PyYAML 依赖）：按顶层 '  - id:' 切块，逐行抓 key: value。
    书写规范见 claims.yaml 头注与设计稿 §6：恰好 2 空格缩进切块、禁行内注释、禁多行值。"""
    claims, cur = [], None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^  - id:\s*(\S+)", line)
        if m:
            cur = {"id": m.group(1), "_lines": []}
            claims.append(cur)
            continue
        if cur is None:
            continue
        cur["_lines"].append(line)
    # 从每块行里抓属性
    for c in claims:
        buf = {"evidence": [], "used_in": [], "conflicts_with": [], "tracked_by": [], "supersedes": []}
        in_evidence = in_used = False
        for ln in c["_lines"]:
            if re.match(r"^    evidence:", ln):
                in_evidence, in_used = True, False
                continue
            if re.match(r"^    used_in:", ln):
                in_evidence, in_used = False, True
                continue
            if re.match(r"^    [a-z_]+:", ln) and not ln.startswith("      "):
                in_evidence = in_used = False
            em = re.match(r"^      - file:\s*(.+)$", ln)
            if em and in_evidence:
                buf["evidence"].append({"file": em.group(1).strip()})
                continue
            rm = re.match(r"^        ref:\s*(.+)$", ln)
            if rm and in_evidence and buf["evidence"]:
                buf["evidence"][-1]["ref"] = rm.group(1).strip()
                continue
            um = re.match(r"^      - \{doc:\s*([^,}]+),\s*loc:\s*(.+?)\}\s*$", ln)
            if um and in_used:
                buf["used_in"].append({"doc": um.group(1).strip(), "loc": um.group(2).strip()})
                continue
            km = re.match(r"^    (\w+):\s*(.*)$", ln)
            if km and not in_evidence:
                k, v = km.group(1), km.group(2).strip()
                if k in ("conflicts_with", "tracked_by", "supersedes"):
                    buf[k] = re.findall(r"[\w-]+", v) if v else []
                elif k not in ("id",):
                    buf[k] = v
        c.pop("_lines")
        c.update(buf)
    return claims


def check_loc_grammar(ctx, claims, warns, errors):
    """v2 高优批（ISS-19#1）：used_in.loc 按文档类型语法校验，片段不匹配为警告。
    片段允许携带括号修饰语（如「附录C第8条（对照项）」）：剥离括号尾巴后再匹配语法。
    config 中非法正则（re.PatternError）不中断校验：报 error 并跳过该条语法。"""
    # 预编译全部语法正则；非法正则报 error，运行时置空跳过
    grammar_ok = {}
    for doc, pats in ctx.loc_grammar.items():
        compiled = []
        for pat in pats:
            try:
                compiled.append(re.compile(pat))
            except re.error as e:
                errors.append(f"loc_grammar 配置非法正则「{doc}」: {pat}（{e}）")
        grammar_ok[doc] = compiled
    for c in claims:
        for u in c.get("used_in", []):
            doc, loc = u.get("doc", ""), u.get("loc", "")
            grammar = grammar_ok.get(doc)
            if not grammar or not loc:
                continue
            for seg in [s.strip() for s in loc.split("/") if s.strip()]:
                core = LOC_TAIL_STRIP.sub("", seg).strip()  # 剥离片段尾部括号修饰语
                if not core:
                    continue
                if any(p.match(core) for p in grammar):
                    continue
                warns.append(f"{c['id']}: used_in.loc 片段「{seg}」不符合「{doc}」定位语法（loc_grammar）")


def check_summary_anchor(ctx, tables, warns):
    """v2 高优批（ISS-19#2）：摘要表行关键列非空校验（described_by 语义锚点）。"""
    hdr = ctx.table_headers
    table_title = hdr["table_title"] if hdr else "文件摘要表"
    file_col = hdr["file_col"] if hdr else "文件"
    claim_col_name = hdr["claim_col"] if hdr else "claim_ids"
    summary_col = hdr["summary_col"] if hdr else "一句话摘要"
    sens_col = hdr["sensitivity_col"] if hdr else "敏感度"
    for key, table in tables.items():
        if not table or not table.get("has_column"):
            continue
        p = ctx.root / ctx.summary_tables[key]
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        m = re.search(r"## " + re.escape(table_title) + r"(.*?)(?=\n## |\n<!-- project-index)", text, re.S)
        if not m:
            continue
        claim_col = None
        for row in m.group(1).splitlines():
            s = row.strip()
            if not s.startswith("|"):
                continue
            cells = [x.strip() for x in s.strip("|").split("|")]
            if cells and cells[0] == file_col:
                claim_col = next((i for i, cc in enumerate(cells) if cc == claim_col_name), None)
                summary_idx = next((i for i, cc in enumerate(cells) if summary_col in cc), None)
                sens_idx = next((i for i, cc in enumerate(cells) if cc == sens_col), None)
                continue
            if all(set(x) <= set("-: ") for x in cells):
                continue
            if claim_col is None or claim_col >= len(cells):
                continue
            fname, summ, sens = cells[0], cells[summary_idx] if summary_idx is not None and summary_idx < len(cells) else "x", cells[sens_idx] if sens_idx is not None and sens_idx < len(cells) else "x"
            if not summ:
                warns.append(f"{key} 摘要表行「{fname}」一句话摘要为空（described_by 锚点缺失）")
            if not sens:
                warns.append(f"{key} 摘要表行「{fname}」敏感度为空（described_by 锚点缺失）")


def load_documents(ctx):
    """解析 knowledge/documents.yaml（v2 文档版本边）。"""
    documents = ctx.root / "knowledge" / "documents.yaml"
    docs = []
    if not documents.exists():
        return docs
    cur = None
    for raw in documents.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^  - id:\s*(\S+)", line)
        if m:
            cur = {"id": m.group(1), "_lines": []}
            docs.append(cur)
            continue
        if cur is not None:
            cur["_lines"].append(line)
    for d in docs:
        for ln in d["_lines"]:
            km = re.match(r"^    (\w+):\s*(.*)$", ln)
            if km:
                k, v = km.group(1), km.group(2).strip()
                if k in ("derived_from", "supersedes"):
                    d[k] = re.findall(r"[\w\-.→：:\s]+", v) if v else []
                    d[k] = [x.strip() for x in re.split(r"[,、]", v) if x.strip()]
                else:
                    d[k] = v
        d.pop("_lines")
    return docs


def check_documents(ctx, docs, id_set, warns, errors):
    """v2 高优批（ISS-19#4）：文档版本边指向存在性＋pptx 页数锚对照。"""
    doc_ids = {d["id"] for d in docs}
    for d in docs:
        for k in ("derived_from", "supersedes"):
            for target in d.get(k, []):
                t = target.strip()
                if not t or t == "无":
                    continue
                if t in doc_ids:
                    continue
                if (ctx.root / t).exists():  # 允许直接写工程相对路径
                    continue
                errors.append(f"{d['id']}: {k} 指向不存在条目或路径: {t}")
        # pptx 页数锚（ISS-017 结构漂移防复发）
        pages = d.get("pages_expected")
        f = d.get("file", "")
        if pages and f and f.endswith(".pptx") and (ctx.root / f).exists():
            try:
                with zipfile.ZipFile(ctx.root / f) as z:
                    actual = len([n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)])
                if actual != int(pages):
                    errors.append(f"{d['id']}: pptx 实际 {actual} 页 ≠ pages_expected {pages}（结构漂移，ISS-017 教训）")
            except Exception as e:
                warns.append(f"{d['id']}: pptx 页数检查失败: {e}")


def write_log(ctx, ok, n_claims, errors, warns):
    """报警落盘（v1.3.1 报警闭环）：每次校验追加一条记录；通过时只记摘要行。"""
    log = ctx.root / "knowledge" / "validation_log.md"
    stamp = datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat(timespec="seconds")
    lines = [f"\n## {stamp}", f"- 结果：{'✅ 通过' if ok else '✗ 存在错误'}；{n_claims} 条主张；error {len(errors)} / warning {len(warns)}"]
    for e in errors:
        lines.append(f"- ✗ {e}")
    for w in warns:
        lines.append(f"- ⚠ {w}")
    log.parent.mkdir(parents=True, exist_ok=True)
    if not log.exists():
        log.write_text("# claims 校验报警台账（自动追加，勿手改）\n\n> 验收口径：警告集合轮次间单调不增；error 必须在下次变更前修复（AGENTS.md 口径纪律）。\n", encoding="utf-8")
    with log.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def main():
    ap = argparse.ArgumentParser(add_help=True, description="claims.yaml 校验器（G2 config 化）")
    ap.add_argument("--config", help="ontology.config.yaml 路径（缺省按三级顺序定位）")
    ap.add_argument("--root", help="工程根（缺省=脚本上级目录）")
    ap.add_argument("--quiet", action="store_true", help="仅报错")
    args, _unknown = ap.parse_known_args()

    quiet = bool(args.quiet)
    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
    cfg_path = locate_config(root, args.config)
    config_msgs = []
    if cfg_path is None:
        cfg_path = root / "knowledge" / "ontology.config.yaml"
        config_msgs = generate_default_config(root, cfg_path)
    config = OntologyConfig(parse_config(cfg_path.read_text(encoding="utf-8")))
    ctx = Context(root, config, str(cfg_path))

    text = (root / "knowledge" / "claims.yaml").read_text(encoding="utf-8")
    claims = parse_claims(text)
    errors, warns = [], []

    # config 缺失节引导（§12.4：保守默认＋warning 指向 config 补登；不改变报警条数口径——
    # 这些是前置提示，逐条输出在警告区之前，不影响下游子集回归的报警逐条对照）
    for m in config_msgs:
        print(f"提示: {m}", file=sys.stderr)
    for w in config.warnings:
        print(f"提示: {w}", file=sys.stderr)

    if not claims:
        errors.append("claims.yaml 未解析到任何条目（检查是否遵循书写规范：claims: 根键＋2 空格缩进）")

    ids = [c["id"] for c in claims]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        errors.append(f"重复 id: {sorted(dup)}")
    id_set = set(ids)

    indexed_files = load_index_snapshots(ctx)
    tables = load_summary_claims_map(ctx)

    # 谓词词典一致性
    pred_map = {}
    for c in claims:
        key = re.sub(r"[\s（）()]", "", c["predicate"])
        pred_map.setdefault(key, c["predicate"])
        if pred_map[key] != c["predicate"]:
            warns.append(f"{c['id']}: 谓词写法不一致「{c['predicate']}」vs「{pred_map[key]}」")

    for c in claims:
        for k in REQUIRED:
            if k not in c or c[k] in (None, "", []):
                errors.append(f"{c['id']}: 缺必填属性 {k}")
        for k, allowed in ctx.enums.items():
            if k in c and c[k] not in allowed:
                errors.append(f"{c['id']}: {k}={c[k]} 不在枚举 {sorted(allowed)}")
        # 证据寻址（v1.3.1：unarchived: 显式标记 / 真实路径；通配与硬编码豁免已废除）
        for ev in c.get("evidence", []):
            f = ev.get("file", "")
            if not f:
                errors.append(f"{c['id']}: evidence.file 为空")
                continue
            if f.startswith("unarchived:"):
                warns.append(f"{c['id']}: 证据「{f}」为未归档来源，待归档存证或企业核证")
                continue
            if "*" in f:
                errors.append(f"{c['id']}: 通配证据路径已废除（v1.3.1），须写真实路径或 unarchived: 标记: {f}")
                continue
            p = root / f
            if not p.exists():
                errors.append(f"{c['id']}: 证据文件不存在: {f}")
                continue
            resolved = str(p.resolve())
            if resolved not in indexed_files and p.name != "index.md":
                warns.append(f"{c['id']}: 证据文件未被任何 index.md 快照收录（建议跑 update_indexes）: {f}")
            # claim_ids 双写一致性（反向：claim→摘要表行；index.md 自身为表载体，不要求入表）
            for key, table in tables.items():
                if table is None:
                    continue
                prefix = key.rstrip("/") + "/"
                if f.startswith(prefix):
                    base = f[len(prefix):]
                    if base == "index.md":
                        continue
                    row_ids = table["rows"].get(base)
                    if row_ids is None:
                        warns.append(f"{c['id']}: 摘要表缺该文件行或行未登记 claim_ids: {base}")
                    elif c["id"] not in row_ids:
                        warns.append(f"{c['id']}: 摘要表 claim_ids 列缺登记本条: {base}")

        # used_in 文档级存在性（v1.3.1）
        for u in c.get("used_in", []):
            doc = u.get("doc", "")
            if doc.startswith("ISS-"):
                if not list(root.glob(f"{ctx.issues_dir}/{doc}*.md")):
                    errors.append(f"{c['id']}: used_in 指向不存在的 {doc}")
            elif doc.startswith("DEC-"):
                if not list(root.glob(f"{ctx.decisions_dir}/{doc}*.md")) + list(root.glob(f"{ctx.decisions_dir}/{doc}*.json")):
                    errors.append(f"{c['id']}: used_in 指向不存在的 {doc}")
            elif doc in ctx.doc_aliases:
                target = root / ctx.doc_aliases[doc]
                if not target.exists():
                    errors.append(f"{c['id']}: used_in.doc 别名「{doc}」目标不存在: {ctx.doc_aliases[doc]}")
            else:
                warns.append(f"{c['id']}: used_in.doc「{doc}」未注册（加入 config doc_aliases 或改用 ISS/DEC 编号）")
        # conflicts_with 双向性
        for other in c.get("conflicts_with", []):
            if other not in id_set:
                errors.append(f"{c['id']}: conflicts_with 指向不存在的 {other}")
            else:
                oc = next(x for x in claims if x["id"] == other)
                if c["id"] not in oc.get("conflicts_with", []):
                    warns.append(f"{c['id']} ⇄ {other}: 冲突边单向（对方未回指）")
        # tracked_by / supersedes 存在性
        for t in c.get("tracked_by", []):
            num = re.sub(r"[\[\]]", "", t)
            if num.startswith("ISS"):
                hits = list(root.glob(f"{ctx.issues_dir}/{num}*.md"))
                if not hits:
                    errors.append(f"{c['id']}: tracked_by 指向不存在的 {num}")
            elif num.startswith("DEC"):
                hits = list(root.glob(f"{ctx.decisions_dir}/{num}*.md")) + list(root.glob(f"{ctx.decisions_dir}/{num}*.json"))
                if not hits:
                    errors.append(f"{c['id']}: tracked_by 指向不存在的 {num}")
        for s in c.get("supersedes", []):
            if s not in id_set:
                errors.append(f"{c['id']}: supersedes 指向不存在的 {s}")

    # claim_ids 双写一致性（正向：摘要表行→claim evidence 反查）
    for key, table in tables.items():
        if table is None:
            warns.append(f"{key}: 摘要表不存在（v1.3.1 种子契约，请补建）")
            continue
        if not table["has_column"]:
            warns.append(f"{key}: 摘要表无 claim_ids 列（v1.3.1 种子契约，请补列）")
            continue
        for base, row_ids in table["rows"].items():
            for cid in row_ids:
                if cid not in id_set:
                    errors.append(f"摘要表 {key} 行「{base}」claim_ids 指向不存在的 {cid}")
                else:
                    claim = next(x for x in claims if x["id"] == cid)
                    bases = {Path(e["file"]).name for e in claim.get("evidence", [])
                             if not e["file"].startswith("unarchived:") and "*" not in e["file"]}
                    if base not in bases:
                        warns.append(f"{cid} 的 evidence 不含「{base}」，摘要表 claim_ids 列疑似多登")

    n_conflict = sum(1 for c in claims if c.get("conflicts_with"))
    n_pending = sum(1 for c in claims if c.get("status") == "pending-cert")

    # v2 高优批（ISS-19#1/#2/#4）
    check_loc_grammar(ctx, claims, warns, errors)
    check_summary_anchor(ctx, tables, warns)
    documents = load_documents(ctx)
    check_documents(ctx, documents, id_set, warns, errors)
    n_docs = len(documents)

    if not quiet:
        print(f"claims.yaml 校验：{len(claims)} 条主张")
        print(f"  conflicts_with 边：{n_conflict * 2} 处声明（{n_conflict} 对）")
        print(f"  pending-cert（待企业核证）：{n_pending} 条")
        print(f"  文档版本节点：{n_docs} 条（documents.yaml）")
    if warns:
        print(f"\n警告 {len(warns)} 条：")
        for w in warns:
            print(f"  ⚠ {w}")
    if errors:
        print(f"\n错误 {len(errors)} 条：")
        for e in errors:
            print(f"  ✗ {e}")
        write_log(ctx, False, len(claims), errors, warns)
        sys.exit(1)
    if not quiet:
        print("\n✅ 全部校验通过")
    write_log(ctx, True, len(claims), errors, warns)


if __name__ == "__main__":
    main()
