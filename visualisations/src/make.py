"""Rebuild visualisations/il-diritto-italiano-in-20-grafici.html from this repository.

    python visualisations/src/make.py [--repo PATH] [--ref REF] [--skip-extract] [--no-fetch]

Steps (all read-only on the repository; scratch output goes to visualisations/src/.build/):
  1. the history of REF (default origin/main), streamed once, one compact line per commit the charts use, by source
     (the commit author's address says which: normattiva, camera, senato, cortecostituzionale, giustizia-amministrativa,
     corteconti, publications.europa, agcm)                                            -> .build/log-*.tsv, counts.json
  2. the tree of REF, streamed: the act folders of normativa/ with their files, the Constitution, the four codes
                                                                                        -> .build/tree-*.tsv
  3. the blobs the charts read, fetched in batches in a partial (blobless) clone, some 248,000 small files in all:
     data/atti.csv, the scheda.md of every decision of the Corte costituzionale, the record of every vote of the
     Camera dei deputati and of every bill of the Senate, the heading (intestazione.md) of every act in normativa/,
     and the articles of the Constitution in force                                      -> .build/blob-*.tsv
  4. prep.py turns those into .build/data.json; build.py fills page.tpl.html with it.
Works in a blobless or --no-checkout clone: everything is read from git objects, nothing large is held in memory, and
GIT_NO_LAZY_FETCH=1 keeps git from fetching anything behind our back (missing blobs are fetched in batches only).
"""
import argparse, collections, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument('--repo', default=os.path.abspath(os.path.join(HERE, '..', '..')))
ap.add_argument('--ref', default=None, help='default: origin/main if present, else HEAD')
ap.add_argument('--out', default=os.path.join(HERE, '..', 'il-diritto-italiano-in-20-grafici.html'))
ap.add_argument('--skip-extract', action='store_true', help='reuse .build/ from a previous run (prep and build only)')
ap.add_argument('--no-fetch', action='store_true', help='never download missing blobs (fail instead)')
ap.add_argument('--steps', default='1234', help='which steps to run (default all: 1234)')
a = ap.parse_args()
B = os.path.join(HERE, '.build')
os.makedirs(B, exist_ok=True)
NOLAZY = dict(os.environ, GIT_NO_LAZY_FETCH='1')   # nothing is fetched behind our back
GIT = ['git', '-C', a.repo, '-c', 'core.quotepath=off']


def git(*args, inp=None):
    return subprocess.run([*GIT, *args], input=inp, check=True, capture_output=True, env=NOLAZY).stdout


ref = a.ref
if not ref:
    ref = 'origin/main' if subprocess.run(['git', '-C', a.repo, 'rev-parse', '--verify', '-q', 'origin/main'], capture_output=True).returncode == 0 else 'HEAD'
sha = git('rev-parse', ref + '^{commit}').decode().strip()
print('ref', ref, sha, flush=True)


def fetch_missing(oids, what, batch=5000):
    """batched fetches for the blobs a partial clone does not have yet (never one at a time)"""
    oids = sorted(set(oids))
    if not oids:
        return
    chk = git('cat-file', '--batch-check', inp=''.join(o + '\n' for o in oids).encode()).decode().split('\n')
    missing = [l.split()[0] for l in chk if l.endswith(' missing')]
    print(f'{what}: {len(oids)} blobs, {len(missing)} to fetch', flush=True)
    if missing and a.no_fetch:
        sys.exit('missing blobs and --no-fetch')
    for i in range(0, len(missing), batch):
        part = missing[i:i + batch]
        print('  fetching', len(part), f'({i + len(part)} of {len(missing)})', flush=True)
        subprocess.run([*GIT, '-c', 'fetch.negotiationAlgorithm=noop', 'fetch', 'origin', '--no-tags', '--no-write-fetch-head',
                        '--recurse-submodules=no', '--filter=blob:none', '--stdin'], input=''.join(m + '\n' for m in part).encode(),
                       check=True, capture_output=True)


def read_blobs(items):
    """yield (path, bytes) for (oid, path) pairs, one blob at a time"""
    p = subprocess.Popen([*GIT, 'cat-file', '--batch'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, env=NOLAZY)
    for oid, path in items:
        p.stdin.write((oid + '\n').encode()); p.stdin.flush()
        head = p.stdout.readline().split()
        if len(head) < 3 or head[1] == b'missing':
            sys.exit('cannot read ' + path)
        data = p.stdout.read(int(head[2])); p.stdout.read(1)
        yield path, data
    p.stdin.close(); p.wait()


def tree(r, *paths, dirs=False):
    """(path, oid, type) of every entry of the tree of r under paths, streamed"""
    lt = subprocess.Popen([*GIT, 'ls-tree', '-r', '-z', *(['-t'] if dirs else []), r, '--', *paths], stdout=subprocess.PIPE, env=NOLAZY)
    buf = b''
    for chunk in iter(lambda: lt.stdout.read(1 << 16), b''):
        buf += chunk
        *ents, buf = buf.split(b'\0')
        for e in ents:
            meta, path = e.split(b'\t', 1)
            _, typ, oid = meta.split()
            yield path.decode('utf-8'), oid.decode(), typ.decode()
    lt.wait()


def clean(s):
    return s.replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').strip()


TRL = re.compile(r'^([A-Z][A-Za-z-]+): (.*)$')


def trailers(body):
    """the trailer block: the "Key: value" lines of the message's last paragraph (a key may repeat)"""
    paras = body.strip('\n').split('\n\n')
    tr = collections.OrderedDict()
    for line in paras[-1].split('\n'):
        m = TRL.match(line)
        if m:
            tr.setdefault(m.group(1), []).append(m.group(2).strip())
    return tr


if not a.skip_extract and '1' in a.steps:
    # ------------------------------------------------------------------ 1. the history, streamed once
    OUTS = {k: open(os.path.join(B, f'log-{k}.tsv'), 'w', encoding='utf-8', newline='\n') for k in
            ['nrm', 'leggi', 'cambill', 'camvote', 'camiter', 'senddl', 'senvote', 'cc', 'ga', 'cdc', 'nim', 'agcm']}
    counts = collections.Counter()      # commits by source and kind
    by_year = collections.Counter()     # commits by source and year of In-force
    lg = subprocess.Popen([*GIT, 'log', sha, '--format=%x1e%H%x1f%ae%x1f%an%x1f%B'], stdout=subprocess.PIPE, env=NOLAZY)
    n = 0

    def emit(rec):
        global n
        rec = rec.decode('utf-8', 'replace').strip('\n')
        if not rec:
            return
        h, ae, an, body = (rec.split('\x1f') + ['', '', '', ''])[:4]
        n += 1
        dom = ae.rsplit('@', 1)[-1].replace('.invalid', '')
        subj = body.split('\n', 1)[0]
        tr = trailers(body)
        g = lambda k: ' ; '.join(tr.get(k, []))
        kind = g('Kind')
        files = g('Files')
        inf = g('In-force')
        counts[f'{dom}|{kind}'] += 1
        by_year[f'{dom}|{inf[:4]}'] += 1
        lines = [l for l in body.split('\n')[1:] if l.strip()]
        line2 = lines[0] if lines else ''
        if dom == 'normattiva':
            OUTS['nrm'].write('\t'.join(clean(x) for x in [h, an, subj, line2 if not TRL.match(line2) else '', inf, g('Enacted'), g('Published'),
                                                           g('Source'), g('ELI'), g('Affecting'), g('Amending-act-candidate'), g('Upstream')[:40]]) + '\n')
        elif dom == 'camera':
            if kind == 'law-record':
                OUTS['leggi'].write('\t'.join(clean(x) for x in [subj, line2, g('Enacted'), g('Published'), files]) + '\n')
            elif kind == 'bill':
                OUTS['cambill'].write('\t'.join(clean(x) for x in [subj, line2, g('Presented'), files]) + '\n')
            elif '/votazioni/' in files:
                OUTS['camvote'].write('\t'.join(clean(x) for x in [subj, inf, files]) + '\n')
            elif kind == 'legislative-process':
                OUTS['camiter'].write('\t'.join(clean(x) for x in [subj, inf, g('Bill'), files]) + '\n')
        elif dom == 'senato':
            if kind == 'bill':
                OUTS['senddl'].write('\t'.join(clean(x) for x in [subj, line2, g('Presented'), g('Became-law'), g('Source'), files]) + '\n')
            elif '/votazioni/' in files:
                OUTS['senvote'].write('\t'.join(clean(x) for x in [subj, inf, files]) + '\n')
        elif dom == 'cortecostituzionale':
            sch = next((f for f in files.split(', ') if f.endswith('/scheda.md')), '')   # the first decision also adds the README
            if sch:
                OUTS['cc'].write('\t'.join(clean(x) for x in [subj, g('Decided'), inf, g('ECLI'), sch]) + '\n')
        elif dom == 'giustizia-amministrativa':
            OUTS['ga'].write('\t'.join(clean(x) for x in [subj, inf, g('Appeal'), files]) + '\n')
        elif dom == 'corteconti':
            OUTS['cdc'].write('\t'.join(clean(x) for x in [subj, inf, g('ECLI'), files]) + '\n')
        elif dom == 'publications.europa':
            OUTS['nim'].write('\t'.join(clean(x) for x in [subj, g('Act-type'), g('Official-journal'), g('Transposes'), inf, files]) + '\n')
        elif dom == 'agcm':
            OUTS['agcm'].write('\t'.join(clean(x) for x in [subj, inf, files]) + '\n')

    buf = b''
    for chunk in iter(lambda: lg.stdout.read(1 << 16), b''):
        buf += chunk
        *recs, buf = buf.split(b'\x1e')
        for r in recs:
            emit(r)
    emit(buf)
    lg.wait()
    for f in OUTS.values():
        f.close()
    json.dump({'commits': n, 'counts': counts, 'by_year': by_year}, open(os.path.join(B, 'counts.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print('commits', n, flush=True)

    # 1b. the files each commit wrote in the Constitution and the four codes (before 17 November 2026 the act folders were
    #     at the top of the repository: both places are read; the layout move itself, a Lexifina commit, is left out)
    CODES = ['regio-decreto/1942/262', 'regio-decreto/1930/1398', 'regio-decreto/1940/1443', 'dpr/1988/447']
    lg = subprocess.Popen([*GIT, 'log', sha, '--format=@@C %H%x1f%an%x1f%(trailers:key=In-force,valueonly,separator=%x20)', '--name-status', '--no-renames', '--',
                           'costituzione', *CODES, *['normativa/' + c for c in CODES]], stdout=subprocess.PIPE, env=NOLAZY)
    cur, nf = None, 0
    with open(os.path.join(B, 'log-files.tsv'), 'w', encoding='utf-8', newline='\n') as out:
        for raw in lg.stdout:
            l = raw.decode('utf-8', 'replace').rstrip('\n')
            if l.startswith('@@C '):
                h, an, inf = (l[4:].split('\x1f') + ['', ''])[:3]
                cur = None if an == 'Lexifina' else (h, an, inf.strip())
                continue
            if l and cur:
                st, _, f = l.partition('\t')
                out.write(f'{cur[0]}\t{cur[1]}\t{cur[2]}\t{st[:1]}\t{f}\n')
                nf += 1
    lg.wait()
    print('file changes in the Constitution and the codes', nf, flush=True)

if not a.skip_extract and '2' in a.steps:
    # ------------------------------------------------------------------ 2. the tree
    acts = collections.Counter()        # files per act folder of normativa/ (articles, annexes, headings)
    arts = collections.Counter()        # art-*.md files per act folder (annex articles counted with their folder)
    added = collections.Counter()       # of which articles numbered with a suffix (art. 3-bis, 12-ter...): added after the original text
    head = {}                           # the heading file (intestazione.md) of every act: its title
    with open(os.path.join(B, 'tree-normativa.tsv'), 'w', encoding='utf-8', newline='\n') as out:
        for path, oid, typ in tree(sha, 'normativa', 'costituzione'):
            p = path.split('/')
            if p[0] == 'normativa' and len(p) >= 5:
                act = '/'.join(p[:4])
                acts[act] += 1
                if re.match(r'art-', p[-1]):
                    arts[act] += 1
                    if re.match(r'art-\d+-[a-z]', p[-1]) and len(p) == 5:
                        added[act] += 1
                if len(p) == 5 and p[-1] == 'intestazione.md':
                    head[act] = oid
                # the four codes and the Constitution, article by article
                if act in ('normativa/regio-decreto/1942/262', 'normativa/regio-decreto/1930/1398', 'normativa/regio-decreto/1940/1443', 'normativa/dpr/1988/447'):
                    out.write(f'F\t{path}\t{oid}\n')
            elif p[0] == 'costituzione':
                out.write(f'F\t{path}\t{oid}\n')
        for act in sorted(acts):
            out.write(f'A\t{act}\t{acts[act]}\t{arts[act]}\t{added[act]}\t{head.get(act, "")}\n')
    print('act folders', len(acts), flush=True)

if not a.skip_extract and '3' in a.steps:
    # ------------------------------------------------------------------ 3. blobs
    blob_of = {p: o for p, o, t in tree(sha, 'data/atti.csv', 'data/versioni.json', 'corpus.json')}
    # 3a. the tables
    fetch_missing(blob_of.values(), 'tables')
    os.makedirs(os.path.join(B, 'repo', 'data'), exist_ok=True)
    for path, data in read_blobs([(o, p) for p, o in blob_of.items()]):
        open(os.path.join(B, 'repo', *path.split('/')), 'wb').write(data)
    # 3b. the scheda.md of every decision of the Corte costituzionale (the kind of proceedings, the judges)
    cc = [(oid, path) for path, oid, typ in tree(sha, 'giurisprudenza/corte-costituzionale') if path.endswith('/scheda.md')]
    fetch_missing([o for o, _ in cc], 'Corte costituzionale schede')
    with open(os.path.join(B, 'blob-cc.tsv'), 'w', encoding='utf-8', newline='\n') as out:
        for path, data in read_blobs(cc):
            t = data.decode('utf-8', 'replace')
            f = dict(re.findall(r'(?m)^- ([^:]+): (.*)$', t))
            out.write('\t'.join(clean(x) for x in [path, f.get('Tipo', ''), f.get('Giudizio', ''), f.get('Relatore', ''), f.get('Presidente', ''),
                                                    f.get('Data della decisione', ''), f.get('Data del deposito', '')]) + '\n')
    print('cc schede', len(cc), flush=True)
    # 3c. the record of every vote of the Camera dei deputati (outcome, votes, confidence, final vote)
    cv = [(oid, path) for path, oid, typ in tree(sha, 'parlamento/atti-parlamentari/camera/votazioni') if path.endswith('.md')]
    fetch_missing([o for o, _ in cv], 'Camera votes')
    KEYS = ['approvato', 'astenuti', 'contrari', 'favorevoli', 'maggioranza', 'presenti', 'votanti', 'richiestaFiducia', 'votazioneFinale', 'votazioneSegreta', 'date', 'type', 'description', 'rif_attoCamera']
    with open(os.path.join(B, 'blob-camvote.tsv'), 'w', encoding='utf-8', newline='\n') as out:
        out.write('\t'.join(['path', 'title'] + KEYS) + '\n')
        for path, data in read_blobs(cv):
            t = data.decode('utf-8', 'replace')
            f = {}
            for k, v in re.findall(r'(?m)^- ([A-Za-z_]+): (.*)$', t):
                f.setdefault(k, v)
            title = t.split('\n', 1)[0].lstrip('# ')
            out.write('\t'.join(clean(x) for x in [path, title] + [f.get(k, '') for k in KEYS]) + '\n')
    print('camera votes', len(cv), flush=True)
    # 3d. the record of every bill of the Senate's open data, 13th to 19th legislature (nature, initiative, status)
    sd = [(oid, path) for path, oid, typ in tree(sha, 'parlamento/schede/senato') if path.endswith('.md')]
    fetch_missing([o for o, _ in sd], 'Senate bills')
    SK = ['Fase', 'Id DDL', 'Id fase', 'Natura', 'Data di presentazione', 'Iniziativa', 'Stato', 'Data dello stato', 'Legge n.', 'Data della legge', 'Ramo']
    with open(os.path.join(B, 'blob-senddl.tsv'), 'w', encoding='utf-8', newline='\n') as out:
        out.write('\t'.join(['path', 'title'] + SK) + '\n')
        for path, data in read_blobs(sd):
            t = data.decode('utf-8', 'replace')
            f = {}
            for k, v in re.findall(r'(?m)^- ([^:]+): (.*)$', t):
                f.setdefault(k, v)
            out.write('\t'.join(clean(x) for x in [path, f.get('Titolo', '')[:400]] + [f.get(k, '') for k in SK]) + '\n')
    print('senate bills', len(sd), flush=True)
    # 3e. the heading (intestazione.md) of every act in normativa/: kind, date, number and title
    hd = [(l.split('\t')[5].strip(), l.split('\t')[1]) for l in open(os.path.join(B, 'tree-normativa.tsv'), encoding='utf-8') if l.startswith('A\t') and l.split('\t')[5].strip()]
    fetch_missing([o for o, _ in hd], 'act headings')
    with open(os.path.join(B, 'blob-head.tsv'), 'w', encoding='utf-8', newline='\n') as out:
        for act, data in read_blobs(hd):
            out.write(act + '\t' + clean(re.sub(r'\s+', ' ', data.decode('utf-8', 'replace')))[:600] + '\n')
    print('act headings', len(hd), flush=True)
    # 3f. the Constitution in force, article by article (which articles are repealed)
    co = [(l.split('\t')[2].strip(), l.split('\t')[1]) for l in open(os.path.join(B, 'tree-normativa.tsv'), encoding='utf-8') if l.startswith('F\tcostituzione/')]
    fetch_missing([o for o, _ in co], 'Constitution')
    with open(os.path.join(B, 'blob-costituzione.jsonl'), 'w', encoding='utf-8', newline='\n') as out:
        for path, data in read_blobs(co):
            out.write(json.dumps({'p': path, 't': data.decode('utf-8', 'replace')}, ensure_ascii=False) + '\n')
    print('Constitution files', len(co), flush=True)

# ------------------------------------------------------------------ 4. prep + build
if '4' not in a.steps:
    sys.exit(0)
env = dict(os.environ, HEAD_SHA=sha)
subprocess.run([sys.executable, '-X', 'utf8', os.path.join(HERE, 'prep.py'), B], check=True, env=env)
subprocess.run([sys.executable, '-X', 'utf8', os.path.join(HERE, 'build.py'), os.path.join(B, 'data.json'), os.path.abspath(a.out)], check=True)
