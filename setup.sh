#!/usr/bin/env bash
# 一体化安装：初始化论文工作区 + 安装 paper-spec-socratic skill 到本机检测到的 agent。
# 用法：
#   bash setup.sh "/path/to/workspace"      # 建工作区，并把 skill 装到所有检测到的 agent
#   bash setup.sh --list                    # 只显示检测到的 agent，不安装
#   bash setup.sh --agent kimi "/path/..."  # skill 只装到指定 agent（kimi|claude|codex|gemini）
#   bash setup.sh --no-skill "/path/..."    # 只建工作区，不装 skill
#   bash setup.sh --force ...               # skill 已存在时覆盖
set -euo pipefail

SKILL_NAME="paper-spec-socratic"
script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
skill_src="$script_dir/skills/$SKILL_NAME"
[ -f "$skill_src/SKILL.md" ] || { echo "缺少 $skill_src/SKILL.md" >&2; exit 1; }

command -v python3 >/dev/null || { echo 'Install Python 3.10+ first.' >&2; exit 1; }
command -v git >/dev/null || { echo 'Install Git first.' >&2; exit 1; }
python3 -c 'import sys; assert sys.version_info >= (3,10), "Python 3.10+ required"'

# zvec 安装解释器：优先 py -3（与 Windows 下 paper.py 的运行约定一致），否则 python3。
PYRUN=python3
if command -v py >/dev/null 2>&1 \
   && py -3 -c 'import sys; sys.exit(0 if sys.version_info >= (3,10) and sys.version_info < (3,15) else 1)' 2>/dev/null; then
  PYRUN='py -3'
fi

home="${USERPROFILE:-$HOME}"
[ -n "$home" ] || { echo '找不到用户主目录。' >&2; exit 1; }

have() { command -v "$1" >/dev/null 2>&1; }
# Bash 3.2 兼容（ISS-001）：不使用关联数组，改用 case 查询。
AGENT_NAMES="kimi claude codex gemini"
agent_cmd() {
  case "$1" in
    kimi|claude|codex|gemini) echo "$1" ;;
    *) return 1 ;;
  esac
}
agent_dir() {
  case "$1" in
    kimi) echo "$home/.kimi-code/skills" ;;
    claude) echo "$home/.claude/skills" ;;
    codex) echo "$home/.agents/skills" ;;
    gemini) echo "$home/.gemini/skills" ;;
    *) return 1 ;;
  esac
}

detected=""
for name in $AGENT_NAMES; do
  if have "$(agent_cmd "$name")" || [ -d "$(agent_dir "$name")" ]; then
    if [ -z "$detected" ]; then detected="$name"; else detected="$detected $name"; fi
  fi
done

mode=full target="" force=0 root=""
while [ $# -gt 0 ]; do
  case "$1" in
    --list) mode=list ;;
    --no-skill) mode=workspace ;;
    --agent) shift; target="${1:?--agent 需要参数: kimi|claude|codex|gemini}" ;;
    --force) force=1 ;;
    -*) echo "未知参数: $1" >&2; exit 2 ;;
    *) root="$1" ;;
  esac
  shift
done

if [ "$mode" = list ]; then
  if [ -z "$detected" ]; then echo '未检测到任何已知 agent。'; else printf '检测到: %s\n' $detected; fi
  exit 0
fi

[ -n "$root" ] || { echo '用法: bash setup.sh [--list|--no-skill|--agent 名|--force] "/path/to/workspace"' >&2; exit 2; }
if [ -n "$target" ] && ! agent_dir "$target" >/dev/null 2>&1; then
  echo "未知 agent: $target（可选: kimi|claude|codex|gemini）" >&2; exit 2
fi

echo "==> 初始化工作区: $root"
python3 "$script_dir/paper.py" init --root "$root"

# zvec（模糊匹配，可选依赖）：初始化阶段自动安装到脚本同级 vendor/；失败仅告警，不阻断工作区初始化。
vendor_dir="$script_dir/vendor"
if [ -f "$vendor_dir/zvec/__init__.py" ]; then
  echo "zvec 已安装，跳过（$vendor_dir）"
else
  vendor_target="$vendor_dir"
  if command -v cygpath >/dev/null 2>&1; then vendor_target="$(cygpath -w "$vendor_dir")"; fi
  echo "==> 安装 zvec 到 $vendor_dir（模糊匹配）"
  if ! $PYRUN -m pip install --quiet --target "$vendor_target" zvec; then
    echo "警告: zvec 安装失败，模糊匹配将降级为标准库 difflib（可稍后手动: $PYRUN -m pip install --target vendor zvec）。" >&2
  elif [ ! -f "$vendor_dir/zvec/__init__.py" ]; then
    echo "警告: zvec 安装结果异常，未在 vendor/zvec 找到包；模糊匹配将降级为 difflib。" >&2
  else
    echo "==> zvec 安装完成（$vendor_dir）"
  fi
fi

if [ "$mode" = full ]; then
  if [ -n "$target" ]; then
    install_to="$target"
  elif [ -n "$detected" ]; then
    install_to="$detected"
  else
    echo '未检测到任何已知 agent，跳过 skill 安装（用 --agent 显式指定）。'
    install_to=""
  fi
  for name in $install_to; do
    dest="$(agent_dir "$name")/$SKILL_NAME"
    if [ -e "$dest/SKILL.md" ] && [ "$force" -eq 0 ]; then
      echo "跳过 $name：$dest 已存在（用 --force 覆盖）"
      continue
    fi
    mkdir -p "$dest"
    cp "$skill_src/SKILL.md" "$dest/SKILL.md"
    echo "==> skill 已安装到 $name：$dest"
  done
fi
echo "完成。"
