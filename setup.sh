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

home="${USERPROFILE:-$HOME}"
[ -n "$home" ] || { echo '找不到用户主目录。' >&2; exit 1; }

have() { command -v "$1" >/dev/null 2>&1; }
declare -A CMDS=( [kimi]=kimi [claude]=claude [codex]=codex [gemini]=gemini )
declare -A DIRS=( [kimi]="$home/.kimi-code/skills" [claude]="$home/.claude/skills" [codex]="$home/.agents/skills" [gemini]="$home/.gemini/skills" )

detected=()
for name in "${!DIRS[@]}"; do
  if have "${CMDS[$name]}" || [ -d "${DIRS[$name]}" ]; then detected+=("$name"); fi
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
  if [ ${#detected[@]} -eq 0 ]; then echo '未检测到任何已知 agent。'; else printf '检测到: %s\n' "${detected[@]}"; fi
  exit 0
fi

[ -n "$root" ] || { echo '用法: bash setup.sh [--list|--no-skill|--agent 名|--force] "/path/to/workspace"' >&2; exit 2; }
if [ -n "$target" ] && [ -z "${DIRS[$target]:-}" ]; then
  echo "未知 agent: $target（可选: kimi|claude|codex|gemini）" >&2; exit 2
fi

echo "==> 初始化工作区: $root"
python3 "$script_dir/paper.py" init --root "$root"

if [ "$mode" = full ]; then
  if [ -n "$target" ]; then
    install_to=("$target")
  else
    [ ${#detected[@]} -gt 0 ] || { echo '未检测到任何已知 agent，跳过 skill 安装（用 --agent 显式指定）。' >&2; install_to=(); }
    [ ${#detected[@]} -gt 0 ] && install_to=("${detected[@]}")
  fi
  for name in "${install_to[@]:-}"; do
    [ -n "$name" ] || continue
    dest="${DIRS[$name]}/$SKILL_NAME"
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
