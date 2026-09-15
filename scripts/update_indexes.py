#!/usr/bin/env python3
"""Update source-project indexes, retaining prose and append-only observations."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from paper import atomic

BEGIN = '<!-- project-index:start -->'
END = '<!-- project-index:end -->'


def update(root, reason):
    cache = root / '.project-runtime/index-state.json'
    prior = json.loads(cache.read_text(encoding='utf-8')) if cache.exists() else {}
    stamp = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
    folders, current = {}, {}
    def ignored(path):
        return subprocess.run(['git', '-C', str(root), 'check-ignore', '-q', '--',
                               path.relative_to(root).as_posix()], check=False).returncode == 0
    for parent, dirs, files in os.walk(root):
        folder = Path(parent)
        dirs[:] = sorted(d for d in dirs if d not in {'.git', '.project-runtime', '__pycache__'}
                         and not (folder / d).is_symlink() and not ignored(folder / d))
        rel = folder.relative_to(root).as_posix()
        names = sorted(f for f in files if f != 'index.md' and not f.startswith('.paper-tmp-')
                       and not (folder / f).is_symlink() and not ignored(folder / f))
        folders[rel] = (folder, dirs[:], names)
        for name in names:
            path = folder / name
            key = path.relative_to(root).as_posix()
            h = hashlib.sha256()
            with path.open('rb') as stream:
                for chunk in iter(lambda: stream.read(1048576), b''):
                    h.update(chunk)
            digest = h.hexdigest()
            old = prior.get(key, {})
            current[key] = {'sha256': digest, 'observed_at': old.get('observed_at', stamp)
                            if old.get('sha256') == digest else stamp}
    changes = []
    for key in sorted(current.keys() | prior.keys()):
        if key not in current:
            changes.append((key, '删除或移出索引范围'))
        elif key not in prior:
            changes.append((key, '首次纳入索引'))
        elif current[key]['sha256'] != prior[key]['sha256']:
            changes.append((key, '修改'))
    pending = []
    for rel, (folder, children, names) in folders.items():
        path = folder / 'index.md'
        if path.is_symlink():
            raise ValueError(f'索引不能是符号链接: {path}')
        text = path.read_text(encoding='utf-8') if path.exists() else f'# {rel} 目录索引\n'
        if text.count(BEGIN) != text.count(END) or text.count(BEGIN) > 1 or (BEGIN in text and text.index(BEGIN) > text.index(END)):
            raise ValueError(f'索引标记损坏: {path}')
        history = ''
        if BEGIN in text:
            block = text.split(BEGIN, 1)[1].split(END, 1)[0]
            history = block.split('### 变更时间线\n', 1)[1].strip()
        rows = []
        for name in names:
            item = current[(folder / name).relative_to(root).as_posix()]
            rows.append(f'| {name.replace("|", "&#124;")} | {item["observed_at"]} | `{item["sha256"][:12]}` |')
        events = [f'- {stamp} · {kind} `{key}` · {reason}' for key, kind in changes
                  if rel == '.' or Path(key).parent.as_posix() == rel]
        block = BEGIN + '\n### 文件快照\n\n| 文件 | 变更观察时间（UTC） | SHA-256 |\n|---|---|---|\n'
        block += '\n'.join(rows) + '\n\n### 子目录\n\n'
        block += '\n'.join(f'- [{d}]({d}/index.md)' for d in children)
        block += '\n\n### 变更时间线\n' + '\n'.join(events + ([history] if history else [])) + '\n' + END
        updated = text.split(BEGIN, 1)[0] + block + text.split(END, 1)[1] if BEGIN in text else text.rstrip() + '\n\n' + block + '\n'
        if text != updated:
            pending.append((path, updated))
    for path, content in pending:
        atomic(path, content)
    atomic(cache, json.dumps(current, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(folders)} 个目录，{len(changes)} 项文件变更，更新 {len(pending)} 个索引。')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reason', required=True, help='本轮变更原因；时间为扫描观察时间')
    args = parser.parse_args()
    update(Path(__file__).resolve().parents[1], args.reason.replace('\n', ' '))
