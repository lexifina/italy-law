"""Hand-check helper: for each flag in data/flags.csv, whether it stands in an article's text or in Normattiva's update
notes (after the '-----' line that opens "AGGIORNAMENTO (n)"), and whether it is in an act folder held twice.
    python -X utf8 notes_split.py <flags.csv> <bare repo> <commit>"""
import collections, csv, re, subprocess, sys
F, G, N = sys.argv[1], sys.argv[2], sys.argv[3]
rows = list(csv.DictReader(open(F, encoding="utf-8")))
paths = sorted({r["path"] for r in rows if r["path"]})
out = subprocess.run(["git", "-C", G, "cat-file", "--batch"], input=("\n".join(f"{N}:{p}" for p in paths) + "\n").encode(),
                     capture_output=True).stdout
T, pos = {}, 0
for p in paths:
    nl = out.index(b"\n", pos); h = out[pos:nl].split()
    if len(h) < 3 or h[1] != b"blob":
        pos = nl + 1; continue
    n = int(h[2]); T[p] = out[nl + 1:nl + 1 + n].decode("utf-8", "replace"); pos = nl + 2 + n
c = collections.Counter()
for r in rows:
    t0 = T.get(r["path"], "")
    m0 = re.search(r"(?m)^-{5,}\s*$", t0)
    det = r["detector"]
    if det in ("dead_currency", "publisher_flag") and r["reference"].isdigit():
        ln = int(r["reference"])
        cutline = t0[:m0.start()].count("\n") + 1 if m0 else None
        where = "notes" if cutline and ln > cutline else "text"
    else:
        t = re.sub(r"\s+", " ", t0)
        cut = len(re.sub(r"\s+", " ", t0[:m0.start()])) if m0 else None
        s = re.sub(r"\s+", " ", r["summary"])
        s = s[len(s) // 3: len(s) // 3 + 60] if len(s) > 90 else s[:60]
        i = t.find(s) if s else -1
        where = "?" if i < 0 else ("notes" if cut is not None and i >= cut else "text")
    c[(det, where)] += 1
for k in sorted(c):
    print(k, c[k])
