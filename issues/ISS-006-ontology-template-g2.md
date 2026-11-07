# ISS-006 — ontology G2 模板资产实施（config 化校验器/图生成器/init 脚本）

- 状态：resolved
- 创建时间：2026-11-07
- 来源：用户指令「读取设计方案，按照设计方案对当前工程进行重构」（2026-11-07），见 [DEC-019](../decisions/DEC-019-ontology-template-g2.md)；设计依据为下游设计方案 §12（DEC-022 拍板 G2、实施主体上游）。

## 依据

下游设计方案 §12 通用化设计：当前本体实现（下游 mba-bdp-优月仓储/knowledge/）达 G1 模式级、
未达 G2 模板级（枚举即耦合、机制依赖未接口化）。拍板启动 G2 改造，实施主体为本上游工程；
下游作为行为零漂移回归基准（§12.7）。

## 验收条件

1. **行为零漂移回归**：ontology/test_ontology.py 内置两项对照——①下游 claims.yaml 全量经
   `--export-legacy` 注入 THEMES 后生成 graph.md 与下游在用 graph.md 字节级一致（仅头部来源行
   路径替换）；②下游 claims 代表性子集（CLM-001/002/004/030）在同一输入下报警逐行一致、退出码一致。✅ 2026-11-07 实测通过
2. **config 五表机械导出**：`--export-legacy` 对下游真实文件提取 DOC_ALIASES 2 条 /
   LOC_GRAMMAR 2 键 4 正则 / SUMMARY_TABLES 1 条 / ENUMS 3 枚举（6/5/4 值）/
   THEMES 10 组 29 谓词，逐条对照进转换报告。✅
3. **init 全新工程幂等**：临时工程 `init` 扫描 issues/decisions/index 区块/摘要表候选写 config；
   重复运行不覆盖；`--force` 可重写。✅
4. **上游既有测试不回归**：`python3 test_paper.py` 全过（45/45，skip 2 为既有平台跳过）。✅
5. **四步实测验收**（§12.7 第二工程实测，人工）：①拷贝＋init 全程不改代码；②登记 3 条真实主张
   校验全绿；③注入 1 个坏点（不存在证据文件）被捕获；④全程 ≤30 分钟。⬜ 待第二工程实测（本轮不阻塞收尾）
6. **编码自检**：全部新文件 UTF-8 无 BOM、LF 换行。✅（test_ontology.py 内置用例）

## 影响

- 新增 `ontology/` 目录：validate_claims.py / gen_graph.py / config_loader.py / init_ontology.py /
  templates/（4 件）/ test_ontology.py / README.md。采用工程经 `init_ontology.py` 或
  `--export-legacy` 在自身 knowledge/ 生成 ontology.config.yaml（上游源码工程不预置该文件）。
- 下游工程零改动（只读基准）；上游 AGENTS.md 不动（纪律条款模板在 templates/，挂接由用户拍板）。

## 处理时间线

- 2026-11-07：登记（open）；同轮完成实现、测试与登记，状态置 in_progress；
  resolved 留待收尾审核（对抗式审核共识后）确认第 5 项四步实测安排。
- 2026-11-07（验证轮）：独立验证 agent 复核——8 轮通道级破坏测试新旧输出逐字一致（33 条全量基线
  exit 0/0）；五表对照 41/41 OK；第二工程四步模拟 13 秒全通过（零代码改动）；边界探针 6 项，
  2 项 P1 已修复复验：①loc_grammar 非法正则改为 error 报警不 traceback；②页数锚文案 ISS-17→ISS-017
  对齐下游。修复后 test_ontology 28/28、test_paper 45/45 复跑通过。
- 2026-11-07（对抗审核 R1 轮）：五维对抗审核判定 FIX_REQUIRED（无 P0，P1×2，P2×3）。
  P1：①本文件时间线曾误将计划中的审核轮次（R1–R5、R2 共识）预写成已完成事实，违背
  「建议不能冒充确认」记录纪律，已更正为按实际发生逐轮补记；②README known-diff 1 补充
  落盘 validation_log.md 影响说明。P2 同批处置：影响节 config 文件表述更正、governance
  命名对照补入 README、.git gitlink 收录缺陷登记为 ISS-007。
- 2026-11-07（对抗审核 R2 轮）：六项修复逐项复核全部 PASS；代码零改动（SHA 比对确认），
  回归抽查（r0/r4 通道）无新漂移；新增 P2 R2-1（本 issue 手工问题表漏 ISS-007 行）已随手补登。
  最终判定 CONSENSUS（无未决 P0/P1），两轮达成（上限 5）。验收条件 1–4、6 全过，
  第 5 项四步实测维持「待真实第二工程执行」标注（模拟已过，13 秒），不阻塞 resolved。
- 2026-11-07（收尾）：状态置 resolved。遗留跟踪：第二工程四步实测（验收条件 5）、
  ISS-007（update_indexes .git gitlink，独立 open）、config 未知节静默（P2，待有需时加提示）。
