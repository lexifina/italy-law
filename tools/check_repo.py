"""Checks the Italian law repository against the official data it was built from.

    python -X utf8 scripts/italy-law/check_repo.py [--repo ../italy-law] [--write]

1. Byte for byte: for every version of every act (up to the build day), the files of that act on main at the last
   commit in force on the version's day are exactly the files the version's Akoma Ntoso text renders to: no file
   missing, none extra, every byte the same.
2. Word for word: the words of those files, in order, equal the words of the whole official text of the version, read
   independently from the XML (every text node of the preface, preamble, body, conclusions and annexes, joined with a
   space only at block boundaries; the part and chapter headings, which the repository keeps in struttura.md, apart).
3. For information: the same words against Normattiva's JSON export of the same version (a second manifestation).
With --write the result goes to verification.json next to this script (for REPRODUCE.md).
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import subprocess
import sys
import zipfile
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build  # noqa: E402

from lxml import etree  # noqa: E402

NS = build.NS
INLINE_IN_QUOTES = build.QUOTED
SKIP = {'meta'}
HEADING_PARENTS = {'chapter', 'part', 'title', 'book', 'section', 'division', 'subsection', 'hcontainer'}
W = re.compile(r'\w+')


def official_words(zpath: str, member: str) -> list[str]:
    """Every word of the version's text, read straight from the XML, independently of build.render_lines."""
    with zipfile.ZipFile(zpath) as z:
        root = etree.fromstring(z.read(member))
    act = root.find(f'{NS}act')
    parts: list[str] = []

    def walk(e, quoted):
        name = build._local(e.tag)
        if not name:
            parts.append(e.tail or '')
            return
        if name in SKIP:
            parts.append(' ' + (e.tail or ''))
            return
        if name in ('num', 'heading') and build._local(e.getparent().tag) in HEADING_PARENTS:
            parts.append(' ' + (e.tail or ''))      # kept in struttura.md, checked apart
            return
        q = quoted or name in INLINE_IN_QUOTES
        block = name in build.BLOCK and not quoted
        parts.append((' ' if block else '') + (e.text or ''))
        for c in e:
            walk(c, q)
        parts.append((' ' if block else '') + (e.tail or ''))

    for top in act:
        if build._local(top.tag) in ('preface', 'preamble', 'body', 'conclusions'):
            walk(top, False)
            parts.append(' ')
    for doc in act.iter(f'{NS}doc'):
        mb = doc.find(f'{NS}mainBody')
        if mb is not None:
            walk(mb, False)
            parts.append(' ')
    text = build.INVISIBLE.sub('', ''.join(parts))
    return text.split()


def json_words(jpath: str, jmember: str) -> list[str]:
    with zipfile.ZipFile(jpath) as z:
        j = json.loads(z.read(jmember))

    def jw(e):
        for x in (e or {}).get('elementi') or []:
            yield x
            yield from jw(x)
    out = []
    for x in list(jw(j.get('articolato'))) + list(jw(j.get('annessi'))):
        if x.get('nomeNir'):
            t = ' '.join(x.get(f) or '' for f in ('testo', 'noteArt'))
            r = ' '.join(W.findall((x.get('rubricaNir') or '').casefold()))
            if r and r not in ' '.join(W.findall(t.casefold())):
                t = (x.get('rubricaNir') or '') + ' ' + t     # the heading, when the text does not repeat it
            out += W.findall(build.INVISIBLE.sub('', t).casefold())
    return out


def task(args):
    zp, member, jp, jm = args
    v = build.read_version(args)
    return {'member': member, 'units': v['units'], 'order': v['order'], 'expr': v['expr'],
            'official': official_words(zp, member), 'json': json_words(jp, jm) if jp else None}


def git(repo, *a, input=None) -> bytes:
    out = subprocess.run(['git', *a], cwd=repo, capture_output=True, input=input)
    if out.returncode:
        raise SystemExit(out.stderr.decode())
    return out.stdout


def files_at(repo, sha: str, prefix: str) -> dict[str, str]:
    names = [n for n in git(repo, 'ls-tree', '-r', '--name-only', sha, '--', prefix + '/').decode().split('\n') if n]
    if not names:
        return {}
    out = git(repo, 'cat-file', '--batch', input=''.join(f'{sha}:{n}\n' for n in names).encode())
    res, i = {}, 0
    for n in names:
        j = out.index(b'\n', i)
        size = int(out[i:j].split()[2])
        res[n[len(prefix) + 1:]] = out[j + 1:j + 1 + size].decode('utf-8')
        i = j + 1 + size + 1
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', default=str(build.ROOT.parent / 'italy-law'))
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()
    repo = args.repo
    rows = git(repo, 'log', '--first-parent', '--reverse', '--format=%H%x09%(trailers:key=In-force,valueonly,separator=)',
               'main').decode().split('\n')
    commits = [(r.split('\t')[0], r.split('\t')[1].strip()) for r in rows if r and r.split('\t')[1].strip()]
    today = commits[-1][1]

    def at(day):
        best = None
        for sha, d in commits:
            if d <= day:
                best = sha
            else:
                break
        return best

    tasks, where = [], []
    for src in build.SOURCES:
        zp, jp = build.ZIPS / f'{src["id"]}.zip', build.ZIPS / f'{src["id"]}-json.zip'
        with zipfile.ZipFile(zp) as z:
            members = [n for n in z.namelist() if n.endswith('.xml')]
        with zipfile.ZipFile(jp) as z:
            jm = {n[:-5]: n for n in z.namelist() if n.endswith('.json')}
        for n in sorted(members, key=lambda n: (n.split('/')[0], int(re.search(r'_V(\d+)\.xml$', n).group(1)))):
            tasks.append((str(zp), n, str(jp) if n[:-4] in jm else None, jm.get(n[:-4])))
            where.append(n.split('/')[0])
    with Pool(8) as pool:
        parsed = list(pool.imap(task, tasks, chunksize=4))
    by_act: dict[str, list[dict]] = collections.defaultdict(list)
    for w, p in zip(where, parsed):
        by_act[w].append(p)

    n_versions = n_files = mismatches = words = word_mismatches = json_same = json_total = 0
    problems = []
    json_by_act: dict[str, list[int]] = {}
    for folder, vs in by_act.items():
        prefix = build.act_from_folder(folder, None)['path']
        vs[0]['from'] = vs[0]['expr']
        for v in vs[1:]:
            v['from'] = re.search(r'_VIGENZA_(\d{4}-\d{2}-\d{2})_V\d+', v['member']).group(1)
        kept = {}
        for v in vs:
            kept[v['from']] = v          # the later version of a day wins, as in the build
        for day, v in sorted(kept.items()):
            if day > today:
                continue
            n_versions += 1
            sha = at(day)
            have = files_at(repo, sha, prefix) if sha else {}
            have.pop('README.md', None)
            want = {u['path']: u['text'] for u in v['units'].values()}
            n_files += len(want)
            bad = sorted(p for p in set(have) | set(want) if have.get(p) != want.get(p))
            if bad:
                mismatches += len(bad)
                problems.append(f'{prefix} {day}: {len(bad)} files differ, e.g. {bad[:3]}')
            ours = ' '.join(have.get(v['units'][k]['path'], '') for k in v['order'] if k != 'struttura').split()
            words += len(ours)
            if ours != v['official']:
                word_mismatches += 1
                problems.append(f'{prefix} {day}: words differ ({len(ours)} against {len(v["official"])})')
            if v['json'] is not None:
                json_total += 1
                ow = W.findall(' '.join(have.get(v['units'][k]['path'], '') for k in v['order']
                                        if k not in ('struttura', 'intestazione')).casefold())
                same = collections.Counter(ow) == collections.Counter(v['json'])
                json_same += same
                json_by_act.setdefault(prefix, [0, 0])
                json_by_act[prefix][0] += same
                json_by_act[prefix][1] += 1
    rec = {'versions': n_versions, 'files': n_files, 'mismatches': mismatches, 'wordcheck': n_versions, 'words': words,
           'word_mismatches': word_mismatches, 'json_versions': json_total, 'json_identical_words': json_same,
           'json_by_act': {k: f'{a}/{b}' for k, (a, b) in sorted(json_by_act.items()) if a != b}}
    for p in problems[:40]:
        print(p)
    print(json.dumps(rec, indent=1))
    if args.write:
        p = HERE / 'verification.json'
        ver = json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
        ver['check'] = rec
        p.write_text(json.dumps(ver, indent=1, sort_keys=True) + '\n', encoding='utf-8', newline='\n')
    raise SystemExit(1 if mismatches or word_mismatches else 0)


if __name__ == '__main__':
    main()
