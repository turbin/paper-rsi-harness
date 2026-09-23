# DEC-018 — 集成 zvec 用于模糊匹配并在初始化阶段自动安装

- 状态：confirmed
- 确认时间：2026-09-23T10:20:39+00:00（用户直接下达实现指令，当前会话用户消息）
- 记录时间：2026-09-23T10:20:39+00:00
- 来源：当前会话用户消息；未提供消息 ID。
- 替代关系：无。
- 关联问题：[ISS-005](../issues/ISS-005-zvec-fuzzy-matching.md)

## 用户原话

> 我希望工程能够集成zvec 用于模糊匹配，帮我在工程中集成zvec 并且在工程初始化阶段就可以自动拉取下载并安装到对应路径。

（此前同轮消息另有：「集成了gvec 这个工具了吗」——经核实用户所指为 alibaba/zvec，后续消息明确写作 zvec。）

## 实现取舍

1. zvec = [alibaba/zvec](https://github.com/alibaba/zvec)，Apache-2.0 进程内向量数据库；经 `pip install --target vendor zvec` 安装到脚本同级 `vendor/`，不写入系统 site-packages。
2. 初始化脚本在工作区 init 之后执行安装：已安装跳过；失败（无网络/无 pip）仅告警并继续，不阻断工作区初始化——模糊匹配是建议性功能，不是校验门禁。
3. `paper.py` 保持可独立运行：zvec 为可选依赖，`fuzzy_rank()` 在 zvec 不可用或查询失败时降级标准库 difflib，接口不变。
4. 向量表示用确定性字符 bigram 哈希（256 维，L2 归一化），不下载 embedding 模型，离线可用。
5. 首个接入点为 CLI 未知命令的最近建议（`错误: 未知命令 inti；是否想输入 "init"？`），只建议不自动执行；按后端分别标定建议阈值（zvec 0.15 / difflib 0.4，2026-09-23 实测标定）。
6. 模糊匹配仅用于建议，不用于任何校验、决议 ID 判定或安全决策。

## 影响范围

`paper.py`（fuzzy 模块与 CLI 预解析）、`setup.sh`、`setup.ps1`、`test_paper.py`、`.gitignore`、`README.md`、新增 `vendor/`（Git 忽略）。

## 时间线

- 2026-09-23T10:20:39+00:00：按用户指令完成集成与验证，状态 confirmed（用户指令即确认，非 Agent 推断）。
