# Tools

The scripts behind this Italy-only run of global-law's vulnerability detectors. They run inside a copy of
[global-law/vulnerabilities/scripts](https://github.com/lexifina/global-law/tree/main/vulnerabilities/scripts) (Python 3.11+,
`pip install duckdb pyarrow`), with a bare clone of this repository at `sources/corpus/italy-law.git`, a blobless bare
clone of global-law at `sources/global-law.git`, and a `pins.json` that names only italy-law and its commit (language
`it`). `build_vulns.py`, `flags_chart.py`, `late_ext_select.py` and `late_ext_rebut.py` sit two folders above the scripts,
next to `config.json`.

| Script | What it does |
| --- | --- |
| `run.sh` | Indexes the history and texts, maps the paths from before the move of 17 November 2026 (`map_moved.py`), adds this repository's history rows, and runs the detectors (`bash run.sh <shards>`; it was run with 6). It sets `LE_SCAN_PATHS="normativa/ costituzione/"`, below |
| `map_moved.py` | Rewrites the paths in the history table to each act's folder since the move of the act-type folders to `normativa/<kind>/` (`data/paths.json`), so that an act's history is not split in two at the move (as patched by `patch_it2.py`, below) |
| `add_root.py` | Builds the history rows from this repository's own commits (global-law replays it only up to an earlier commit), so the history detectors read every change |
| `run_triage.sh` | The model review: the 40 strongest flags per category, the 40 strongest lapsed time limits in law texts, and the empty periods |
| `late_ext_select.py` | Chooses the empty periods for global-law's review of that category (here all 3) |
| `late_ext_rebut.py` | Adds the second, arguing-against pass to the empty-period review, as `triage.py` does for the other categories |
| `build_vulns.py` | Builds `data/flags.csv`, `data/reviewed.csv` and `data/by_category.csv` from the findings and the model review |
| `flags_chart.py` | Draws the chart at the top of the READMEs, in Italian and English, light and dark |
| `config.json` | The repository, the Italian category names, the folders that are not law, the chart's labels, and `dedup_second_copies` (below) |
| `patch_detectors.py` | Fixes blind spots found in runs on several country repositories in the copy of global-law's scripts (`python -X utf8 patch_detectors.py <scripts dir>`) |
| `patch_detectors_vi.py`, `patch_es.py`, `patch_ca.py`, `patch_en.py`, `patch_de.py`, `patch_en_et.py`, `patch_co.py`, `patch_sv.py`, `patch_pt.py`, `patch_ru.py`, `patch_r18.py`, `patch_xk.py`, `patch_mo.py`, `patch_lu.py`, `patch_li.py`, `patch_mx.py`, `patch_mn.py`, `patch_mt.py`, `patch_np.py`, `patch_en_nr.py`, `patch_dv.py`, `patch_az.py`, `patch_ar.py`, `patch_en_nz.py`, `patch_nb.py`, `patch_mk.py`, `patch_pa.py`, `patch_py.py`, `patch_pe.py`, `patch_en_ph.py`, `patch_qa.py`, `patch_nl.py`, `patch_pl.py`, `patch_ru_fz.py`, `patch_sl.py`, `patch_sk.py` | The same for the blind spots that runs on other countries and languages found, one file each; this run's copy carries them all. Most apply only to their own language; those for every language (references, currencies, notes) apply here too |
| `patch_it.py` | The first fixes for Italian, made for San Marino's coordinated texts: deadlines and extensions ("entro il 30 giugno 2021", "prorogato al"), repeal clauses that are not placeholders, "articolo 14, comma 1 della Legge ...", lire written "L. 10.000" or in words |
| `patch_it2.py` | This run's fixes, below (`python -X utf8 patch_it2.py <scripts dir>`; each change carries a `patch_it2` marker, and one already in place is skipped) |
| `apply_patches.py` | Applies every patch above once, in order, recording each in `.kit_patches.json` in the scripts folder (`python -X utf8 apply_patches.py <scripts dir>`); `patch_it2.py` is last in its list |
| `redo.py` | Runs `apply_patches.py`, then again only the scans and detectors the fixes change, the model review of lapsed time limits, references to deleted provisions and empty periods, and the build (`python -X utf8 redo.py <run folder> [--keep-reviews] [--full]`; `EMBED_FONTS` names the script that embeds the chart's fonts). Not used here: the fixes were applied before the run, except those to references and currencies, after which the scans and detectors they change were run again by hand |
| `notes_split.py` | Hand-check helper: for each flag, whether it stands in an article's text or in Normattiva's update notes ("AGGIORNAMENTO", after the line of dashes) (the counts in the READMEs) |

The model review needs `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL` and `LLM_AUTH` set for an OpenAI-compatible Responses API.
It was run as `bash run_triage.sh '^(parlamento|giurisprudenza|autorita|eu-nim|data|tools|visualisations|vulnerabilities)/'`;
every file scanned is law, so the review of lapsed time limits in law texts drew the same 40 flags as the review of all of
them, and `build_vulns.py` keeps the later review of each flag.

## What was scanned

This repository holds 4,052,201 commits and 4,481,963 files at the commit read. The scans of the files at that commit read
only `normativa/` (527,728 files, the acts) and `costituzione/` (161), through `LE_SCAN_PATHS`. They do not read
`parlamento/` (2,777,870 files: bills, sittings, votes and parliamentary documents), `giurisprudenza/` (1,169,780 court
decisions), `autorita/` (938 competition-authority decisions) or `eu-nim/` (5,465 records of EU transposition measures):
none of them is law, together they are 12.4 GB of text, and the detectors that read every file at once would not fit in
memory on the machine that ran them. The history table is read whole: its 75,583 commits without a `Kind:` trailer are
the law (one "testo vigente" commit for nearly every act, and the versions of the acts held with every version);
`add_root.py` needed no change, as none of this repository's other kinds (`parliamentary-record`, `case-law`,
`parliamentary-document`, `bill`, `legislative-process`, `correction`, `law-record`, `transposition-record`,
`authority-decision`, `documentation`) is in its list of law.

## Changes made for this repository (`patch_it2.py` and the build)

Scale (every language; nothing changes for a small repository):

- `ingest/extract.py`: `git log --raw` is read in pieces and written in row groups (7,818,199 file changes here), not held
  in memory as one string and seven lists. The commit read is the folder move itself (a `Paths: data/paths.json` trailer,
  every moved folder's tree identical before and after): its 3,305,597 renames are written from `git ls-tree` as the
  `R100` rows `git log -M` gives, and the log starts at its parent, because git's rename search over that commit alone
  needed some 8 GB.
- `ingest/trailers.py`: the same streaming for the 4,052,201 commit messages.
- `map_moved.py`: the kit's version mapped a file only when its parent folder had moved; here the act-type folders
  moved (`legge/` to `normativa/legge/`), so it now maps a moved folder's files at any depth and a moved root file
  (`atti.csv`), in batches: 9,932,927 paths rewritten.
- `LE_SCAN_PATHS` (above): read by `is_law_file` (text, reference and heading scans, empty periods), by the `ls-tree` of
  `detectors/placeholder_ref.py`, `dup_labels.py` and `dead_fine.py`, and by the `git grep` of `currency_scan.py` and
  `notes_scan.py`. Unset, every file is read, as before. `ingest/headings.py` reads only law files and writes in row
  groups.
- `build_vulns.py` finds the commit that deleted a file in the history table, one query per such file, instead of one
  `git log --diff-filter=D` over the whole history, and reads only the commits of the retroactive-date flags from the
  history table, not all its rows.

Italian (Normattiva's text, language `it`):

- `ingest/refscan.py`: a reference is not to one of this act's own articles when it stands inside quoted text (an
  amendment's new wording, a note quoting another act), follows "con l'art." (a note naming the amending act's article),
  follows "citato", "predetto", "suddetto", "medesimo", "stesso" and the like, is "(Art. 173.)" in `struttura.md` (the
  article a chapter starts at), or is followed in its clause by another act ("articoli 4 e 5 della legge n. 241 del
  1990", "articolo 12 del d.P.R. 22 dicembre 1986, n. 917", "art. 2043 c.c.") before any "presente legge". The folders a
  code is split into (`codice-civile/art-0000-0499/`) count as one act. References to repealed placeholders went from
  6,812 to 2,101 (2,238 of them were the table of contents in `struttura.md`), dead fines from 132 to 79; references to
  deleted provisions stayed at 0.
- `detectors/placeholder_ref.py`: "Art. 7-bis." is a heading, as "Art. 7." is, so the article under it that reads only
  "((ARTICOLO ABROGATO DAL D.P.R. ...))" is a placeholder.
- `ingest/textscan.py`: "a tutto il 31 dicembre 2020", "fino a tutto il" and "sino a tutto il" are time limits, and
  "entro il termine del" a deadline.
- `detectors/currency_scan.py`: in Italian, "DM" (decreto ministeriale), "franco", "lati" and "inti" are not currencies, and
  dinars (Tunisian, Algerian, Jordanian) are not dead: dead currencies went from 39,033 to 38,899.
- `config.json` sets `dedup_second_copies`: 901 act folders are a second copy of another (`normativa/<kind>/<year>/<n>-<codice
  redazionale>/` beside `<n>/`), 896 with the same title, number and date, the Codice penale and the Codice di procedura
  civile among them. `build_vulns.py` counts a flag in such a copy once, in the first copy, when the first copy has the
  same flag (same detector, file, date and reference); a reviewed flag stays where it is. 1,007 flags were counted once
  (581 lapsed time limits, 77 references to repealed placeholders, 349 dead currencies).

Not fixed: the update notes at the end of each article ("AGGIORNAMENTO") are read as text by every detector; months or
years without a day ("entro il mese di dicembre 2020") and relative terms ("entro trenta giorni") are not time limits;
"(SIC)" (siti di interesse comunitario, sistema integrato delle comunicazioni) is read as the editor's "[sic]"; an article
with a suffix past "decies" ("2409-septiesdecies") is read as the article without it; the references still include lists
of other acts' articles and amendments without quotation marks (see the README).
