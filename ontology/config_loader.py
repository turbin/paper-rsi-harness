# ontology/config_loader.py——轻量 YAML 解析与 ontology.config.yaml 加载（G2 模板级改造，DEC-019/DEC-022）
#
# stdlib-only（无 PyYAML），Python 3.10+。config 结构与保守默认见 ontology/README.md（L5 适配契约）。
# 顶层节：doc_aliases / loc_grammar / summary_tables / enums / governance / index_markers /
#         summary_table_headers / themes。全部可选，缺省走保守默认并由校验器 warning 引导补登。
# summary_tables 值为两级嵌套映射（目录 → index 路径），解析器支持该形态；也可写成
# 「- 目录：index 路径」列表行，两种写法等价（init_ontology.py 生成列表行写法，README 有说明）。

import re
from pathlib import Path

# 缺省 index 区块标记（C6；可被 config 的 index_markers 节覆盖）
DEFAULT_INDEX_START = "<!-- project-index:start -->"
DEFAULT_INDEX_END = "<!-- project-index:end -->"


def parse_scalar(v):
    v = v.strip()
    if not v:
        return ""
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        return v[1:-1]
    return v


def _split_flow_items(inner):
    """按顶层逗号切分行内集合内容，尊重引号与方括号嵌套。"""
    items, buf, depth, quote = [], "", 0, None
    for ch in inner:
        if quote:
            buf += ch
            if ch == quote:
                quote = None
            continue
        if ch in "\"'":
            quote = ch
            buf += ch
            continue
        if ch == "[":
            depth += 1
            buf += ch
            continue
        if ch == "]":
            depth -= 1
            buf += ch
            continue
        if ch == "," and depth == 0:
            items.append(buf.strip())
            buf = ""
            continue
        buf += ch
    if buf.strip():
        items.append(buf.strip())
    return [x for x in items if x.strip()]


def parse_flow(v):
    """行内值解析：[...]（支持一层以上嵌套子列表）、{k: v, ...}、标量。"""
    v = v.strip()
    if v.startswith("[") and v.endswith("]"):
        return [parse_flow(x) for x in _split_flow_items(v[1:-1])]
    if v.startswith("{") and v.endswith("}"):
        d = {}
        for part in _split_flow_items(v[1:-1]):
            pm = re.match(r"([^:：]+)[:：]\s*(.*)$", part.strip())
            if pm:
                d[parse_scalar(pm.group(1))] = parse_flow(pm.group(2))
        return d
    return parse_scalar(v)


# 兼容旧名
def parse_flow_list(v):
    return parse_flow(v) if (v.strip().startswith("[") and v.strip().endswith("]")) else [parse_scalar(v)]


def parse_config(text):
    """ontology.config.yaml 轻量解析。

    支持：顶层 key: 节、两级嵌套 key:/key:/value、列表行（- 项 或 - k: v）、
    行内 flow（含嵌套子列表，如 themes 行）、行内 flow 映射、# 注释行、引号值。
    「key:」（空值）后既可跟嵌套映射也可跟列表项（如 loc_grammar 的正则列表）。
    不支持：多行块标量、>2 级嵌套映射、锚点/别名——书写规范见 ontology/README.md。
    """
    root = {}
    # 栈帧：[indent, obj, parent, key_in_parent]；root 帧无 parent
    stack = [[-1, root, None, None]]
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        s = line.strip()
        # 列表项
        if s.startswith("- "):
            item = s[2:].strip()
            while len(stack) > 1 and stack[-1][0] >= indent:
                stack.pop()
            frame = stack[-1]
            obj = frame[1]
            # 帧本身是空占位 dict（key: 后直接跟列表项，如 themes:）→ 就地转列表
            if isinstance(obj, dict) and not obj and frame[2] is not None:
                lst = []
                frame[2][frame[3]] = lst
                frame[1] = lst
                obj = lst
            if isinstance(obj, list):
                if item.startswith("[") or item.startswith("{"):
                    obj.append(parse_flow(item))
                else:
                    fm = re.match(r"([^:：]+)[:：]\s*(.*)$", item)
                    if fm:
                        obj.append([parse_scalar(fm.group(1)), parse_flow(fm.group(2))])
                    else:
                        obj.append(parse_scalar(item))
                continue
            if isinstance(obj, dict):
                # 挂在最近一个空占位 key 上（None 或空 dict 占位）
                holder = None
                for k in reversed(list(obj.keys())):
                    v = obj[k]
                    if v is None or (isinstance(v, dict) and not v):
                        holder = k
                        break
                if holder is None:
                    continue
                old = obj[holder]
                lst = old if isinstance(old, list) else []
                if item.startswith("[") or item.startswith("{"):
                    lst.append(parse_flow(item))
                else:
                    fm = re.match(r"([^:：]+)[:：]\s*(.*)$", item)
                    if fm:
                        lst.append([parse_scalar(fm.group(1)), parse_flow(fm.group(2))])
                    else:
                        lst.append(parse_scalar(item))
                obj[holder] = lst
            continue
        # key: value（或嵌套节头）
        m = re.match(r"([^:：]+)[:：]\s*(.*)$", s)
        if not m:
            continue
        key = parse_scalar(m.group(1))
        val = m.group(2).strip()
        while len(stack) > 1 and stack[-1][0] >= indent:
            stack.pop()
        frame = stack[-1]
        parent = frame[1]
        if isinstance(parent, list):
            # 节内列表已开始却又出现 key 行：忽略（不支持的形态）
            continue
        if val == "":
            child = parent.get(key)
            if not isinstance(child, dict):
                child = {}
                parent[key] = child
            stack.append([indent, child, parent, key])
            continue
        parent[key] = parse_flow(val)
    return root


# ---------------------------------------------------------------- config 默认值

DEFAULT_ENUMS = {
    "caliber": ["written", "self", "disclosed", "planned", "visit", "official"],
    "status": ["verified", "self-reported", "pending-cert", "conflict", "retired"],
    "verify_depth": ["transcribed", "source_verified", "passage_checked", "value_recalculated"],
}

DEFAULT_TABLE_HEADERS = {
    "table_title": "文件摘要表",
    "file_col": "文件",
    "claim_col": "claim_ids",
    "summary_col": "一句话摘要",
    "sensitivity_col": "敏感度",
}


class OntologyConfig:
    """ontology.config.yaml 加载结果。缺失节保持 None 并记 warning（§12.4 保守默认闭环）。"""

    def __init__(self, data):
        self.data = data or {}
        self.warnings = []
        cfg = self.data
        # C1 文档别名：alias → 工程内相对路径（文件或目录）
        self.doc_aliases = cfg.get("doc_aliases")
        # C2 loc 语法：别名 → 正则列表
        self.loc_grammar = cfg.get("loc_grammar")
        # C3 摘要表：目录 → index 路径（嵌套映射或「- 目录：index」列表均归一为此形态）
        self.summary_tables = self._normalize_summary_tables(cfg.get("summary_tables"))
        # C4 枚举：缺省=当前三枚举（属性名不动）
        self.enums = cfg.get("enums")
        if self.enums is None:
            self.enums = {k: list(v) for k, v in DEFAULT_ENUMS.items()}
            self.warnings.append(
                "config 缺 enums 节，已用保守默认枚举（caliber/status/verify_depth）；请在 ontology.config.yaml 补登"
            )
        # C5 治理目录与编号 glob
        self.governance = cfg.get("governance")
        # C6 索引区块标记
        im = cfg.get("index_markers")
        if isinstance(im, dict) and im.get("start") and im.get("end"):
            self.index_start = str(im["start"])
            self.index_end = str(im["end"])
        else:
            self.index_start = DEFAULT_INDEX_START
            self.index_end = DEFAULT_INDEX_END
        # C7 摘要表表头
        hdr = cfg.get("summary_table_headers")
        merged = dict(DEFAULT_TABLE_HEADERS)
        if isinstance(hdr, dict):
            for k, v in hdr.items():
                if v:
                    merged[k] = str(v)
        self.table_headers = merged
        # C8 主题分组：[[主题, [谓词...]], ...]
        self.themes = self._normalize_themes(cfg.get("themes"))

    @staticmethod
    def _normalize_summary_tables(raw):
        """两种写法归一为 {目录: index路径}：
        嵌套映射：summary_tables:\n  目录: index 路径
        列表行：  summary_tables:\n  - 目录: index 路径"""
        if raw is None:
            return None
        result = {}
        if isinstance(raw, dict):
            for k, v in raw.items():
                result[str(k)] = str(v)
        elif isinstance(raw, list):
            for item in raw:
                if isinstance(item, (list, tuple)) and len(item) == 2:
                    result[str(item[0])] = str(item[1])
        return result

    @staticmethod
    def _normalize_themes(raw):
        if raw is None:
            return None
        if isinstance(raw, list):
            out = []
            for item in raw:
                if isinstance(item, (list, tuple)) and len(item) >= 2:
                    name = str(item[0])
                    preds = [str(x) for x in item[1]]
                    out.append((name, preds))
            return out
        return None


def load_config(path):
    """从路径加载 config；文件不存在时返回 None。"""
    p = Path(path)
    if not p.exists():
        return None
    return OntologyConfig(parse_config(p.read_text(encoding="utf-8")))
