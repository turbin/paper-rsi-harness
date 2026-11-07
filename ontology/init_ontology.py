#!/usr/bin/env python3
"""init_ontology.py——ontology.config.yaml 初始化与下游硬编码五表导出（G2 模板级，DEC-019/设计稿 §12.5）

子命令：
  init                可发现项自动扫描（issues/、decisions/ 目录与编号 glob、index.md 自动区块
                      标记、含「## 文件摘要表」标题的 index.md）→ 写 config；config 已存在不覆盖
                      （--force 才覆盖）。
  --export-legacy     从下游硬编码版 validate_claims.py / gen_graph.py 源码中**正则提取**五张
                      字面量表（DOC_ALIASES/LOC_GRAMMAR/SUMMARY_TABLES/ENUMS/THEMES），机械转写
                      为 config YAML 并输出转换报告（每表条数、逐条对照）。不猜测、不补全。
用法：
  python3 ontology/init_ontology.py init [--root 工程根] [--force]
  python3 ontology/init_ontology.py --export-legacy --legacy-dir <下游knowledge目录> [--out 路径]
幂等：config 已存在时不覆盖（除非 --force）。
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config_loader import DEFAULT_INDEX_START, DEFAULT_INDEX_END, parse_flow_list  # noqa: E402

SUMMARY_TABLE_TITLE = "文件摘要表"


# ---------------------------------------------------------------- init 扫描

def scan_discoverable(root):
    """可发现项自动扫描（§12.5）：全部为机械判断，不做语义猜测。返回 dict。"""
    found = {
        "issues_dir": None,
        "decisions_dir": None,
        "issue_glob": None,
        "dec_glob": None,
        "index_markers": None,
        "summary_tables": {},   # 目录 → index.md 相对路径（发现到「## 文件摘要表」标题）
        "existing_config": None,
    }
    # 治理目录与编号惯例：从现有文件名机械归纳 glob 前缀
    for name in ("issues", "decisions"):
        d = root / name
        if d.is_dir():
            found[f"{name[:-1]}s_dir" if False else ("issues_dir" if name == "issues" else "decisions_dir")] = name
            stems = sorted(p.name for p in d.glob("*.md") if re.match(r"^(ISS|DEC)-", p.name))
            prefix = "ISS" if name == "issues" else "DEC"
            hits = [s for s in stems if s.startswith(prefix + "-")]
            if hits:
                found["issue_glob" if name == "issues" else "dec_glob"] = f"{prefix}-*"
    # index.md 自动区块标记（取第一个命中的文件确认缺省标记在盘）
    for idx in root.rglob("index.md"):
        if ".git" in idx.parts or "node_modules" in idx.parts:
            continue
        try:
            text = idx.read_text(encoding="utf-8")
        except Exception:
            continue
        if DEFAULT_INDEX_START in text and DEFAULT_INDEX_END in text:
            found["index_markers"] = {"start": DEFAULT_INDEX_START, "end": DEFAULT_INDEX_END}
        # 含「## 文件摘要表」的 index.md → 记录为摘要表候选（目录 → index 路径）
        if re.search(r"^## " + re.escape(SUMMARY_TABLE_TITLE) + r"\s*$", text, re.M):
            rel = idx.relative_to(root).as_posix()
            found["summary_tables"][idx.parent.relative_to(root).as_posix() if str(idx.parent.relative_to(root)) != "." else "."] = rel
    return found


def build_config_text(found, seeded=False):
    """根据扫描结果生成 config 文本（含注释示例；seeded=True 时来自 legacy 导出）。"""
    f = found
    lines = [
        "# ontology.config.yaml——本体注册表（G2 模板级，DEC-019；由 init_ontology.py init 生成）",
        "# 各节含义与迁移三步见 ontology/README.md（L5 适配契约）。全部可选，缺省走保守默认。",
        "",
    ]
    if f.get("doc_aliases") is not None:
        lines.append("# C1 文档别名：used_in.doc 别名 → 工程内路径（文件或目录）")
        if f["doc_aliases"]:
            lines.append("doc_aliases:")
            for k, v in f["doc_aliases"].items():
                lines.append(f"  {yaml_quote(k)}: {yaml_quote(v)}")
        else:
            lines.append("doc_aliases: {}")
        lines.append("")
    else:
        lines += [
            "# C1 文档别名：used_in.doc 别名 → 工程内路径（文件或目录）。ISS/DEC 编号无需注册。",
            "# 示例：",
            "# doc_aliases:",
            "#   '建议书v3.1': 'output/项目建议书-v3.1.md'",
            "doc_aliases: {}",
            "",
        ]
    if f.get("loc_grammar") is not None:
        lines.append("# C2 used_in.loc 定位语法：别名 → 正则片段列表（loc 为「/」分隔的锚点片段序列）")
        if f["loc_grammar"]:
            lines.append("loc_grammar:")
            for k, pats in f["loc_grammar"].items():
                lines.append(f"  {yaml_quote(k)}:")
                for p in pats:
                    lines.append(f"    - {yaml_quote(p)}")
        else:
            lines.append("loc_grammar: {}")
        lines.append("")
    else:
        lines += [
            "# C2 used_in.loc 定位语法：别名 → 正则片段列表。片段不匹配为 warning（不阻断）。",
            "# 示例：",
            "# loc_grammar:",
            "#   '建议书v3.1':",
            "#     - '^附录C第\\d+条(④)?$'",
            "#   '汇报PPT':",
            "#     - '^P\\d+(/P\\d+)*$'",
            "loc_grammar: {}",
            "",
        ]
    lines.append("# C3 摘要表 claim_ids 双写检查范围：目录 → 该目录 index.md（须含「## 文件摘要表」标题）")
    if f.get("summary_tables"):
        lines.append("summary_tables:")
        for k, v in f["summary_tables"].items():
            lines.append(f"  {yaml_quote(k)}: {yaml_quote(v)}")
    else:
        lines.append("summary_tables: {}")
    lines.append("")
    lines += [
        "# C4 枚举（属性名 id/predicate/value/caliber/status/subject/verify_depth/evidence/used_in 领域无关，不改）",
        "enums:",
        "  caliber: [written, self, disclosed, planned, visit, official]",
        "  status: [verified, self-reported, pending-cert, conflict, retired]",
        "  verify_depth: [transcribed, source_verified, passage_checked, value_recalculated]",
        "",
    ]
    lines += [
        "# C5 治理目录与编号 glob（可选；缺省即下列值；无此惯例的工程可改/留空关闭对应校验）",
        "governance:",
        f'  issues_dir: {f.get("issues_dir") or "issues"}',
        f'  decisions_dir: {f.get("decisions_dir") or "decisions"}',
        f'  issue_glob: "{f.get("issue_glob") or "ISS-*"}"',
        f'  dec_glob: "{f.get("dec_glob") or "DEC-*"}"',
        "",
    ]
    im = f.get("index_markers") or {"start": DEFAULT_INDEX_START, "end": DEFAULT_INDEX_END}
    lines += [
        "# C6 索引自动区块标记（可选；缺省即 project-index 标记）",
        "index_markers:",
        f"  start: {yaml_quote(im['start'])}",
        f"  end: {yaml_quote(im['end'])}",
        "",
    ]
    lines += [
        "# C7 摘要表表头（可选；缺省即下列中文表头）",
        "summary_table_headers:",
        f'  table_title: {SUMMARY_TABLE_TITLE}',
        "  file_col: 文件",
        "  claim_col: claim_ids",
        "  summary_col: 一句话摘要",
        "  sensitivity_col: 敏感度",
        "",
    ]
    lines.append("# C8 图主题分组：[主题名, [谓词...]]；空 = 全部落「其他」组（gen_graph.py 用）")
    if f.get("themes"):
        lines.append("themes:")
        for theme, preds in f["themes"]:
            pred_str = ", ".join(yaml_quote(p.strip("'\"")) for p in preds)
            lines.append(f"  - [{yaml_quote(theme)}, [{pred_str}]]")
        lines.append("")
    else:
        lines += [
            "# 示例：",
            "# themes:",
            "#   - ['资产与资质', ['罐容', '许可介质']]",
            "themes: []",
            "",
        ]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines) + "\n"


def cmd_init(args):
    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
    ontology_dir = root / "ontology"
    ontology_dir.mkdir(parents=True, exist_ok=True)
    target = ontology_dir / "ontology.config.yaml"
    if target.exists() and not args.force:
        print(f"config 已存在，不覆盖（--force 可强制重写）: {target}")
        return 0
    found = scan_discoverable(root)
    text = build_config_text(found)
    target.write_text(text, encoding="utf-8")
    print(f"已生成 config: {target}")
    print(f"  扫描发现：issues_dir={found['issues_dir']} decisions_dir={found['decisions_dir']} "
          f"issue_glob={found['issue_glob']} dec_glob={found['dec_glob']}")
    print(f"  index 区块标记：{'发现（缺省标记）' if found['index_markers'] else '未发现（写缺省值）'}")
    print(f"  摘要表候选：{found['summary_tables'] or '无'}")
    print("  语义项（doc_aliases/loc_grammar/themes）为空骨架＋注释示例；校验 warning 会引导补登。")
    return 0


# ---------------------------------------------------------------- export-legacy

TABLE_PATTERNS = {
    "DOC_ALIASES": re.compile(r"DOC_ALIASES\s*=\s*\{(.*?)\n\}", re.S),
    "LOC_GRAMMAR": re.compile(r"LOC_GRAMMAR\s*=\s*\{(.*?)\n\}", re.S),
    "SUMMARY_TABLES": re.compile(r"SUMMARY_TABLES\s*=\s*\{(.*?)\n\}", re.S),
    "ENUMS": re.compile(r"ENUMS\s*=\s*\{(.*?)\n\}", re.S),
    "THEMES": re.compile(r"THEMES\s*=\s*\[(.*?)\n\]", re.S),
}


def extract_dict_entries(body):
    """从 dict 字面量 body 提取 (key, value字符串) 序列。
    仅处理「"key": "value"」单行字符串键值形态（下游 DOC_ALIASES/SUMMARY_TABLES 即此形态），
    值内引号由正则捕获组自然排除，不重复加引号。"""
    entries = []
    for m in re.finditer(r'"([^"]+)"\s*:\s*"([^"]*)"', body):
        entries.append((m.group(1), m.group(2)))
    return entries


def extract_string_list(body):
    """从列表/集合字面量 body 提取字符串序列。"""
    return re.findall(r'"([^"]*)"', body)


def extract_loc_grammar(body):
    """LOC_GRAMMAR 值形如 "key": [r"...","...", ...]（可跨行，正则串内可能含 [一二三] 方括号）。
    按「"key": 锚点」切分块（下一处 "key": 或结尾），块内提取全部 r"..." 正则字符串，
    不依赖方括号配对。"""
    keys = list(re.finditer(r'"([^"]+)"\s*:', body))
    result = []
    for i, m in enumerate(keys):
        chunk_end = keys[i + 1].start() if i + 1 < len(keys) else len(body)
        chunk = body[m.end():chunk_end]
        pats = re.findall(r'r"([^"]*)"', chunk)
        if not pats:
            pats = re.findall(r"'([^']*)'", chunk)
        result.append((m.group(1), pats))
    return result


def yaml_quote(s):
    """YAML 单引号字符串（单引号内反斜杠无转义语义，正则往返无损）。"""
    return "'" + s.replace("'", "''") + "'"


def export_legacy(legacy_dir, out_path):
    legacy_dir = Path(legacy_dir)
    vc = legacy_dir / "validate_claims.py"
    gg = legacy_dir / "gen_graph.py"
    missing = [str(p) for p in (vc, gg) if not p.exists()]
    if missing:
        print(f"错误: 下游文件缺失: {missing}", file=sys.stderr)
        return 1
    vc_text = vc.read_text(encoding="utf-8")
    gg_text = gg.read_text(encoding="utf-8")
    sources = {"DOC_ALIASES": vc_text, "LOC_GRAMMAR": vc_text, "SUMMARY_TABLES": vc_text,
               "ENUMS": vc_text, "THEMES": gg_text}

    extracted = {}
    report = ["# legacy 五表导出报告（机械提取，无语义补全）", ""]
    for table, pat in TABLE_PATTERNS.items():
        m = pat.search(sources[table])
        if not m:
            report.append(f"- {table}: 未找到（提取 0 条）")
            extracted[table] = []
            continue
        body = m.group(1)
        if table == "THEMES":
            themes = []
            for tm in re.finditer(r'\(\s*"([^"]+)"\s*,\s*\[(.*?)\]\s*\)', body, re.S):
                themes.append((tm.group(1), extract_string_list(tm.group(2))))
            extracted[table] = themes
            report.append(f"- {table}: 提取 {len(themes)} 组")
            for name, preds in themes:
                report.append(f"    {name}: {len(preds)} 个谓词 {preds}")
        elif table == "ENUMS":
            enums = {}
            for em in re.finditer(r'"([^"]+)":\s*\{(.*?)\}', body, re.S):
                enums[em.group(1)] = extract_string_list(em.group(2))
            extracted[table] = enums
            report.append(f"- {table}: {len(enums)} 个枚举 " + "；".join(f"{k}={len(v)} 值" for k, v in enums.items()))
            for k, v in enums.items():
                report.append(f"    {k}: {v}")
        elif table == "LOC_GRAMMAR":
            entries = extract_loc_grammar(body)
            extracted[table] = entries
            report.append(f"- {table}: 提取 {len(entries)} 条")
            for k, pats in entries:
                report.append(f"    {k} → {len(pats)} 个正则 {pats}")
        else:
            entries = extract_dict_entries(body)
            extracted[table] = entries
            report.append(f"- {table}: 提取 {len(entries)} 条")
            for k, v in entries:
                report.append(f"    {k} → {v[:80]}")
    report.append("")

    # 转写为 config YAML
    lines = [
        "# ontology.config.yaml——由 init_ontology.py --export-legacy 从下游硬编码版机械导出（DEC-019/§12.5）",
        f"# 来源: {vc} / {gg}",
        "# 语义：五表条目一比一转写，未做任何语义补全；行为零漂移由 test_ontology.py 回归保证。",
        "",
        "# C1 文档别名",
        "doc_aliases:",
    ]
    for k, v in extracted["DOC_ALIASES"]:
        lines.append(f"  {yaml_quote(k)}: {yaml_quote(v)}")
    lines += ["", "# C2 loc 定位语法", "loc_grammar:"]
    for k, pats in extracted["LOC_GRAMMAR"]:
        lines.append(f"  {yaml_quote(k)}:")
        for p in pats:
            lines.append(f"    - {yaml_quote(p)}")
    lines += ["", "# C3 摘要表范围", "summary_tables:"]
    for k, v in extracted["SUMMARY_TABLES"]:
        lines.append(f"  {yaml_quote(k)}: {yaml_quote(v)}")
    lines += ["", "# C4 枚举", "enums:"]
    for k, vals in extracted["ENUMS"].items():
        lines.append(f"  {k}: [{', '.join(vals)}]")
    lines += ["", "# C8 图主题分组", "themes:"]
    for name, preds in extracted["THEMES"]:
        pred_str = ", ".join(yaml_quote(p) for p in preds)
        lines.append(f"  - [{yaml_quote(name)}, [{pred_str}]]")
    lines += ["", "# C5/C6/C7 使用保守默认（见 ontology/README.md），下游无对应硬编码差异。", ""]

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    report.append(f"已写出 config: {out_path}")
    print("\n".join(report))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", nargs="?", default=None, help="子命令：init")
    ap.add_argument("--export-legacy", action="store_true", help="从下游硬编码版导出五表为 config")
    ap.add_argument("--legacy-dir", help="下游 knowledge 目录（含 validate_claims.py / gen_graph.py）")
    ap.add_argument("--out", help="导出 config 输出路径（缺省 ontology/ontology.config.yaml）")
    ap.add_argument("--root", help="工程根（缺省=脚本上级目录）")
    ap.add_argument("--force", action="store_true", help="config 已存在时强制重写")
    args = ap.parse_args()

    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
    if args.export_legacy:
        if not args.legacy_dir:
            print("错误: --export-legacy 需要 --legacy-dir 指向下游 knowledge 目录", file=sys.stderr)
            return 2
        out = args.out or (root / "ontology" / "ontology.config.yaml")
        return export_legacy(args.legacy_dir, out)
    if args.command == "init":
        return cmd_init(args)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
