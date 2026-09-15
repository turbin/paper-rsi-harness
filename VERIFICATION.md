# 验证记录

记录日期：2026-09-15；执行环境：当前 Linux 沙盒。

- `python3 -m unittest -v test_paper.py`：20/20 通过。
- `bash -n install.sh`：通过 Bash 语法检查。
- `bash install.sh <新建独立目录>`：成功创建完整模板和 `.git/`。
- `paper.py run --dry-run`：成功生成待调用请求，未调用任何模型。
- 离线端到端：真实启动 Python 子进程夹具，PM规划 → Writer → Reviewer → PM汇总 → awaiting_user_acceptance；不冒充模型测试。
- 补充测试：原话保留、运行中输入变更后暂停、决议替代环路、目录整体删除、索引标记损坏拒绝写入。

未验证：Windows/macOS 原生运行、PowerShell 解析/执行（本环境无 pwsh）、各真实 Agent CLI 登录及兼容性、真实 MBA 学术质量、OS 级隔离与子进程树回收。
CLI 适配来自官方文档，不能等同于已经通过对应产品实机测试。

所有模型后端初始为 disabled；未调用付费服务，也未对外发送用户论文材料。
