"""Fixes for italy-law (4,052,201 commits, 4.48 million files at the pin) in the copy of global-law's scripts.

Scale (every language; nothing changes for a small repository):
 1. ingest/extract.py: git log --raw is read in pieces and written to index/changes/<repo>.parquet in row groups, not held
    whole in memory as one string and seven Python lists (italy-law: about 11 million file changes); and where the pinned
    commit is a folder move (a "Paths: data/paths.json" trailer, every moved folder's tree unchanged), its rows are the
    R100 rows git log -M gives, written from git ls-tree, and the log starts at its parent (git's rename search over
    3.3 million moved files needed ~8 GB at its peak);
 2. ingest/trailers.py: the same for index/commits/<repo>.parquet (4 million commit messages);
 3. map_moved.py: a moved folder's files at any depth are mapped (italy-law moved the act-type folders, legge/ to
    normativa/legge/, so a file's parent folder is never the moved one), a moved root file is mapped too (atti.csv), and
    the table is rewritten in batches;
 4. LE_SCAN_PATHS (space-separated folder prefixes, e.g. "normativa/ costituzione/"): when set, the scans of the files at
    the pin (ingest/textscan.py, ingest/refscan.py, ingest/headings.py, detectors/late_extension.py through is_law_file;
    detectors/placeholder_ref.py, dup_labels.py, dead_fine.py through ls-tree; currency_scan.py and notes_scan.py through
    git grep) read only those folders. Unset, every file is read, as before;
 5. ingest/headings.py: reads only law files (is_law_file) and writes in row groups.
Italian (normattiva text, language "it"):
 6. ingest/refscan.py: the folders a code is split into (codice-civile/art-0000-0499/) are one act (act_of);
 7. ingest/refscan.py: another act named after a reference by its abbreviation ("del d.P.R. 22 dicembre 1986, n. 917",
    "del D.Lgs.", "del D.M.", "del R.D.", "del regio decreto", "del D.P.C.M.", "del t.u."), as a code ("art. 2043 c.c.",
    "c.p.", "c.p.c.", "c.p.p."), or as the act just cited ("del citato decreto", "del predetto", "suddetto", "medesimo",
    "stesso", "richiamato" + an act's name) is another act, not this one;
 8. ingest/textscan.py: "a tutto il 31 dicembre 2020", "fino a tutto il ...", "sino a tutto il ..." are time limits, and
    "entro il termine del 31 dicembre 2021" a deadline;
 9. detectors/placeholder_ref.py: an article heading with a Latin suffix ("Art. 7-bis.", "Art. 3 ter") is a heading, so
    "Art. 7-bis." over "((ARTICOLO ABROGATO DAL D.P.R. ...))" is a repealed placeholder, as "Art. 7." over it already was.
    python -X utf8 patch_it2.py <scripts dir>      (each change carries a patch_it2 marker; one in place is skipped)"""
import sys
from pathlib import Path

S = Path(sys.argv[1])


def patch(rel, pairs):
    p = S / rel
    s = p.read_text(encoding="utf-8")
    for name, a, b, marker in pairs:
        if marker in s:
            print("in place:", name)
            continue
        if callable(a):
            s2 = a(s)
            if s2 is None:
                raise SystemExit(f"not found: {name}")
            s = s2
        elif a in s:
            s = s.replace(a, b, 1)
        else:
            raise SystemExit(f"not found: {name}")
        print("patched:", name)
    p.write_text(s, encoding="utf-8", newline="\n")


def between(start, end, new):
    def f(s):
        i = s.find(start)
        j = s.find(end, i)
        if i < 0 or j < 0:
            return None
        return s[:i] + new + s[j + len(end):]
    return f


EXTRACT = '''def corpus_changes(c: dict) -> tuple[str, int, float]:
    # patch_it2: streamed. git log's output is read in pieces and written in row groups, not held whole: italy-law's
    # 4.05 million commits did not fit in memory as one string and seven Python lists
    import subprocess
    from common import FLAGS
    lower_priority()
    t0 = time.time()
    repo = CORPUS / f"{c['repo']}.git"
    names = ("commit", "author_date", "status", "old_blob", "new_blob", "old_path", "path")
    schema = pa.schema([(k, pa.string()) for k in names + ("corpus",)])
    (INDEX / "changes").mkdir(parents=True, exist_ok=True)
    w = pq.ParquetWriter(INDEX / "changes" / f"{c['repo']}.parquet", schema, compression="zstd")
    st = {"cols": {k: [] for k in names}, "n": 0}

    def flush():
        cols = st["cols"]
        k = len(cols["commit"])
        if k:
            w.write_table(pa.table({**cols, "corpus": [c["path"]] * k}, schema=schema))
            st["n"] += k
            st["cols"] = {x: [] for x in names}

    def parse(rec: str):
        head, _, raw = rec.partition("\\n")
        parts = head.split("\\x1f")
        sha, date = parts[0], parts[2]
        toks = raw.lstrip("\\n").split("\\x00")
        i = 0
        while i < len(toks):
            tok = toks[i].lstrip("\\n")
            if not tok.startswith(":"):
                i += 1
                continue
            f = tok[1:].split()
            s_ = f[4]
            if s_[0] in "RC":
                old, new = toks[i + 1], toks[i + 2]; i += 3
            else:
                old = new = toks[i + 1]; i += 2
            cols = st["cols"]
            cols["commit"].append(sha); cols["author_date"].append(date); cols["status"].append(s_)
            cols["old_blob"].append(f[2]); cols["new_blob"].append(f[3])
            cols["old_path"].append(old); cols["path"].append(new)
            if len(cols["commit"]) >= 500_000:
                flush()

    # patch_it2: the pinned commit, when it is the move itself (a "Paths: data/paths.json" trailer, and every moved
    # folder's tree identical before and after), is written from git ls-tree as the R100 rows git log -M gives, and the
    # log starts at its parent: git's rename search over italy-law's 3.3 million moved files took ~8 GB at its peak
    def gout(*a):
        return subprocess.run(["git", "-c", "core.quotepath=false", *a], cwd=repo, capture_output=True, creationflags=FLAGS)
    start = c["sha"]
    par, adate, body = gout("log", "-1", "--format=%P%x1f%aI%x1f%B", c["sha"]).stdout.decode("utf-8", "replace").split("\\x1f", 2)
    pj = gout("show", f"{c['sha']}:data/paths.json")
    moved = {}
    if pj.returncode == 0 and "\\nPaths: data/paths.json" in body and len(par.split()) == 1:
        import json as _json
        moved = {k: v for k, v in _json.loads(pj.stdout.decode("utf-8")).get("paths", {}).items() if k != v}
        par = par.strip()
        if not moved or not all(gout("rev-parse", f"{par}:{k}").stdout == gout("rev-parse", f"{c['sha']}:{v}").stdout
                                and gout("rev-parse", f"{par}:{k}").returncode == 0 for k, v in moved.items()):
            moved = {}
    if moved:
        inv = {v: k for k, v in moved.items()}
        lt = subprocess.Popen(["git", "-c", "core.quotepath=false", "ls-tree", "-r", "-z", "--format=%(objectname) %(path)",
                               c["sha"], "--", *moved.values()], cwd=repo, stdout=subprocess.PIPE, creationflags=FLAGS)
        rest = b""
        while True:
            chunk = lt.stdout.read(1 << 22)
            if not chunk:
                break
            items = (rest + chunk).split(b"\\x00")
            rest = items.pop()
            for it in items:
                blob, path = it.decode("utf-8", "replace").split(" ", 1)
                v = path
                while v not in inv:
                    v = v.rsplit("/", 1)[0]
                cols = st["cols"]
                cols["commit"].append(c["sha"]); cols["author_date"].append(adate); cols["status"].append("R100")
                cols["old_blob"].append(blob); cols["new_blob"].append(blob)
                cols["old_path"].append(inv[v] + path[len(v):]); cols["path"].append(path)
                if len(cols["commit"]) >= 500_000:
                    flush()
        if lt.wait():
            raise RuntimeError("git ls-tree failed")
        r = gout("diff-tree", "-r", "-z", "--no-renames", "--raw", "--no-abbrev", "--no-commit-id", par, c["sha"], "--", ".",
                 *[f":(exclude){x}" for x in list(moved) + list(moved.values())])
        parse(f"{c['sha']}\\x1f{par}\\x1f{adate}\\x1f\\n" + r.stdout.decode("utf-8", "replace"))
        start = par
    p = subprocess.Popen(["git", "-c", "core.quotepath=false", "log", "--raw", "--no-abbrev", "-M", "-z",
                          "--format=%x1e%H%x1f%P%x1f%aI%x1f%s", start], cwd=repo, stdout=subprocess.PIPE,
                         creationflags=FLAGS)
    pend, first = [], True
    while True:
        chunk = p.stdout.read(1 << 24)
        if not chunk:
            break
        if b"\\x1e" not in chunk:
            pend.append(chunk)
            continue
        recs = (b"".join(pend) + chunk).split(b"\\x1e")
        pend = [recs.pop()]
        for r in recs:
            if first:  # what comes before the first record separator
                first = False
                continue
            parse(r.decode("utf-8", errors="replace"))
        if len(st["cols"]["commit"]) >= 500_000:
            flush()
    tail = b"".join(pend)
    if tail and not first:
        parse(tail.decode("utf-8", errors="replace"))
    if p.wait():
        raise RuntimeError(f"git log failed in {repo}")
    flush()
    w.close()
    return c["repo"], st["n"], time.time() - t0
'''

TRAILERS = '''def one(c: dict):
    # patch_it2: streamed, in row groups (italy-law: 4 million commit messages)
    import subprocess
    from common import FLAGS
    lower_priority()
    names = ("commit", "author_date", "commit_date", "subject", "trailers")
    schema = pa.schema([(k, pa.string()) for k in names + ("corpus",)])
    (INDEX / "commits").mkdir(parents=True, exist_ok=True)
    w = pq.ParquetWriter(INDEX / "commits" / f"{c['repo']}.parquet", schema, compression="zstd")
    st = {"rows": {k: [] for k in names}, "n": 0}

    def flush():
        rows = st["rows"]
        k = len(rows["commit"])
        if k:
            w.write_table(pa.table({**rows, "corpus": [c["path"]] * k}, schema=schema))
            st["n"] += k
            st["rows"] = {x: [] for x in names}

    def parse(rec: str):
        sha, ad, cd, body = rec.split("\\x1f", 3)
        t: dict[str, list[str]] = {}
        for line in body.splitlines():
            m = TR.match(line.strip())
            if m:
                t.setdefault(m.group(1), []).append(m.group(2).strip()[:2000])
        rows = st["rows"]
        rows["commit"].append(sha); rows["author_date"].append(ad); rows["commit_date"].append(cd)
        rows["subject"].append(body.split("\\n", 1)[0][:500]); rows["trailers"].append(json.dumps(t, ensure_ascii=False))
        if len(rows["commit"]) >= 200_000:
            flush()

    p = subprocess.Popen(["git", "-c", "core.quotepath=false", "log", "--format=%x1e%H%x1f%aI%x1f%cI%x1f%B", c["sha"]],
                         cwd=CORPUS / f"{c['repo']}.git", stdout=subprocess.PIPE, creationflags=FLAGS)
    pend, first = [], True
    while True:
        chunk = p.stdout.read(1 << 24)
        if not chunk:
            break
        if b"\\x1e" not in chunk:
            pend.append(chunk)
            continue
        recs = (b"".join(pend) + chunk).split(b"\\x1e")
        pend = [recs.pop()]
        for r in recs:
            if first:
                first = False
                continue
            parse(r.decode("utf-8", errors="replace"))
    tail = b"".join(pend)
    if tail and not first:
        parse(tail.decode("utf-8", errors="replace"))
    if p.wait():
        raise RuntimeError("git log failed for " + c["repo"])
    flush()
    w.close()
    return c["repo"], st["n"]
'''

MAP_MOVED = '''# patch_it2: a moved folder's files at any depth (italy-law moved legge/ to normativa/legge/: a file's parent folder is
# never the moved one), a moved root file (atti.csv), and the table rewritten in batches (11 million rows)
import pyarrow.parquet as pq
_keys = sorted(moved, key=len, reverse=True)


def m(p):
    if not p:
        return p
    if p in moved:
        return moved[p]
    head = p
    while "/" in head:
        head = head.rsplit("/", 1)[0]
        if head in moved:
            return moved[head] + p[len(head):]
    return p


n = 0
tmp = f + ".new"
src = pq.ParquetFile(f)
w = pq.ParquetWriter(tmp, src.schema_arrow, compression="zstd")
for b in src.iter_batches(batch_size=500_000):
    t = pa.Table.from_batches([b])
    for c in ("path", "old_path"):
        vals = t.column(c).to_pylist()
        new = [m(v) for v in vals]
        n += sum(a != b_ for a, b_ in zip(vals, new))
        t = t.set_column(t.schema.get_field_index(c), c, pa.array(new, pa.string()))
    w.write_table(t)
w.close()
src.close()
os.replace(tmp, f)
print(f"map_moved: {len(moved)} folders, {n} paths rewritten to their folder since the move")
'''

HEADINGS = """    # patch_it2: only law files (is_law_file, LE_SCAN_PATHS), written in row groups
    from textscan import SCAN_PATHS
    pre = " or ".join(f"starts_with(path, '{x}')" for x in SCAN_PATHS) or "true"
    blobs = list(dict.fromkeys(b for (b, p) in con.sql(f\"\"\"select new_blob, path from '{(INDEX/'changes'/(c['repo']+'.parquet')).as_posix()}'
        where left(status,1) <> 'D' and ({pre})\"\"\").fetchall() if is_law_file(p)))
    (INDEX / "headings").mkdir(parents=True, exist_ok=True)
    schema = pa.schema([("blob", pa.string()), ("heading", pa.string()), ("head", pa.string())])
    w = pq.ParquetWriter(INDEX / "headings" / f"{c['repo']}.parquet", schema, compression="zstd")
    H = {"blob": [], "heading": [], "head": []}
    for sha, text in stream(repo, blobs):
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        H["blob"].append(sha)
        H["heading"].append(lines[0].lstrip("#").strip()[:300] if lines else "")
        H["head"].append(text[:1500])
        if len(H["blob"]) >= 100_000:
            w.write_table(pa.table(H, schema=schema)); H = {"blob": [], "heading": [], "head": []}
    w.write_table(pa.table(H, schema=schema)); w.close()
"""

IT_OTHER = r'''# patch_it2: an Italian reference that is not to one of this act's own articles: inside quoted text (an amendment's new
# wording, a note quoting another act), "con l'art. 13" (a note naming the amending act's article), "il citato articolo 9",
# "(Art. 173.)" in struttura.md (the article a chapter starts at), or followed, in its clause, by another act's name
# ("articoli 4 e 5 della legge n. 241 del 1990", "articolo 7, comma 3, quarto periodo, del decreto-legge ...") before any
# "presente legge"
IT_ACT_WORD = re.compile(r"(?i)(?:\b(?:del|della|dello|dei|degli|delle|al|alla|allo|ai|agli|alle|dal|dalla|dallo|dai|dagli|dalle|"
                         r"nel|nella|nello|nei|negli|nelle|di|il|la|lo|i|gli|le)\s+|\b[dl]['’]\s*)"
                         r"(?:(?P<own>present\w*|quest\w*)\s+|(?:citat|predett|suddett|medesim|stess|richiamat|menzionat|succitat|sopracitat|anzidett)\w*\s+)?"
                         r"(?:legg[ei]|decret\w*|d\.\s?P\.\s?R\.|d\.\s?lgs\.?|d\.\s?l\.|d\.\s?m\.|d\.\s?p\.\s?c\.\s?m\.|r\.\s?d\.|regi\w*\s+decret\w*|"
                         r"codic[ei]|testo\s+unico|t\.\s?u\.|regolament\w*|direttiv\w*|trattat\w*|convenzion\w*|costituzion\w*|statut\w*|"
                         r"accord\w*|protocoll\w*|l\.)(?!\w)")


def it_other(body: str, end: int, before: str) -> bool:
    if before.count('"') % 2 == 1 or before.count("“") > before.count("”"):
        return True
    if re.search(r"(?i)(?:\bcon\s+l['’]\s*|\b(?:citat|predett|suddett|medesim|stess|richiamat|menzionat|succitat|sopracitat|anzidett)\w*\s+)$", before):
        return True
    if re.search(r"\(\s*$", before) and re.match(r"\s*\.?\s*\)", body[end:end + 6]):
        return True
    seg = re.split(r"[;\n]|\.\s+(?=[A-Z])", body[end:end + 300], maxsplit=1)[0]
    a = IT_ACT_WORD.search(seg)
    return bool(a) and not a.group("own")'''

patch("ingest/extract.py", [
    ("streamed changes", between("def corpus_changes(c: dict) -> tuple[str, int, float]:\n",
                                 '    return c["repo"], len(cols["commit"]), time.time() - t0\n', EXTRACT), None, "# patch_it2: streamed."),
])
patch("ingest/trailers.py", [
    ("streamed commits", between("def one(c: dict):\n", '    return c["repo"], len(rows["commit"])\n', TRAILERS), None,
     "# patch_it2: streamed"),
])
patch("map_moved.py", [
    ("moved folders at any depth, streamed",
     between('t = duckdb.sql(f"select * from \'{f.replace(chr(92), \'/\')}\'").arrow()\n',
             'print(f"map_moved: {len(moved)} folders, {n} paths rewritten to their folder since the move")\n', MAP_MOVED),
     None, "# patch_it2: a moved folder"),
])
patch("ingest/textscan.py", [
    ("LE_SCAN_PATHS in is_law_file",
     'def is_law_file(path: str) -> bool:\n    p = path.lower()\n    return p.endswith((".md", ".txt")) and p.rsplit("/", 1)[-1] not in SKIP and not p.startswith(("docs/", "tools/", "tests/", ".github/"))\n',
     '# patch_it2: LE_SCAN_PATHS ("normativa/ costituzione/") limits the scans of the files at the pin to those folders\n'
     'SCAN_PATHS = tuple(__import__("os").environ.get("LE_SCAN_PATHS", "").split())\n\n\n'
     'def is_law_file(path: str) -> bool:\n    p = path.lower()\n    return p.endswith((".md", ".txt")) and p.rsplit("/", 1)[-1] not in SKIP and not p.startswith(("docs/", "tools/", "tests/", ".github/")) \\\n'
     '        and (not SCAN_PATHS or path.startswith(SCAN_PATHS))\n',
     "# patch_it2: LE_SCAN_PATHS"),
    ("Italian 'a tutto il', 'entro il termine del'",
     'IT_UNTIL = (r"entro\\s+e\\s+non\\s+oltre|non\\s+oltre|entro|',
     'IT_UNTIL = (r"entro\\s+il\\s+termine\\s+(?:ultimo\\s+)?(?:del|dell[\'’])(?#patch_it2)|(?:(?:fino|sino)\\s+)?a\\s+tutto(?=\\s+il\\s)|entro\\s+e\\s+non\\s+oltre|non\\s+oltre|entro|',
     "(?#patch_it2)"),
])
LSTREE = '"ls-tree", "-r", "-z", "--format=%(objectname) %(path)", c["sha"]]'
LSTREE2 = '"ls-tree", "-r", "-z", "--format=%(objectname) %(path)", c["sha"], "--", *__import__("os").environ.get("LE_SCAN_PATHS", "").split()]'
for f in ("detectors/placeholder_ref.py", "detectors/dup_labels.py", "detectors/dead_fine.py"):
    patch(f, [("LE_SCAN_PATHS in ls-tree", LSTREE, LSTREE2, "LE_SCAN_PATHS")])
patch("detectors/currency_scan.py", [
    ("LE_SCAN_PATHS in git grep", 'pat_for(c), c["sha"], "--", "*.md"]',
     'pat_for(c), c["sha"], "--", *([p + "*.md" for p in __import__("os").environ.get("LE_SCAN_PATHS", "").split()] or ["*.md"])]',
     "LE_SCAN_PATHS"),
])
patch("detectors/currency_scan.py", [
    ("Italian words that are not currencies",
     '\n\n# a currency that is dead in one jurisdiction only',
     '\n# patch_it2: in Italian "DM" is a decreto ministeriale ("DM 12 marzo 2001"), "franco" a word ("terreno franco", "franco\n'
     '# destino"), "lati" sides, "inti" in "interventi" split by the layout, and dinars named today are mostly current\n'
     '# (Tunisian, Algerian, Jordanian)\n'
     'NOT_CURRENCY["it"] = (r"(?-i:francos?|FRANCOS?)\\b(?!\\s+suizos?)|", r"(?-i:\\bDM\\b)|", r"intis?\\b|", r"\\blat[uůi]\\b|", r"|dinara?(?!ic)")\n'
     '\n\n# a currency that is dead in one jurisdiction only',
     'NOT_CURRENCY["it"] = '),
])
patch("detectors/notes_scan.py", [
    ("LE_SCAN_PATHS in git grep", 'PAT, c["sha"], "--"]', 'PAT, c["sha"], "--", *__import__("os").environ.get("LE_SCAN_PATHS", "").split()]',
     "LE_SCAN_PATHS"),
])
patch("ingest/headings.py", [
    ("law files only, row groups",
     between("    blobs = [b for (b,) in con.sql(",
             '    pq.write_table(pa.table(H), INDEX / "headings" / f"{c[\'repo\']}.parquet", compression="zstd")\n',
             HEADINGS),
     None, "# patch_it2: only law files"),
])
patch("ingest/refscan.py", [
    ("a code's article folders are one act",
     'def act_of(path: str) -> str:\n    return path.rsplit("/", 1)[0] if "/" in path else ""\n',
     'def act_of(path: str) -> str:\n    a = path.rsplit("/", 1)[0] if "/" in path else ""\n'
     '    if _LANG["v"] == "it":  # patch_it2: codice-civile/art-0000-0499/ and the other folders a code is split into are one act\n'
     '        a = re.sub(r"/art-\\d{4}-\\d{4}$", "", a)\n'
     '    return a\n',
     "# patch_it2: codice-civile"),
    ("Italian: another act by abbreviation, as a code, or as the act just cited",
     '                          r"(?!presente|medesim|stess)(?:Legge|Decreto|',
     '                          r"(?!presente)(?:(?:citat|predett|suddett|medesim|stess|richiamat|menzionat|succitat|sopracitat)[oaie]\\s+(?:decreto|legge|d\\.|testo|codice|regolamento|direttiva|trattato|convenzione|accordo|t\\.\\s?u\\.|provvediment|atto|r\\.\\s?d\\.|regio)(?#patch_it2)|'
     'd\\.\\s?P\\.\\s?R\\.|d\\.\\s?lgs\\.?|d\\.\\s?lg\\.|d\\.\\s?m\\.|d\\.\\s?p\\.\\s?c\\.\\s?m\\.|r\\.\\s?d\\.|r\\.\\s?d\\.\\s?l\\.|regio\\s+decreto|t\\.\\s?u\\.|"\n'
     '                          r"codice|testo\\s+unico|trattato|regolamento|direttiva|convenzione|accordo|protocollo|legge|decreto|Legge|Decreto|',
     "(?#patch_it2)"),
    ("Italian: a code by its abbreviation after the article",
     '    if _LANG["v"] == "it" and EXT_AFTER_IT.match(tail):  # patch_it\n        return True\n',
     '    if _LANG["v"] == "it" and EXT_AFTER_IT.match(tail):  # patch_it\n        return True\n'
     '    if _LANG["v"] == "it" and re.match(r"(?i)^[\\s,-]*(?:bis|ter|quater|quinquies|sexies|septies|octies|novies|decies)?\\s*,?\\s*(?:(?:primo|secondo|terzo|quarto|quinto|sesto|ultimo)\\s+comma\\s*,?\\s*|comma\\s+\\d+\\s*,?\\s*)?'
     '(?:c\\.\\s?c\\.|c\\.\\s?p\\.|c\\.\\s?p\\.\\s?c\\.|c\\.\\s?p\\.\\s?p\\.|cod\\.\\s?(?:civ|pen|proc)|disp\\.\\s?att\\.)", tail):\n'
     '        return True  # patch_it2: "art. 2043 c.c.", "art. 416-bis c.p."\n',
     "# patch_it2: \"art. 2043 c.c.\""),
    ("Italian: references that are not to this act's own articles (definition)",
     "\n\ndef refs(text: str):\n",
     "\n\n" + IT_OTHER + "\n\ndef refs(text: str):\n",
     "def it_other("),
    ("Italian: references that are not to this act's own articles (read)",
     '            if _LANG["v"] == "ru" and ru_other_act(body, m.end()):  # RU_CLAUSE\n                continue\n',
     '            if _LANG["v"] == "ru" and ru_other_act(body, m.end()):  # RU_CLAUSE\n                continue\n'
     '            if _LANG["v"] == "it" and it_other(body, m.end(), before):  # patch_it2\n                continue\n',
     "it_other(body, m.end(), before):  # patch_it2"),
])
patch("detectors/placeholder_ref.py", [
    ("Italian headings with a Latin suffix",
     '    body = [l for l in lines if not l.startswith("#")]\n    labels = [l for l in body if LABEL.match(l)]\n',
     '    body = [l for l in lines if not l.startswith("#")]\n'
     '    if _RS._LANG["v"] == "it":  # patch_it2: "Art. 7-bis." is a heading, as "Art. 7." is\n'
     '        body = [re.sub(r"(?i)^(\\W{0,3}art\\.?\\s*\\d{1,4})[\\s-]*(?:bis|ter|quater|quinquies|sexies|septies|octies|novies|nonies|decies)\\b", r"\\1", l) for l in body]\n'
     '    labels = [l for l in body if LABEL.match(l)]\n',
     "# patch_it2: \"Art. 7-bis.\""),
])
