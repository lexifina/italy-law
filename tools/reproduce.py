"""Writes data/versioni.json, corpus.json and REPRODUCE.md into the Italian law repository, from the facts of the build
that made it. Called by build.py; kept apart so the record of how the repository was made reads as one document.

The results of the checks (check_repo.py --write, test_repo.py --record and build.py --verify-rebuild) are read from
verification.json next to this file. They describe the build before the one that writes this file, from the same data;
a rebuild with the same data and the same verification.json gives the same hashes."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _v(cmd: list[str]) -> str:
    try:
        out = subprocess.run(cmd, capture_output=True, text=True)
        return (out.stdout or out.stderr).strip().split('\n')[0]
    except OSError:
        return '?'


def write_manifest(repo: Path, built: list[dict], today: str):
    """Every version the text comes from, with the file it was read from and that file's sha256."""
    out = {'built': today, 'source': 'https://dati.normattiva.it', 'acts': [{
        'path': b['act']['path'], 'act': b['act']['short'], 'citation': b['self']['cite'] if b['self'] else '',
        'versions': [{'from': v['from'], 'file': v['member'], 'sha256': v['sha256'],
                      'eli': f'https://www.normattiva.it/{v["eli"]}' if v['eli'] else None}
                     for v in b['versions'] if v['from'] <= today],
    } for b in built]}
    (repo / 'data').mkdir(exist_ok=True)
    (repo / 'data' / 'versioni.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8',
                                                 newline='\n')


def write_corpus(repo: Path, built: list[dict], log: list[dict], today: str):
    days = sorted(e['day'] for e in log)
    corpus = {
        'corpus': 'it/national/acts',
        'name': 'Italian law: the Constitution, every legge costituzionale, L. 300/1970, L. 241/1990, D.Lgs. 196/2003 '
                'and D.Lgs. 82/2005, from Normattiva\'s multivigente text',
        'acts': [b['act']['short'] for b in built],
        'history_from': days[0],
        'built': today,
        'dates': {'commit': 'in-force', 'other_trailers': ['Enacted', 'Published'],
                  'time': '12:00 Europe/Rome (UTC+1, UTC+2 in summer time); in force before 1970: 1970-01-01T00:00Z '
                          'plus one second per commit, real day in In-force'},
        'scope': {
            'trailer': 'Applies',
            'when_absent': 'this corpus records no scope notes (no commit carries Applies:); the absence is not a '
                           'statement that the change reaches every case',
            'default_reach': {
                'rule': 'no retroactivity',
                'meaning': 'a law provides only for the future and has no retroactive effect, unless it says otherwise '
                           '(the rule binds ordinary interpretation, not the legislator, except in criminal law, where '
                           'no one may be punished under a law that was not in force when the act was committed)',
                'authority': 'Disposizioni sulla legge in generale, art. 11 ("La legge non dispone che per l\'avvenire: '
                             'essa non ha effetto retroattivo."); Costituzione, art. 25, secondo comma ("Nessuno può '
                             'essere punito se non in forza di una legge che sia entrata in vigore prima del fatto '
                             'commesso.")',
                'decided_here': False}},
        'tool': 'tools/vigente.py',
        'in_force_trailer': 'In-force',
        'record_to': max(d for d in days if d <= today),
    }
    (repo / 'corpus.json').write_text(json.dumps(corpus, ensure_ascii=False, indent=2) + '\n', encoding='utf-8',
                                      newline='\n')


def write_reproduce(repo: Path, built: list[dict], log: list[dict], tags: dict, requests: list[dict], today: str,
                    future: bool):
    write_corpus(repo, built, log, today)
    blob = _v(['git', 'hash-object', str(HERE / 'build.py')])
    import lxml.etree
    lxmlv = '.'.join(str(x) for x in lxml.etree.LXML_VERSION[:3])
    ver = json.loads((HERE / 'verification.json').read_text(encoding='utf-8')) if (HERE / 'verification.json').exists() else {}
    zips = sorted({r['file'] for r in requests}, key=lambda p: p.name)
    metas = {z.name: json.loads(z.with_suffix('.json').read_text()) for z in zips if z.with_suffix('.json').exists()}
    kinds: dict[str, int] = {}
    for e in log:
        kinds[e['kind']] = kinds.get(e['kind'], 0) + 1
    why: dict[str, int] = {}
    listed: dict[str, list[str]] = {}
    for b in built:
        for ch in b['changes']:
            if ch['from'] > today:
                continue
            for k, w in ch['why'].items():
                w2 = w.split(':')[0]
                why[w2] = why.get(w2, 0) + 1
                if w2 in ('no act in the record or the update history', 'two or more acts possible', 'history',
                          'only act of this version'):
                    u = ch['cur']['units'].get(k) or ch['prev']['units'][k]
                    extra = ''
                    if k in ch['cands']:
                        extra = ' (' + ', '.join(sorted({l['label'] for l in ch['cands'][k]})) + ')'
                    listed.setdefault(w2, []).append(f'{b["act"]["short"]} {ch["from"]}: {u["label"]}{extra}')
    n_clamped = sum(1 for e in log if e['clamped'])
    authors = sorted({e['author'] for e in log})
    chk, det, smoke = ver.get('check', {}), ver.get('rebuild', {}), ver.get('smoke', {})
    rows = '\n'.join(
        f'| {b["act"]["short"]} | `{b["act"]["path"]}/` | {len([v for v in b["versions"] if v["from"] <= today])} | '
        f'{b["versions"][0]["from"]} | {len(b["versions"][-1]["units"])} |' for b in built)
    data_rows = '\n'.join(
        f'| `{z}` | {m.get("retrieved", "")} | {m.get("bytes", "")} | `{m.get("sha256", "")}` |' for z, m in metas.items())
    check_line = (f'{chk["versions"]} versions checked ({chk["files"]} files): **{chk["mismatches"]} mismatches** byte for '
                  f'byte; {chk["wordcheck"]} versions word for word ({chk["words"]} words) against every word of the '
                  f'official XML: **{chk["word_mismatches"]} mismatches**. Against Normattiva\'s JSON export of the same '
                  f'versions (a second manifestation, with its own headings and numbering), the words agree as a '
                  f'multiset in {chk["json_identical_words"]} of {chk["json_versions"]} versions; the differences are '
                  'in how the JSON repeats headings, prints the preamble inside article 1, escapes `<` and `>`, and '
                  'spells a few identifiers (`nonies`/`novies`). It is information, not a pass/fail test.'
                  if chk else '(not yet run)')
    rebuild_line = (f'A second build from the same cache into an empty folder gave the same history: the last law commit '
                    f'was `{det["history_tip"]}` in both, and every one of the {det["commits"]} law commits and '
                    f'{det["tags"]} tags had the same hash.' if det.get('identical') else '(not yet run)')
    smoke_lines = ('\n'.join(f'   - {"pass" if r["ok"] else "FAIL"}: {r["test"]}: {r["detail"]}' for r in smoke['results'])
                   if smoke else '   (not yet run)')

    def items(w):
        xs = listed.get(w, [])
        return '\n'.join(f'  - {x}' for x in xs) if xs else '  - (none)'
    text = f"""# How this repository was made

Everything needed to rebuild this repository exactly, from the same data: the sources, the commands in order, the
software, the decisions made by hand, and what an AI model did and did not do. Built {today} from data retrieved
{', '.join(sorted({m.get('retrieved', '') for m in metas.values()}))}.

## Sources

Normattiva Open Data, <https://dati.normattiva.it>, run by the Istituto Poligrafico e Zecca dello Stato for the
Presidenza del Consiglio dei Ministri, under CC BY 4.0 (see LICENSE). Its API is documented by the portal itself
(`/assets/come_fare_per/API_Normattiva_OpenData.pdf` and `openapi-bff-opendata.json`); base address
`https://api.normattiva.it/t/normattiva.api/bff-opendata/v1/api/v1`. Robots: `www.normattiva.it/robots.txt` disallows
only `/ricerca/` and `/mfr/ricerca/`, and names no AI crawler; the build does not touch www.normattiva.it at all.

- Single acts: the documented asynchronous export. `POST ricerca-asincrona/nuova-ricerca` with
  `{{"formato": "AKN" or "JSON", "tipoRicerca": "A", "richiestaExport": "M", "parametriRicerca": {{...}}}}` returns a token
  (no e-mail address is needed); `GET ricerca-asincrona/check-status/<token>` is polled every 10 seconds (and
  `PUT ricerca-asincrona/conferma-ricerca` sent if the export waits for confirmation) until it is ready;
  `GET collections/download/collection-asincrona/<token>` returns the zip. `richiestaExport: "M"` asks for the
  multivigente export (every version); the `modalita` field takes only C or R.
- The constitutional laws: the prepared collection "Leggi costituzionali",
  `GET collections/download/collection-preconfezionata?nome=Leggi%20costituzionali&formato=AKN|JSON&formatoRichiesta=M`.
- Requests: 6 sources x 2 formats = 12 exports, each one request to start it (or one GET for the prepared
  collection), a few status polls, and one download. One request at a time, with a 600-second timeout, the User-Agent
  `Lexifina-gitlaw/1.0 (+https://lexifina.com; legal research)` and gzip.

The data, cached in `scripts/italy-law/.cache/zips/` (self-gitignored):

| File | Retrieved | Bytes | sha256 |
| --- | --- | ---: | --- |
{data_rows}

Each zip has one folder per act and one file per version: `<GU date>_<codice redazionale>_ORIGINALE_V0.xml` and
`..._VIGENZA_<day the version applies from>_V<n>.xml`. `data/versioni.json` lists every version used, with its
file name, sha256 and ELI address.

## The acts

| Act | Folder | Versions | First in force | Provisions now |
| --- | --- | ---: | --- | ---: |
{rows}

## Commands, in order

```sh
# 1. Fetch (online; everything is cached) and build into an empty folder or an existing clone
python -X utf8 scripts/italy-law/build.py --repo ../italy-law
# 2. Check every version against the official data, and record the result
python -X utf8 scripts/italy-law/check_repo.py --repo ../italy-law --write
# 3. The smoke test of the commands in README.md, and the corpus smoke test
python -X utf8 scripts/italy-law/test_repo.py --repo ../italy-law --record
python -X utf8 scripts/test_corpus.py ../italy-law tools/vigente.py
# 4. Rebuild from the cache into a temporary folder and compare every hash
python -X utf8 scripts/italy-law/build.py --offline --verify-rebuild --repo ../italy-law
# 5. The final build (it writes the results above into this file), and the same comparison again
python -X utf8 scripts/italy-law/build.py --offline --repo ../italy-law
python -X utf8 scripts/italy-law/build.py --offline --verify-rebuild --repo ../italy-law
```

`--offline` reads only the cache. The build day defaults to the day the data was retrieved, so the documentation
commit has the same date on any later rebuild. The same scripts are in `tools/`.

## Software

- build.py blob `{blob}` (`git hash-object`), with reproduce.py, check_repo.py and test_repo.py in `tools/`
- {_v(['python', '--version'])}, lxml {lxmlv}
- {_v(['git', '--version'])}; commits are written with `git fast-import` (one stream, no working tree)
- {_v(['curl', '--version'])}

## How the history is made

1. Each version file is parsed (Akoma Ntoso 3.0): the preface, the preamble, each `article`, the conclusions and
   each annex (`doc`) become one unit each, rendered as one line per block (paragraph, list item, point, and each
   line inside a paragraph); structure inside quoted text is not split. Spacing is normalised to single spaces, soft
   hyphens and zero-width characters are removed; nothing else is changed. Chapter, title and section headings go to
   `struttura.md`. The same version's JSON gives each article's amending provisions and the day its wording applies
   from, and the act's update history ("storia": type, number, date and Gazzetta date of every act).
2. Consecutive versions are compared unit by unit. Each changed unit is credited (counts over all acts):
   - Normattiva's per-article record names one act of this version: {why.get('record', 0)}
   - the record names several, one of them new in this version's history: {why.get('record+history', 0)}
   - by date only, the one act new in this version's history: {why.get('history', 0)}
   - a unit without a record, the only act recorded in this version: {why.get('only act of this version', 0)}
   - editorial (only the (( )) marks, spacing or case changed): {why.get('editorial', 0)}
   - two or more acts possible, credited to none: {why.get('two or more acts possible', 0)}
   - no act in the record or the history, credited to none: {why.get('no act in the record or the update history', 0)}
3. One commit per amending act per day, across all the acts (an act of the record that also amends another on the
   day it takes effect is one commit with both), then the labelled commits by `Normattiva (IPZS)`. The first version
   of each act is a commit by the act itself. Commits: {kinds.get('start', 0)} first versions, {kinds.get('law', 0)}
   by an act, {kinds.get('candidates', 0)} with candidates, {kinds.get('unexplained', 0)} unexplained,
   {kinds.get('editorial', 0)} editorial; {n_clamped} are in force before 1970 and dated 1970-01-01 (real day in
   `In-force:`). {len(authors)} distinct authors. {len(tags)} tags. {'Versions in force after the build day were left out.' if future else 'No version starts after the build day.'}

Changes credited by date only:
{items('history')}

Units credited as the only act of the version:
{items('only act of this version')}

Changes two or more acts could have made (credited to none):
{items('two or more acts possible')}

Changes no act explains (credited to none):
{items('no act in the record or the update history')}

## Checks

1. `check_repo.py`: {check_line}
2. Rebuild: {rebuild_line}
3. `test_repo.py`: {f'{smoke["passed"]} of {smoke["total"]} passed' if smoke else 'not yet run'}
{smoke_lines}

## Decisions made by hand

- The acts: the Constitution and every constitutional law (cheap: one prepared collection), plus four statutes with a
  long multivigente history: L. 300/1970, L. 241/1990, D.Lgs. 196/2003, D.Lgs. 82/2005.
- The text is the Akoma Ntoso export; the JSON export is used only for the per-article records and the update history,
  and as a second check. Normattiva's `(( ))` marks and its notes ("AGGIORNAMENTO") are kept as printed, because they
  are part of the published consolidated text; a change of the marks alone is labelled editorial.
- A decree-law is the author of changes its conversion law made, as Normattiva records them under the decree-law.
- Judgments of the Constitutional Court and published corrections are authors, labelled as such. Normattiva gives a
  judgment's number but not its date, so its year (in the label and the ECLI link) is the year of the Gazzetta that
  published it; a judgment filed in late December and published in January would carry the later year.
- Annexes (codes of conduct and similar texts in D.Lgs. 196/2003) are never credited by date only: they take effect on
  days the update history does not record. Such changes are labelled, with the act new in that version named as an
  unconfirmed `Candidate:`.
- Two versions with the same start day: the later one (higher V number) is the text of that day.
- Summer time in Rome: the tz database's Italy rules for 1970-1979, then the EU rules (start <= day < end).
- The licence: CC BY 4.0, per the portal's "Dati disponibili" page (CC BY-NC applied only during the 2025
  experimental phase).

## What the AI did

This repository was built by Claude Code with Claude Opus 5.5 (`claude-opus-5-5`), which found the API in the
portal's own documentation and JavaScript bundle, wrote build.py, reproduce.py, check_repo.py, test_repo.py and
tools/vigente.py, and wrote the documentation. No AI wrote or changed any legal text, and no model runs at build time:
the text, the dates and the authors all come from Normattiva's data by the rules above.
"""
    (repo / 'REPRODUCE.md').write_text(text, encoding='utf-8', newline='\n')
