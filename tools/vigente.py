"""Prints an act, or one provision of it, as it stood on a given day, from this repository's history.

    python tools/vigente.py 2000-01-01 costituzione 117          # art. 117 of the Constitution on 1 January 2000
    python tools/vigente.py 2023-01-01 costituzione              # the whole Constitution on 1 January 2023
    python tools/vigente.py 2015-06-01 decreto-legislativo/2003/196 13    # art. 13 of the privacy code
    python tools/vigente.py 2015-06-01 legge/1990/241 art-021-quater.md   # a file by name

Each commit carries the day its change took effect in an `In-force:` trailer (git cannot store dates before 1970, so
the trailer, not the commit date, is the source of truth). The text in force on a day is the file as of the last
commit on main whose In-force day is on or before it. A path that is a folder prints every file in it. Standard
library only.
"""
import re
import subprocess
import sys


def git(*args: str) -> str:
    return subprocess.run(['git', *args], capture_output=True, text=True, encoding='utf-8', check=True).stdout


def commit_on(day: str, path: str) -> str:
    out = git('log', '--first-parent', '--format=%H%x09%(trailers:key=In-force,valueonly,separator=)', 'main', '--', path)
    for line in out.splitlines():
        h, _, d = line.partition('\t')
        if d.strip() and d.strip() <= day:
            return h
    return ''


def file_for(act: str, key: str) -> str:
    """'117' -> art-117.md, '21-quater' -> art-021-quater.md; anything else is a file name in the act's folder."""
    m = re.fullmatch(r'(\d+)(?:[- ]?([a-z]+))?', key)
    if m:
        return f'art-{int(m.group(1)):03d}' + (f'-{m.group(2)}' if m.group(2) else '') + '.md'
    return key if key.endswith('.md') else f'{key}.md'


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    if len(sys.argv) < 3 or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', sys.argv[1]):
        sys.exit(__doc__)
    day, path = sys.argv[1], sys.argv[2].strip('/')
    if len(sys.argv) > 3:
        path = f'{path}/{file_for(path, sys.argv[3])}'
    commit = commit_on(day, path)
    if not commit:
        sys.exit(f'{path} is not in the record on {day}.')
    try:
        kind = git('cat-file', '-t', f'{commit}:{path}').strip()
    except subprocess.CalledProcessError:
        sys.exit(f'{path} was not in the text on {day} (repealed or not yet inserted).')
    if kind == 'blob':
        sys.stdout.write(git('show', f'{commit}:{path}'))
        return
    files = [f for f in git('ls-tree', '-r', '--name-only', commit, '--', f'{path}/').split('\n')
             if f.endswith('.md') and not f.endswith('README.md')]
    for f in files:
        sys.stdout.write(f'==> {f} <==\n' + git('show', f'{commit}:{f}') + '\n')


if __name__ == '__main__':
    main()
