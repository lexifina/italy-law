"""Functional smoke test of the built Italian law repository: the things a reader does with it work. Standard library
only.

    python -X utf8 scripts/italy-law/test_repo.py [--repo ../italy-law] [--record]
    python -X utf8 tools/test_repo.py                   # from inside the repository

It asserts that:
1. `git blame` on a changed article names amending acts as authors of its lines;
2. tools/vigente.py gives the text before and after known amendments, each equal to the file at that day's tag;
3. `git log --follow` on a file lists its amending acts in the order they took effect;
4. every tag resolves to a commit, and every commit but the documentation commit has an `In-force:` trailer;
5. no commit is authored by Lexifina except the documentation commit (the last one), and law authors use .invalid
   addresses;
6. every git or tool command in the README's table runs and prints something.
With --record the result is written to verification.json next to this script (for REPRODUCE.md).
"""
import argparse
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PUBLISHER = 'Normattiva (IPZS)'


DOC_TOP = ('REPRODUCE.md', 'LICENSE', 'PLAN.md', 'SOURCES.md', '.gitattributes', '.gitignore')
DOC_DIRS = ('data/', 'tools/', 'visualisations/', 'vulnerabilities/', 'registry/', 'monitoring/')


def is_doc_file(path):
    """A file a documentation commit may touch, never law text: README*, REPRODUCE.md, LICENSE, PLAN.md, SOURCES.md,
    *.csv and *.json at the top; anything under data/, tools/, visualisations/, vulnerabilities/, registry/, monitoring/;
    an act folder's README.md (no law text file is named README.md)."""
    if '/' not in path:
        return path.startswith('README') or path in DOC_TOP or path.endswith(('.csv', '.json'))
    return path.startswith(DOC_DIRS) or path.endswith('/README.md')


def doc_commit_problems(repo, rows):
    """rows: (sha, In-force value) of each commit authored by Lexifina. Every one is a documentation commit (README,
    charts, tools): no In-force trailer and no law text file (one git log --no-walk --name-only for all of them)."""
    if not rows:
        return []
    out = subprocess.run(['git', '-c', 'core.quotePath=false', 'log', '--no-walk=unsorted', '--stdin', '--name-only',
                          '--format=%x00%H'], cwd=repo, input=''.join(h + '\n' for h, _ in rows), capture_output=True,
                         text=True, encoding='utf-8')
    if out.returncode:
        raise AssertionError(f'git log --no-walk: {out.stderr.strip()}')
    files = {}
    for block in out.stdout.split('\x00')[1:]:
        lines = [l for l in block.splitlines() if l]
        files[lines[0]] = lines[1:]
    bad = []
    for h, day in rows:
        law = [f for f in files.get(h, []) if not is_doc_file(f)]
        if day.strip() or law:
            bad.append(h[:10] + (f' In-force {day.strip()}' if day.strip() else '')
                       + (f' touches {len(law)} law text file(s), e.g. {law[0]}' if law else ''))
    return bad


def default_repo() -> Path:
    if (HERE.parent / '.git').exists():
        return HERE.parent
    return HERE.parents[2] / 'italy-law'


class Smoke:
    def __init__(self, repo: Path):
        self.repo = repo
        self.results: list[tuple[str, bool, str]] = []

    def git(self, *args: str) -> str:
        out = subprocess.run(['git', *args], cwd=self.repo, capture_output=True, text=True, encoding='utf-8')
        if out.returncode:
            raise AssertionError(f'git {" ".join(args)}: {out.stderr.strip()}')
        return out.stdout

    def tool(self, *args: str) -> str:
        out = subprocess.run([sys.executable, 'tools/vigente.py', *args], cwd=self.repo, capture_output=True, text=True,
                             encoding='utf-8')
        if out.returncode:
            raise AssertionError(f'vigente {" ".join(args)}: {out.stderr.strip()}')
        return out.stdout

    def check(self, name: str, fn):
        try:
            detail = fn() or ''
            self.results.append((name, True, detail))
            print(f'PASS {name}: {detail}')
        except AssertionError as exc:
            self.results.append((name, False, str(exc)))
            print(f'FAIL {name}: {exc}')
        except Exception as exc:  # any other error fails this check only; the run goes on
            self.results.append((name, False, f'{type(exc).__name__}: {exc}'))
            print(f'FAIL {name}: {type(exc).__name__}: {exc}')

    # 1
    def blame(self):
        out = self.git('blame', '--line-porcelain', 'main', '--', 'costituzione/art-117.md')
        authors = {l[7:] for l in out.splitlines() if l.startswith('author ')}
        assert 'Legge costituzionale 3/2001' in authors, f'Legge costituzionale 3/2001 not among {authors}'
        assert 'Legge costituzionale 1/2012' in authors, f'Legge costituzionale 1/2012 not among {authors}'
        assert 'Lexifina' not in authors
        return f'costituzione/art-117.md lines by {", ".join(sorted(authors))}'

    # 2
    def on_date(self):
        done = []
        for act, prov, path, tag, before, after in [
                ('costituzione', '9', 'costituzione/art-009.md', 'costituzione/2022-03-09', '2022-03-08', '2022-03-09'),
                ('costituzione', '117', 'costituzione/art-117.md', 'costituzione/2001-11-08', '2001-11-07', '2001-11-08'),
                ('decreto-legislativo/2003/196', '13', 'decreto-legislativo/2003/196/art-013.md',
                 'decreto-legislativo/2003/196/2018-09-19', '2018-09-18', '2018-09-19')]:
            a, b = self.tool(before, act, prov), self.tool(after, act, prov)
            assert a and b and a != b, f'{path}: no change between {before} and {after}'
            assert b == self.git('show', f'{tag}:{path}'), f'{path} on {after} is not the file at {tag}'
            assert a == self.git('show', f'{tag}~1:{path}'), f'{path} on {before} is not the file before {tag}'
            done.append(f'{path} {before} != {after}')
        whole = self.tool('1950-01-01', 'costituzione')
        assert 'Art. 117.' in whole and 'Tutela l\'ambiente' not in whole, 'whole Constitution on 1950-01-01 is wrong'
        return '; '.join(done)

    # 3
    def follow(self):
        checked = []
        for path in ('costituzione/art-117.md', 'legge/1990/241/art-021-quater.md', 'decreto-legislativo/2003/196/art-132.md'):
            out = self.git('log', '--follow', '--format=%an%x09%(trailers:key=In-force,valueonly,separator=)', 'main', '--', path)
            rows = [l.split('\t') for l in out.splitlines() if l]
            assert len(rows) >= 2, f'{path}: {len(rows)} commits'
            days = [d.strip() for _, d in rows]
            assert days == sorted(days, reverse=True), f'{path}: not in date order {days}'
            assert sum(1 for a, _ in rows if a != PUBLISHER) >= 2, f'{path}: fewer than two acts'
            checked.append(f'{path} {len(rows)} commits')
        return '; '.join(checked)

    # 4
    def tags_and_trailers(self):
        tags = self.git('tag').split()
        assert tags, 'no tags'
        for t in tags:
            self.git('rev-parse', '--verify', '-q', f'{t}^{{commit}}')
        rows = self.git('log', '--format=%H%x09%an%x09%(trailers:key=In-force,valueonly,separator=)', 'main').splitlines()
        rows = [r for r in rows if r.split('\t')[1] != 'Lexifina']   # documentation commits (by Lexifina) carry no In-force
        missing = [r for r in rows if not r.split('\t')[2].strip()]
        assert not missing, f'{len(missing)} commits without In-force, e.g. {missing[:2]}'
        bad = [r for r in rows if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', r.split('\t')[2].strip())]
        assert not bad, f'malformed In-force {bad[:2]}'
        days = [r.split('\t')[2].strip() for r in rows]
        assert days == sorted(days, reverse=True), 'In-force days are not in history order'
        parsed = ''.join(self.git('log', '-1', '--format=%(trailers:key=In-force,valueonly)', r.split('\t')[0])
                         for r in rows[:5]).split()
        assert parsed, 'trailers do not parse'
        return f'{len(tags)} tags resolve; {len(rows)} law commits carry In-force, in order'

    # 5
    def lexifina(self):
        rows = self.git('log', '--format=%H%x09%an%x09%ae%x09%cn%x09%(trailers:key=In-force,valueonly,separator=)',
                        'main').splitlines()
        by_lex = [r for r in rows if r.split('\t')[1] == 'Lexifina']
        assert by_lex, 'no documentation commit by Lexifina'
        bad = doc_commit_problems(self.repo, [(r.split('\t')[0], r.split('\t')[4]) for r in by_lex])
        assert not bad, f'{len(bad)} Lexifina commits are not documentation commits, e.g. {bad[:3]}'
        law = [r for r in rows if r.split('\t')[1] != 'Lexifina']
        assert all(r.split('\t')[3] == 'Lexifina' for r in rows), 'a committer other than Lexifina'
        assert all(r.split('\t')[2].endswith('.invalid') for r in law), 'a law author without an .invalid address'
        authors = {r.split('\t')[1] for r in law}
        return f'{len(by_lex)} documentation commits by Lexifina, none with In-force or law text; {len(authors)} distinct authors'

    # 6
    def readme(self):
        readme_path = self.repo / 'README.en.md'  # the English README where there is one, else README.md
        text = (readme_path if readme_path.exists() else self.repo / 'README.md').read_text(encoding='utf-8')
        start = text.index('## Questions as git commands')
        end = text.find('\n## ', start + 1)
        table = text[start:end if end != -1 else len(text)]
        rows = '\n'.join(l for l in table.splitlines() if l.startswith('|'))
        cmds = [c for c in re.findall(r'`([^`]+)`', rows) if c.startswith(('git ', 'python ')) and '<' not in c]
        assert len(cmds) >= 3, f'only {len(cmds)} commands found'
        for c in cmds:
            args = shlex.split(c)
            if args[0] == 'python':
                args[0] = sys.executable
            out = subprocess.run(args, cwd=self.repo, capture_output=True, text=True, encoding='utf-8')
            assert out.returncode == 0, f'{c}: exit {out.returncode} {out.stderr.strip()[:200]}'
            assert out.stdout.strip(), f'{c}: printed nothing'
        return f'{len(cmds)} README commands ran and printed output'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', default=None)
    ap.add_argument('--record', action='store_true')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    s = Smoke(Path(args.repo) if args.repo else default_repo())
    s.check('blame names the amending acts', s.blame)
    s.check('text before and after an amendment', s.on_date)
    s.check('log --follow in date order', s.follow)
    s.check('tags resolve, In-force on every law commit', s.tags_and_trailers)
    s.check('only the documentation commit is by Lexifina', s.lexifina)
    s.check('README commands run', s.readme)
    ok = all(r[1] for r in s.results)
    print(f'{sum(r[1] for r in s.results)}/{len(s.results)} passed')
    if args.record:
        p = HERE / 'verification.json'
        rec = json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
        rec['smoke'] = {'passed': sum(r[1] for r in s.results), 'total': len(s.results),
                        'results': [{'test': n, 'ok': o, 'detail': d} for n, o, d in s.results]}
        p.write_text(json.dumps(rec, indent=1, sort_keys=True, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    raise SystemExit(0 if ok else 1)


if __name__ == '__main__':
    main()
