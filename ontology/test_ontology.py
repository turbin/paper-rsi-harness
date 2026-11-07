#!/usr/bin/env python3
"""ontology/test_ontology.py——G2 模板资产回归测试（stdlib unittest）

用例覆盖：轻量 YAML 解析（嵌套/flow/注释边界）、config 加载与保守默认、missing config 自动生成、
--export-legacy 对下游真实文件提取正确性（下游文件缺失时 skipTest）、doc_aliases 未注册警告、
枚举外置生效、claims 解析 0 条 error、通配路径 error、unarchived 警告、conflicts_with 单向
warning/不存在 error、summary_tables 行匹配（含「—」行）、documents.yaml 页数锚、pptx 页数不符
error、init 幂等、graph.md 与下游字节级对照（THEMES 注入下游值）。
测试全部在临时目录构造微型工程，不污染真实工程；下游工程只读。
运行：python3 ontology/test_ontology.py
"""
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ONTOLOGY_DIR = Path(__file__).resolve().parent
ROOT = ONTOLOGY_DIR.parent
sys.path.insert(0, str(ONTOLOGY_DIR))

from config_loader import OntologyConfig, parse_config  # noqa: E402
import validate_claims as vc  # noqa: E402
import init_ontology as io_mod  # noqa: E402

LEGACY_KNOWLEDGE = Path("/Users/yanbin/Workspace/repo-workspace/mba-bdp-优月仓储/knowledge")
LEGACY_ROOT = LEGACY_KNOWLEDGE.parent


def make_project(tmp):
    """构造微型工程骨架：ontology 脚本副本 + knowledge 目录。"""
    root = Path(tmp) / "proj"
    (root / "ontology").mkdir(parents=True)
    (root / "knowledge").mkdir(parents=True)
    (root / "issues").mkdir()
    (root / "decisions").mkdir()
    for f in ("validate_claims.py", "gen_graph.py", "init_ontology.py", "config_loader.py"):
        shutil.copy(ONTOLOGY_DIR / f, root / "ontology" / f)
    return root


def write_claims(root, body):
    (root / "knowledge" / "claims.yaml").write_text("claims:\n" + body, encoding="utf-8")


def write_config(root, text):
    (root / "ontology" / "ontology.config.yaml").write_text(text, encoding="utf-8")


def run_validator(root, *extra):
    return subprocess.run(
        [sys.executable, str(root / "ontology" / "validate_claims.py"), "--root", str(root), *extra],
        capture_output=True, text=True, cwd=str(root))


DEFAULT_CONFIG = """\
doc_aliases:
  '报告v1': 'output/报告-v1.md'
loc_grammar:
  '报告v1':
    - '^第\\d+节$'
  '简报':
    - '^P\\d+$'
summary_tables:
  'materials/docs': 'materials/docs/index.md'
enums:
  caliber: [written, self, disclosed, planned, visit, official]
  status: [verified, self-reported, pending-cert, conflict, retired]
  verify_depth: [transcribed, source_verified, passage_checked, value_recalculated]
themes:
  - ['资产', ['罐容']]
  - ['角色', ['角色']]
"""


def make_claim(cid="CLM-001", *, predicate="罐容", value="10万m³", caliber="written",
               status="verified", subject="主体A", verify_depth="passage_checked",
               evidence="- file: materials/docs/资料A.pdf\n        locator: 第2页",
               used_in="- {doc: 报告v1, loc: 第3节}", extra=""):
    return (f"  - id: {cid}\n    predicate: {predicate}\n    value: {value}\n"
            f"    caliber: {caliber}\n    status: {status}\n    subject: {subject}\n"
            f"    verify_depth: {verify_depth}\n    evidence:\n      {evidence}\n"
            f"    used_in:\n      {used_in}\n{extra}\n")


def seed_project(root):
    """带索引/摘要表/文档版本的最小全绿工程。"""
    write_config(root, DEFAULT_CONFIG)
    (root / "materials" / "docs").mkdir(parents=True)
    (root / "materials" / "docs" / "资料A.pdf").write_text("x", encoding="utf-8")
    (root / "materials" / "docs" / "index.md").write_text(
        "# 索引\n\n## 文件摘要表\n\n| 文件 | 类型 | 一句话摘要 | 敏感度 | claim_ids |\n|---|---|---|---|---|\n"
        "| 资料A.pdf | pdf | 摘要内容 | 内部 | CLM-001 |\n"
        "| 占位文件.pdf | pdf | — | 内部 | — |\n\n"
        "<!-- project-index:start -->\n### 文件快照\n\n| 文件 | 变更观察时间（UTC） | SHA-256 |\n|---|---|---|\n"
        "| 资料A.pdf | 2026-01-01T00:00:00+00:00 | `abc` |\n<!-- project-index:end -->\n", encoding="utf-8")
    (root / "output").mkdir()
    (root / "output" / "报告-v1.md").write_text("# 报告\n", encoding="utf-8")
    write_claims(root, make_claim())


class TestParseConfig(unittest.TestCase):
    def test_flat_and_nested(self):
        cfg = parse_config(
            "doc_aliases:\n  'a': 'x.md'\n  b: y\nenums:\n  caliber: [written, self]\n")
        self.assertEqual(cfg["doc_aliases"], {"a": "x.md", "b": "y"})
        self.assertEqual(cfg["enums"]["caliber"], ["written", "self"])

    def test_flow_nested_list(self):
        cfg = parse_config("themes:\n  - ['资产', ['罐容', '介质']]\n  - ['角色', ['角色']]\n")
        self.assertEqual(cfg["themes"], [["资产", ["罐容", "介质"]], ["角色", ["角色"]]])

    def test_flow_inline(self):
        cfg = parse_config("a: [1, 2, 3]\nb: {k1: v1, k2: v2}\n")
        self.assertEqual(cfg["a"], ["1", "2", "3"])
        self.assertEqual(cfg["b"], {"k1": "v1", "k2": "v2"})

    def test_comments_and_quotes(self):
        cfg = parse_config("# 顶注\nkey: 'v # 不是注释'\n# 行注\nk2: 值2\n")
        self.assertEqual(cfg["key"], "v # 不是注释")
        self.assertEqual(cfg["k2"], "值2")

    def test_list_of_regex_with_brackets(self):
        cfg = parse_config("loc_grammar:\n  'doc':\n    - '^矛盾[一二三]$'\n    - '^P\\d+$'\n")
        self.assertEqual(cfg["loc_grammar"]["doc"], ["^矛盾[一二三]$", "^P\\d+$"])

    def test_summary_tables_two_writes(self):
        nested = parse_config("summary_tables:\n  'dirA': 'dirA/index.md'\n")
        listed = parse_config("summary_tables:\n  - 'dirA': 'dirA/index.md'\n")
        self.assertEqual(OntologyConfig(nested).summary_tables,
                         OntologyConfig(listed).summary_tables)

    def test_empty_flow_list(self):
        cfg = parse_config("themes: []\n")
        self.assertEqual(cfg["themes"], [])


class TestConfigDefaults(unittest.TestCase):
    def test_missing_sections_defaults_and_warnings(self):
        c = OntologyConfig(parse_config("themes:\n  - ['t', ['p']]\n"))
        self.assertEqual(c.doc_aliases, None)
        self.assertEqual(c.enums["caliber"], ["written", "self", "disclosed", "planned", "visit", "official"])
        self.assertEqual(c.enums["status"], ["verified", "self-reported", "pending-cert", "conflict", "retired"])
        self.assertEqual(c.enums["verify_depth"], ["transcribed", "source_verified", "passage_checked", "value_recalculated"])
        self.assertTrue(any("enums" in w for w in c.warnings))
        self.assertEqual(c.index_start, "<!-- project-index:start -->")
        self.assertEqual(c.table_headers["claim_col"], "claim_ids")

    def test_custom_markers_and_headers(self):
        c = OntologyConfig(parse_config(
            "index_markers:\n  start: '<!-- IDX:A -->'\n  end: '<!-- IDX:B -->'\n"
            "summary_table_headers:\n  claim_col: claims\n"))
        self.assertEqual(c.index_start, "<!-- IDX:A -->")
        self.assertEqual(c.table_headers["claim_col"], "claims")
        self.assertEqual(c.table_headers["file_col"], "文件")  # 未覆盖项保持缺省


class TestMissingConfigAutoGenerate(unittest.TestCase):
    def test_auto_generate_and_second_run_stable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_project(tmp)
            (root / "materials" / "docs").mkdir(parents=True)
            (root / "materials" / "docs" / "资料A.pdf").write_text("x", encoding="utf-8")
            write_claims(root, make_claim())
            r1 = run_validator(root)
            self.assertEqual(r1.returncode, 0, r1.stderr + r1.stdout)
            cfg_path = root / "knowledge" / "ontology.config.yaml"
            self.assertTrue(cfg_path.exists())
            self.assertIn("doc_aliases: {}", cfg_path.read_text(encoding="utf-8"))
            self.assertIn("提示", r1.stderr)
            # 第二跑不再生成（幂等），claims 引用未注册别名触发 warning
            r2 = run_validator(root)
            self.assertEqual(r2.returncode, 0)
            self.assertNotIn("生成骨架", r2.stderr)


class TestExportLegacy(unittest.TestCase):
    """--export-legacy 对下游真实文件的提取正确性（下游缺失时 skip）。"""

    def setUp(self):
        if not LEGACY_KNOWLEDGE.exists():
            self.skipTest(f"下游工程不存在: {LEGACY_KNOWLEDGE}")

    def test_five_tables_extracted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_project(tmp)
            out = root / "ontology" / "ontology.config.yaml"
            rc = io_mod.main.__wrapped__ if hasattr(io_mod.main, "__wrapped__") else None
            # 直接走 CLI 入口
            proc = subprocess.run(
                [sys.executable, str(root / "ontology" / "init_ontology.py"),
                 "--export-legacy", "--legacy-dir", str(LEGACY_KNOWLEDGE), "--out", str(out)],
                capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            text = out.read_text(encoding="utf-8")
            cfg = OntologyConfig(parse_config(text))
            # DOC_ALIASES 2 条
            self.assertEqual(cfg.doc_aliases, {
                "建议书v3.1": "output/组名柒棱镜-项目建议书-20261102-v3.1.md",
                "汇报PPT-20261102": "output/柒棱镜-项目建议书汇报PPT-20261102"})
            # LOC_GRAMMAR 2 键 4 正则（含方括号语义项）
            self.assertEqual(set(cfg.loc_grammar), {"建议书v3.1", "汇报PPT-20261102"})
            self.assertEqual(len(cfg.loc_grammar["建议书v3.1"]), 3)
            self.assertEqual(len(cfg.loc_grammar["汇报PPT-20261102"]), 1)
            self.assertIn("矛盾[一二三]", cfg.loc_grammar["建议书v3.1"][2])
            # SUMMARY_TABLES 1 条
            self.assertEqual(cfg.summary_tables, {
                "materials/company/需求资料-2026-10": "materials/company/需求资料-2026-10/index.md"})
            # ENUMS 3 枚举 6/5/4 值
            self.assertEqual(len(cfg.enums["caliber"]), 6)
            self.assertEqual(len(cfg.enums["status"]), 5)
            self.assertEqual(len(cfg.enums["verify_depth"]), 4)
            # THEMES 10 组，谓词总数 29
            self.assertEqual(len(cfg.themes), 10)
            total_preds = sum(len(p) for _, p in cfg.themes)
            self.assertEqual(total_preds, 29)
            self.assertEqual(cfg.themes[0], ("资产与资质", ["罐容", "许可介质", "许可外介质提及", "固体库面积"]))

    def test_regex_patterns_match(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_project(tmp)
            out = root / "ontology" / "ontology.config.yaml"
            subprocess.run(
                [sys.executable, str(root / "ontology" / "init_ontology.py"),
                 "--export-legacy", "--legacy-dir", str(LEGACY_KNOWLEDGE), "--out", str(out)],
                capture_output=True, text=True, check=True)
            cfg = OntologyConfig(parse_config(out.read_text(encoding="utf-8")))
            pats = cfg.loc_grammar["建议书v3.1"]
            self.assertTrue(any(re.match(p, "附录C第8条") for p in pats))
            self.assertTrue(any(re.match(p, "表1-3") for p in pats))
            self.assertTrue(any(re.match(p, "微观画像节") for p in pats))
            deck = cfg.loc_grammar["汇报PPT-20261102"]
            self.assertTrue(any(re.match(p, "P4") for p in deck))
            self.assertFalse(any(re.match(p, "随便写") for p in pats + deck))


class TestValidatorWarnings(unittest.TestCase):
    def _seed(self, tmp):
        root = make_project(tmp)
        seed_project(root)
        return root

    def test_unregistered_doc_alias_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._seed(tmp)
            write_claims(root, make_claim(used_in="- {doc: 未注册文档, loc: 随意}"))
            r = run_validator(root)
            self.assertEqual(r.returncode, 0)
            self.assertIn("used_in.doc「未注册文档」未注册（加入 config doc_aliases 或改用 ISS/DEC 编号）", r.stdout)

    def test_enum_externalized(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._seed(tmp)
            write_claims(root, make_claim(caliber="口头"))
            r = run_validator(root)
            self.assertEqual(r.returncode, 1)
            self.assertIn("不在枚举", r.stdout)
            # 外置生效：config 中加「口头」后不再报
            cfg = (root / "ontology" / "ontology.config.yaml").read_text(encoding="utf-8")
            cfg = cfg.replace("caliber: [written, self, disclosed, planned, visit, official]",
                              "caliber: [written, self, disclosed, planned, visit, official, 口头]")
            write_config(root, cfg)
            r2 = run_validator(root)
            self.assertEqual(r2.returncode, 0, r2.stdout)

    def test_zero_claims_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._seed(tmp)
            write_claims(root, "")
            r = run_validator(root)
            self.assertEqual(r.returncode, 1)
            self.assertIn("claims.yaml 未解析到任何条目", r.stdout)

    def test_wildcard_path_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._seed(tmp)
            write_claims(root, make_claim(evidence="- file: references/REF-01*\n        locator: 通配"))
            r = run_validator(root)
            self.assertEqual(r.returncode, 1)
            self.assertIn("通配证据路径已废除（v1.3.1）", r.stdout)

    def test_unarchived_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._seed(tmp)
            write_claims(root, make_claim(evidence="- file: unarchived:企业官网\n        locator: 官网页面"))
            r = run_validator(root)
            self.assertEqual(r.returncode, 0)
            self.assertIn("证据「unarchived:企业官网」为未归档来源", r.stdout)

    def test_conflicts_unilateral_and_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._seed(tmp)
            write_claims(root,
                         make_claim("CLM-001", extra="    conflicts_with: [CLM-002]")
                         + make_claim("CLM-002", extra="    conflicts_with: [CLM-099]"))
            r = run_validator(root)
            self.assertEqual(r.returncode, 1)
            self.assertIn("CLM-001 ⇄ CLM-002: 冲突边单向（对方未回指）", r.stdout)
            self.assertIn("CLM-002: conflicts_with 指向不存在的 CLM-099", r.stdout)

    def test_summary_table_row_matching_and_dash(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._seed(tmp)
            # 「—」行不产生任何报警（占位行），claim 文件行双向一致
            r = run_validator(root)
            self.assertEqual(r.returncode, 0, r.stdout)
            self.assertNotIn("摘要表", r.stdout)
            # 反向：claim_ids 多登
            idx = root / "materials" / "docs" / "index.md"
            idx.write_text(idx.read_text(encoding="utf-8").replace("| 占位文件.pdf | pdf | — | 内部 | — |",
                                                                   "| 占位文件.pdf | pdf | — | 内部 | CLM-001 |"), encoding="utf-8")
            r2 = run_validator(root)
            self.assertIn("的 evidence 不含「占位文件.pdf」", r2.stdout)

    def test_missing_evidence_file_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._seed(tmp)
            write_claims(root, make_claim(evidence="- file: materials/docs/不存在.pdf\n        locator: x"))
            r = run_validator(root)
            self.assertEqual(r.returncode, 1)
            self.assertIn("证据文件不存在: materials/docs/不存在.pdf", r.stdout)


class TestDocumentsYaml(unittest.TestCase):
    def _seed(self, tmp):
        root = make_project(tmp)
        seed_project(root)
        return root

    def test_derived_from_missing_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._seed(tmp)
            (root / "knowledge" / "documents.yaml").write_text(
                "documents:\n  - id: 报告v2\n    type: doc\n    file: output/报告-v2.md\n"
                "    derived_from: 报告v0\n    supersedes: 无\n", encoding="utf-8")
            r = run_validator(root)
            self.assertEqual(r.returncode, 1)
            self.assertIn("报告v2: derived_from 指向不存在条目或路径: 报告v0", r.stdout)

    def test_pptx_pages_anchor(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._seed(tmp)
            # 造一个 2 页 pptx（zip 内 slide xml 计数）
            pptx = root / "output" / "deck.pptx"
            with zipfile.ZipFile(pptx, "w") as z:
                z.writestr("ppt/slides/slide1.xml", "<s/>")
                z.writestr("ppt/slides/slide2.xml", "<s/>")
                z.writestr("[Content_Types].xml", "<x/>")
            (root / "knowledge" / "documents.yaml").write_text(
                "documents:\n  - id: 汇报PPT\n    type: deck\n    file: output/deck.pptx\n"
                "    derived_from: 无\n    supersedes: 无\n    pages_expected: 3\n", encoding="utf-8")
            r = run_validator(root)
            self.assertEqual(r.returncode, 1)
            self.assertIn("pptx 实际 2 页 ≠ pages_expected 3", r.stdout)
            # 页数一致时通过
            (root / "knowledge" / "documents.yaml").write_text(
                (root / "knowledge" / "documents.yaml").read_text(encoding="utf-8").replace("pages_expected: 3", "pages_expected: 2"),
                encoding="utf-8")
            r2 = run_validator(root)
            self.assertEqual(r2.returncode, 0, r2.stdout)


class TestLocGrammar(unittest.TestCase):
    def test_pattern_mismatch_warning_from_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_project(tmp)
            seed_project(root)
            write_claims(root, make_claim(used_in="- {doc: 简报, loc: 第3节}"))
            cfg = (root / "ontology" / "ontology.config.yaml").read_text(encoding="utf-8")
            cfg = cfg.replace("  '简报':\n    - '^P\\d+$'", "  '简报':\n    - '^P\\d+$'")
            write_config(root, cfg + "\n")
            r = run_validator(root)
            self.assertEqual(r.returncode, 0)
            self.assertIn("used_in.loc 片段「第3节」不符合「简报」定位语法（loc_grammar）", r.stdout)


class TestInitIdempotent(unittest.TestCase):
    def test_init_fresh_and_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_project(tmp)
            (root / "issues" / "ISS-001-x.md").write_text("x", encoding="utf-8")
            (root / "decisions" / "DEC-001-x.md").write_text("x", encoding="utf-8")
            (root / "index.md").write_text(
                "# r\n\n<!-- project-index:start -->\n| f | 2026-01-01T00:00:00+00:00 | x |\n<!-- project-index:end -->\n",
                encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(root / "ontology" / "init_ontology.py"), "init", "--root", str(root)],
                capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            cfg_path = root / "ontology" / "ontology.config.yaml"
            self.assertTrue(cfg_path.exists())
            text1 = cfg_path.read_text(encoding="utf-8")
            # 幂等：再跑不覆盖
            proc2 = subprocess.run(
                [sys.executable, str(root / "ontology" / "init_ontology.py"), "init", "--root", str(root)],
                capture_output=True, text=True)
            self.assertIn("不覆盖", proc2.stdout)
            self.assertEqual(cfg_path.read_text(encoding="utf-8"), text1)
            # --force 重写成功
            proc3 = subprocess.run(
                [sys.executable, str(root / "ontology" / "init_ontology.py"), "init", "--root", str(root), "--force"],
                capture_output=True, text=True)
            self.assertEqual(proc3.returncode, 0)
            # 解析生成的 config 无异常且枚举齐全
            c = OntologyConfig(parse_config(cfg_path.read_text(encoding="utf-8")))
            self.assertIn("caliber", c.enums)

    def test_init_detects_summary_table(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_project(tmp)
            d = root / "materials" / "docs"
            d.mkdir(parents=True)
            (d / "index.md").write_text("# i\n\n## 文件摘要表\n\n| 文件 | claim_ids |\n|---|---|\n", encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(root / "ontology" / "init_ontology.py"), "init", "--root", str(root), "--force"],
                capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0)
            text = (root / "ontology" / "ontology.config.yaml").read_text(encoding="utf-8")
            self.assertIn("'materials/docs': 'materials/docs/index.md'", text)


class TestZeroDriftAgainstLegacy(unittest.TestCase):
    """下游子集回归：同一 claims 输入下，上游 config 化版与下游硬编码版报警逐条一致。"""

    def setUp(self):
        if not LEGACY_KNOWLEDGE.exists():
            self.skipTest(f"下游工程不存在: {LEGACY_KNOWLEDGE}")

    def test_graph_md_byte_identical(self):
        """THEMES 经 --export-legacy 注入后，对下游 claims.yaml 生成的 graph.md 字节级一致
        （known-diff 3：头部来源行 knowledge/→ontology/ 除外）。"""
        with tempfile.TemporaryDirectory() as tmp:
            root = make_project(tmp)
            out = root / "ontology" / "ontology.config.yaml"
            subprocess.run(
                [sys.executable, str(root / "ontology" / "init_ontology.py"),
                 "--export-legacy", "--legacy-dir", str(LEGACY_KNOWLEDGE), "--out", str(out)],
                capture_output=True, text=True, check=True)
            shutil.copy(LEGACY_KNOWLEDGE / "claims.yaml", root / "knowledge" / "claims.yaml")
            gen = subprocess.run(
                [sys.executable, str(root / "ontology" / "gen_graph.py"), "--root", str(root)],
                capture_output=True, text=True)
            self.assertEqual(gen.returncode, 0, gen.stderr)
            produced = (root / "knowledge" / "graph.md").read_text(encoding="utf-8")
            baseline = (LEGACY_KNOWLEDGE / "graph.md").read_text(encoding="utf-8")
            norm = lambda t: t.replace("由 ontology/gen_graph.py", "由 knowledge/gen_graph.py")
            self.assertEqual(norm(produced), baseline)

    def test_validator_subset_claims_identical(self):
        """取下游 claims.yaml 中引用别名/语法/摘要表/冲突边的代表性子集，逐条对照报警。"""
        legacy_text = (LEGACY_KNOWLEDGE / "claims.yaml").read_text(encoding="utf-8")
        # 子集：CLM-001/002（冲突+unarchived+别名）、CLM-004（对照项 loc 语法）、CLM-030（index.md 证据+摘要表反向）
        wanted = ["CLM-001", "CLM-002", "CLM-004", "CLM-030"]
        blocks = re.findall(r"(  - id: (?:%s)\b.*?)(?=\n  - id:|\Z)" % "|".join(wanted),
                            legacy_text, re.S)
        self.assertEqual(len(blocks), 4)
        with tempfile.TemporaryDirectory() as tmp:
            root = make_project(tmp)
            out = root / "ontology" / "ontology.config.yaml"
            subprocess.run(
                [sys.executable, str(root / "ontology" / "init_ontology.py"),
                 "--export-legacy", "--legacy-dir", str(LEGACY_KNOWLEDGE), "--out", str(out)],
                capture_output=True, text=True, check=True)
            write_claims(root, "\n".join(b.rstrip() for b in blocks) + "\n")
            # 摘要表：下游真实 index 的表结构无法拷入（跨工程路径不同），
            # 用最小同构表替代并保留 claim_ids 反向一致的行语义
            (root / "materials" / "需求资料-2026-10").mkdir(parents=True)
            (root / "materials" / "需求资料-2026-10" / "index.md").write_text(
                "# i\n\n## 文件摘要表\n\n| 文件 | 类型 | 一句话摘要 | 敏感度 | claim_ids |\n|---|---|---|---|---|\n"
                "| 需求7-客户参观交流与行业来访记录-总结性汇报.docx | docx | 资产底册 | 内部 | CLM-001 |\n"
                "| index.md | md | 表载体 | 内部 | — |\n\n", encoding="utf-8")
            r_up = run_validator(root)
            # 下游硬编码版跑同子集：拷 claims 子集进下游副本工程（只读下游源文件，用其脚本拷贝）
            down_root = Path(tmp) / "down"
            (down_root / "knowledge").mkdir(parents=True)
            (down_root / "issues").mkdir()
            (down_root / "decisions").mkdir()
            (down_root / "materials" / "需求资料-2026-10").mkdir(parents=True)
            shutil.copy(LEGACY_KNOWLEDGE / "validate_claims.py", down_root / "knowledge" / "validate_claims.py")
            shutil.copy(LEGACY_KNOWLEDGE / "gen_graph.py", down_root / "knowledge" / "gen_graph.py")
            (down_root / "knowledge" / "claims.yaml").write_text("claims:\n" + "\n".join(b.rstrip() for b in blocks) + "\n", encoding="utf-8")
            (down_root / "materials" / "需求资料-2026-10" / "index.md").write_text(
                (root / "materials" / "需求资料-2026-10" / "index.md").read_text(encoding="utf-8"), encoding="utf-8")
            r_down = subprocess.run(
                [sys.executable, str(down_root / "knowledge" / "validate_claims.py")],
                capture_output=True, text=True, cwd=str(down_root))
            # 对照：去掉路径性差异（证据文件在两个工程都不存在 → error 相同）后逐行比较 stdout
            up_lines = [l for l in r_up.stdout.splitlines() if l.strip()]
            down_lines = [l for l in r_down.stdout.splitlines() if l.strip()]
            self.assertEqual(r_up.returncode, r_down.returncode)
            self.assertEqual(len(up_lines), len(down_lines))
            for u, d in zip(up_lines, down_lines):
                self.assertEqual(u, d)


class TestEncodingSelfCheck(unittest.TestCase):
    def test_all_new_files_utf8_no_bom_lf(self):
        for p in ONTOLOGY_DIR.rglob("*"):
            if not p.is_file() or p.name == "__pycache__" or "__pycache__" in p.parts:
                continue
            raw = p.read_bytes()
            self.assertFalse(raw.startswith(b"\xef\xbb\xbf"), f"BOM found: {p.name}")
            self.assertNotIn(b"\r\n", raw, f"CRLF found: {p.name}")
            raw.decode("utf-8")


if __name__ == "__main__":
    unittest.main(verbosity=2)
