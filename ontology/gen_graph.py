#!/usr/bin/env python3
"""从 claims.yaml 生成 knowledge/graph.md（人读视图）

生成内容：口径速查表（按主题分组）、待核证清单、冲突对清单、红线谓词清单、证据文件→claim 反查表。
每次 claims.yaml 变更后运行；update_indexes.py 变更后建议重跑（registered_in 指向会变）。
主题分组（THEMES）从 ontology.config.yaml 的 themes 节读取（G2 config 化，DEC-019）；
缺省空主题 = 全部主张落「其他」组。STATUS_CN/CALIBER_CN 为领域无关显示层，保留内置（设计稿 §12.6）。
用法：python3 ontology/gen_graph.py [--root 工程根]
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config_loader import OntologyConfig, parse_config  # noqa: E402
from validate_claims import parse_claims, locate_config  # noqa: E402

STATUS_CN = {"verified": "✅已核实", "self-reported": "🗣自述", "pending-cert": "⏳待核证",
             "conflict": "⚔冲突待解", "retired": "🗄已废弃"}
CALIBER_CN = {"written": "书面", "self": "自述", "disclosed": "介绍会披露",
              "planned": "规划", "visit": "参访", "official": "官网/公告"}


def load_themes(root, config_arg=None):
    """themes（C8）：[主题, [谓词...]] 列表；config 缺失或无 themes 节时返回空列表。"""
    cfg_path = locate_config(root, config_arg)
    if cfg_path is None or not Path(cfg_path).exists():
        return []
    config = OntologyConfig(parse_config(Path(cfg_path).read_text(encoding="utf-8")))
    return config.themes or []


def main():
    ap = argparse.ArgumentParser(add_help=True, description="从 claims.yaml 生成 graph.md")
    ap.add_argument("--root", help="工程根（缺省=脚本上级目录）")
    ap.add_argument("--config", help="ontology.config.yaml 路径（缺省按三级顺序定位）")
    args, _unknown = ap.parse_known_args()

    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
    themes = load_themes(root, args.config)
    claims_path = root / "knowledge" / "claims.yaml"
    out_path = root / "knowledge" / "graph.md"

    text = claims_path.read_text(encoding="utf-8")
    claims = parse_claims(text)
    by_id = {c["id"]: c for c in claims}

    lines = ["# 口径主张图（自动生成，勿手改）",
             "",
             f"> 由 ontology/gen_graph.py 从 claims.yaml（{len(claims)} 条）生成；claims.yaml 变更后重跑。",
             "> 溯源路径：本表 → claims.yaml 证据定位 → 原文件（SHA 见各目录 index.md）。修改主张请编辑 claims.yaml。",
             ""]

    # 分组速查表
    assigned = set()
    for theme, preds in themes:
        rows = [c for c in claims if c["predicate"] in preds and c["id"] not in assigned]
        if not rows:
            continue
        assigned |= {c["id"] for c in rows}
        lines += [f"## {theme}", "", "| id | 谓词 | 值 | 口径 | 状态 | 主体 | 引用位置 |", "|---|---|---|---|---|---|---|"]
        for c in rows:
            used = "；".join(f"{u['doc']}::{u['loc']}" for u in c.get("used_in", [])[:3])
            conflict_mark = " ⚔" if c.get("conflicts_with") else ""
            lines.append(f"| {c['id']}{conflict_mark} | {c['predicate']} | {c['value'][:60]} | "
                         f"{CALIBER_CN.get(c['caliber'], c['caliber'])} | {STATUS_CN.get(c['status'], c['status'])} | "
                         f"{c['subject']} | {used[:80]} |")
        lines.append("")

    leftover = [c for c in claims if c["id"] not in assigned]
    if leftover:
        lines += ["## 其他", "", "| id | 谓词 | 值 | 状态 |", "|---|---|---|---|"]
        for c in leftover:
            lines.append(f"| {c['id']} | {c['predicate']} | {c['value'][:60]} | {STATUS_CN.get(c['status'], c['status'])} |")
        lines.append("")

    # 待核证
    pend = [c for c in claims if c.get("status") == "pending-cert"]
    lines += [f"## 待企业核证（{len(pend)} 条）", ""]
    for c in pend:
        tr = "、".join(c.get("tracked_by", [])) or "—"
        lines.append(f"- **{c['id']}** {c['predicate']}={c['value']}（跟踪：{tr}）")
    lines.append("")

    # 冲突对
    seen = set()
    pairs = []
    for c in claims:
        for o in c.get("conflicts_with", []):
            key = tuple(sorted([c["id"], o]))
            if key not in seen:
                seen.add(key)
                pairs.append(key)
    lines += [f"## 冲突对（{len(pairs)} 对）", ""]
    for a, b in pairs:
        ca, cb = by_id.get(a, {}), by_id.get(b, {})
        lines.append(f"- **{a} ⇄ {b}**：{ca.get('predicate','?')}（{ca.get('value','?')} vs {cb.get('value','?')}）")
    lines.append("")

    # 红线
    reds = [c for c in claims if any(x.startswith("DEC") for x in c.get("tracked_by", []))]
    lines += [f"## 红线谓词（{len(reds)} 条，受 DEC 约束）", ""]
    for c in reds:
        lines.append(f"- **{c['id']}** {c['value']} — {c.get('notes','')}")
    lines.append("")

    # 证据反查
    lines += ["## 证据文件 → claim 反查", ""]
    ev_map = {}
    for c in claims:
        for ev in c.get("evidence", []):
            ev_map.setdefault(ev["file"], []).append(c["id"])
    for f in sorted(ev_map):
        mark = "（未归档来源）" if f.startswith("unarchived:") else ""
        lines.append(f"- `{f}`{mark} → {'、'.join(ev_map[f])}")
    lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"graph.md 已生成：{len(claims)} 条主张、{len(pairs)} 对冲突、{len(pend)} 条待核证")


if __name__ == "__main__":
    main()
