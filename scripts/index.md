# 工程维护脚本

`update_indexes.py` 为源码工程生成目录索引。运行：

```bash
python3 scripts/update_indexes.py --reason "简述本轮变更"
```

保留目录说明和变更时间线；重复扫描未变文件不会新增记录。根索引汇总整个工程的文件变更，各子目录记录直接所属文件。删除目录的事件保留在根索引。索引文件自身不计入快照，避免递归更新。

本地哈希基线位于 Git 忽略的 `.project-runtime/`；丢失后下次扫描重建基线，已写入索引的历史仍保留。请串行运行此命令。

<!-- project-index:start -->
### 文件快照

| 文件 | 变更观察时间（UTC） | SHA-256 |
|---|---|---|
| update_indexes.py | 2026-11-07T07:59:58+00:00 | `2dd8ade83f6f` |

### 子目录



### 变更时间线
- 2026-11-07T07:59:58+00:00 · 首次纳入索引 `scripts/update_indexes.py` · 登记 DEC-019/ISS-006，新增 ontology G2 模板资产（config 化校验器/图生成器/init 脚本）
- 2026-09-15T04:11:09+00:00 · 首次纳入索引 `scripts/update_indexes.py` · 依据 DEC-001 初始化源码工程管理，登记四项已有问题，建立首次文件基线
<!-- project-index:end -->
