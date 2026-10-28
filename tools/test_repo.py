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
        missing = [r for r in rows[1:] if not r.split('\t')[2].strip()]
        assert not missing, f'{len(missing)} commits without In-force, e.g. {missing[:2]}'
        assert not rows[0].split('\t')[2].strip(), 'documentation commit should carry no In-force'
        bad = [r for r in rows[1:] if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', r.split('\t')[2].strip())]
        assert not bad, f'malformed In-force {bad[:2]}'
        days = [r.split('\t')[2].strip() for r in rows[1:]]
        assert days == sorted(days, reverse=True), 'In-force days are not in history order'
        parsed = self.git('log', '-5', '--format=%(trailers:key=In-force,valueonly)', 'main').split()
        assert parsed, 'trailers do not parse'
        return f'{len(tags)} tags resolve; {len(rows) - 1} law commits carry In-force, in order'

    # 5
    def lexifina(self):
        rows = self.git('log', '--format=%H%x09%an%x09%ae%x09%cn', 'main').splitlines()
        by_lex = [r for r in rows if r.split('\t')[1] == 'Lexifina']
        assert len(by_lex) == 1 and by_lex[0] == rows[0], f'{len(by_lex)} commits by Lexifina'
        assert all(r.split('\t')[3] == 'Lexifina' for r in rows), 'a committer other than Lexifina'
        assert all(r.split('\t')[2].endswith('.invalid') for r in rows[1:]), 'a law author without an .invalid address'
        authors = {r.split('\t')[1] for r in rows[1:]}
        return f'only the documentation commit {rows[0][:10]} is by Lexifina; {len(authors)} distinct authors'

    # 6
    def readme(self):
        text = (self.repo / 'README.md').read_text(encoding='utf-8')
        table = text[text.index('## The questions'):text.index('## The dates')]
        cmds = [c for c in re.findall(r'`([^`]+)`', table) if c.startswith(('git ', 'python '))]
        assert len(cmds) >= 8, f'only {len(cmds)} commands found'
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
