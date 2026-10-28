# How this repository was made

Everything needed to rebuild this repository exactly, from the same data: the sources, the commands in order, the
software, the decisions made by hand, and what an AI model did and did not do. Built 2026-10-28 from data retrieved
2026-10-28.

## Sources

Normattiva Open Data, <https://dati.normattiva.it>, run by the Istituto Poligrafico e Zecca dello Stato for the
Presidenza del Consiglio dei Ministri, under CC BY 4.0 (see LICENSE). Its API is documented by the portal itself
(`/assets/come_fare_per/API_Normattiva_OpenData.pdf` and `openapi-bff-opendata.json`); base address
`https://api.normattiva.it/t/normattiva.api/bff-opendata/v1/api/v1`. Robots: `www.normattiva.it/robots.txt` disallows
only `/ricerca/` and `/mfr/ricerca/`, and names no AI crawler; the build does not touch www.normattiva.it at all.

- Single acts: the documented asynchronous export. `POST ricerca-asincrona/nuova-ricerca` with
  `{"formato": "AKN" or "JSON", "tipoRicerca": "A", "richiestaExport": "M", "parametriRicerca": {...}}` returns a token
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
| `costituzione-json.zip` | 2026-10-28 | 848733 | `7e34b1741092f7e3e0a28d5d7664e4a00c95be85962d7889aab08060fe4027a1` |
| `costituzione.zip` | 2026-10-28 | 873754 | `a5d97f6abfe81215d0c22a7c8b4b700ec68cafe707eff525c16ed94decefcdb6` |
| `dlgs-196-2003-json.zip` | 2026-10-28 | 10881067 | `f0b31b96ba154ee9e99dde865dc925583a15563ced2ff80643ebe81bf8786648` |
| `dlgs-196-2003.zip` | 2026-10-28 | 13830132 | `ca1dca4a1bf03e90cc2bf5a8dac098bcd5c6f2434abd21f4cef482e7658fde94` |
| `dlgs-82-2005-json.zip` | 2026-10-28 | 4409884 | `41694cef428b4d6b9c8392dadbb1cd1507c5dca05a5b0d6487c93ac35512da1f` |
| `dlgs-82-2005.zip` | 2026-10-28 | 5272965 | `e9379f1220a3ed2dd2237adfcbf42c12c6089ce26670404152518aaa6ae716b0` |
| `legge-241-1990-json.zip` | 2026-10-28 | 1662772 | `1b050463b1c1788630414c85699459a7afac4c051c49c816fc78b7f19851d96d` |
| `legge-241-1990.zip` | 2026-10-28 | 2035379 | `9251a39598ef559cb7328b444fa17126f307bb1214e47d093761f1cdcc58ddec` |
| `legge-300-1970-json.zip` | 2026-10-28 | 600643 | `9504e40a77c37d81c0de5795277646d2d9ca35803029f09bd0bc8714ea09b309` |
| `legge-300-1970.zip` | 2026-10-28 | 622319 | `3b4f93c9b7e70e0935e90b5929ce7949b7cd441a1ac69029e0e60393eec44949` |
| `leggi-costituzionali-json.zip` | 2026-10-28 | 847225 | `0f85c022368e731d8d8d3f236dc78b5a108841651c6088134598164714df3896` |
| `leggi-costituzionali.zip` | 2026-10-28 | 910258 | `27d9afe863d4012721ff48d3d72a3d789eb625b9632db3c9ae972accce37ba1f` |

Each zip has one folder per act and one file per version: `<GU date>_<codice redazionale>_ORIGINALE_V0.xml` and
`..._VIGENZA_<day the version applies from>_V<n>.xml`. `data/versioni.json` lists every version used, with its
file name, sha256 and ELI address.

## The acts

| Act | Folder | Versions | First in force | Provisions now |
| --- | --- | ---: | --- | ---: |
| Costituzione | `costituzione/` | 28 | 1948-01-01 | 160 |
| D.Lgs. 196/2003 | `decreto-legislativo/2003/196/` | 59 | 2004-01-01 | 331 |
| D.Lgs. 82/2005 | `decreto-legislativo/2005/82/` | 62 | 2006-01-01 | 127 |
| Legge costituzionale 1/1947 | `legge-costituzionale/1947/1/` | 1 | 1947-02-22 | 4 |
| Legge costituzionale 2/1947 | `legge-costituzionale/1947/2/` | 1 | 1947-06-19 | 5 |
| Legge costituzionale 3/1947 | `legge-costituzionale/1947/3/` | 1 | 1947-11-07 | 6 |
| Legge costituzionale 1/1948 | `legge-costituzionale/1948/1/` | 2 | 1948-02-21 | 7 |
| Legge costituzionale 2/1948 | `legge-costituzionale/1948/2/` | 1 | 1948-03-10 | 5 |
| Legge costituzionale 3/1948 | `legge-costituzionale/1948/3/` | 16 | 1948-03-10 | 62 |
| Legge costituzionale 4/1948 | `legge-costituzionale/1948/4/` | 6 | 1948-03-11 | 58 |
| Legge costituzionale 5/1948 | `legge-costituzionale/1948/5/` | 4 | 1948-03-14 | 118 |
| Legge costituzionale 1/1953 | `legge-costituzionale/1953/1/` | 4 | 1953-03-29 | 17 |
| Legge costituzionale 1/1958 | `legge-costituzionale/1958/1/` | 1 | 1958-04-16 | 3 |
| Legge costituzionale 1/1961 | `legge-costituzionale/1961/1/` | 1 | 1961-04-16 | 5 |
| Legge costituzionale 1/1963 | `legge-costituzionale/1963/1/` | 19 | 1963-02-16 | 73 |
| Legge costituzionale 2/1963 | `legge-costituzionale/1963/2/` | 1 | 1963-02-27 | 8 |
| Legge costituzionale 3/1963 | `legge-costituzionale/1963/3/` | 1 | 1964-01-19 | 4 |
| Legge costituzionale 1/1967 | `legge-costituzionale/1967/1/` | 1 | 1967-07-18 | 3 |
| Legge costituzionale 2/1967 | `legge-costituzionale/1967/2/` | 1 | 1967-12-10 | 9 |
| Legge costituzionale 1/1971 | `legge-costituzionale/1971/1/` | 1 | 1972-01-20 | 69 |
| Legge costituzionale 1/1972 | `legge-costituzionale/1972/1/` | 1 | 1972-03-22 | 10 |
| Legge costituzionale 1/1986 | `legge-costituzionale/1986/1/` | 1 | 1986-05-27 | 3 |
| Legge costituzionale 1/1989 | `legge-costituzionale/1989/1/` | 1 | 1989-01-18 | 16 |
| Legge costituzionale 2/1989 | `legge-costituzionale/1989/2/` | 1 | 1989-04-07 | 5 |
| Legge costituzionale 3/1989 | `legge-costituzionale/1989/3/` | 1 | 1989-04-14 | 9 |
| Legge costituzionale 1/1991 | `legge-costituzionale/1991/1/` | 1 | 1991-11-23 | 3 |
| Legge costituzionale 1/1992 | `legge-costituzionale/1992/1/` | 1 | 1992-03-24 | 3 |
| Legge costituzionale 1/1993 | `legge-costituzionale/1993/1/` | 1 | 1993-08-11 | 9 |
| Legge costituzionale 2/1993 | `legge-costituzionale/1993/2/` | 1 | 1993-10-10 | 8 |
| Legge costituzionale 3/1993 | `legge-costituzionale/1993/3/` | 1 | 1993-11-14 | 3 |
| Legge costituzionale 1/1997 | `legge-costituzionale/1997/1/` | 1 | 1997-01-29 | 10 |
| Legge costituzionale 1/1999 | `legge-costituzionale/1999/1/` | 1 | 2000-01-06 | 7 |
| Legge costituzionale 2/1999 | `legge-costituzionale/1999/2/` | 1 | 2000-01-07 | 4 |
| Legge costituzionale 1/2000 | `legge-costituzionale/2000/1/` | 1 | 2000-02-04 | 3 |
| Legge costituzionale 1/2001 | `legge-costituzionale/2001/1/` | 1 | 2001-02-08 | 5 |
| Legge costituzionale 2/2001 | `legge-costituzionale/2001/2/` | 1 | 2001-02-16 | 9 |
| Legge costituzionale 3/2001 | `legge-costituzionale/2001/3/` | 1 | 2001-11-08 | 13 |
| Legge costituzionale 1/2002 | `legge-costituzionale/2002/1/` | 1 | 2002-11-10 | 3 |
| Legge costituzionale 1/2003 | `legge-costituzionale/2003/1/` | 1 | 2003-06-27 | 3 |
| Legge costituzionale 1/2007 | `legge-costituzionale/2007/1/` | 1 | 2007-10-25 | 3 |
| Legge costituzionale 1/2012 | `legge-costituzionale/2012/1/` | 1 | 2012-05-08 | 8 |
| Legge costituzionale 1/2013 | `legge-costituzionale/2013/1/` | 1 | 2013-03-03 | 4 |
| Legge costituzionale 2/2013 | `legge-costituzionale/2013/2/` | 1 | 2013-03-05 | 4 |
| Legge costituzionale 3/2013 | `legge-costituzionale/2013/3/` | 1 | 2013-03-15 | 3 |
| Legge costituzionale 1/2016 | `legge-costituzionale/2016/1/` | 1 | 2016-08-23 | 14 |
| Legge costituzionale 1/2017 | `legge-costituzionale/2017/1/` | 1 | 2017-12-15 | 13 |
| Legge costituzionale 1/2020 | `legge-costituzionale/2020/1/` | 1 | 2020-11-05 | 6 |
| Legge costituzionale 1/2021 | `legge-costituzionale/2021/1/` | 1 | 2021-11-04 | 3 |
| Legge costituzionale 1/2022 | `legge-costituzionale/2022/1/` | 1 | 2022-03-09 | 5 |
| Legge costituzionale 2/2022 | `legge-costituzionale/2022/2/` | 1 | 2022-11-30 | 3 |
| Legge costituzionale 1/2023 | `legge-costituzionale/2023/1/` | 1 | 2023-10-22 | 3 |
| Legge costituzionale 1/2026 | `legge-costituzionale/2026/1/` | 1 | 2026-02-24 | 12 |
| Legge costituzionale 2/2026 | `legge-costituzionale/2026/2/` | 1 | 2026-06-23 | 3 |
| Legge 300/1970 | `legge/1970/300/` | 35 | 1970-06-11 | 45 |
| Legge 241/1990 | `legge/1990/241/` | 61 | 1990-09-02 | 55 |

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

- build.py blob `7387e435691f12e2f85036ce509f1f31b88483da` (`git hash-object`), with reproduce.py, check_repo.py and test_repo.py in `tools/`
- Python 3.12.10, lxml 6.1.3
- git version 2.46.0.windows.1; commits are written with `git fast-import` (one stream, no working tree)
- curl 8.21.0 (Windows) libcurl/8.21.0 Schannel zlib/1.3.2 WinIDN WinLDAP

## How the history is made

1. Each version file is parsed (Akoma Ntoso 3.0): the preface, the preamble, each `article`, the conclusions and
   each annex (`doc`) become one unit each, rendered as one line per block (paragraph, list item, point, and each
   line inside a paragraph); structure inside quoted text is not split. Spacing is normalised to single spaces, soft
   hyphens and zero-width characters are removed; nothing else is changed. Chapter, title and section headings go to
   `struttura.md`. The same version's JSON gives each article's amending provisions and the day its wording applies
   from, and the act's update history ("storia": type, number, date and Gazzetta date of every act).
2. Consecutive versions are compared unit by unit. Each changed unit is credited (counts over all acts):
   - Normattiva's per-article record names one act of this version: 1294
   - the record names several, one of them new in this version's history: 59
   - by date only, the one act new in this version's history: 10
   - a unit without a record, the only act recorded in this version: 5
   - editorial (only the (( )) marks, spacing or case changed): 4
   - two or more acts possible, credited to none: 40
   - no act in the record or the history, credited to none: 78
3. One commit per amending act per day, across all the acts (an act of the record that also amends another on the
   day it takes effect is one commit with both), then the labelled commits by `Normattiva (IPZS)`. The first version
   of each act is a commit by the act itself. Commits: 21 first versions, 207
   by an act, 4 with candidates, 6 unexplained,
   4 editorial; 23 are in force before 1970 and dated 1970-01-01 (real day in
   `In-force:`). 224 distinct authors. 533 tags. No version starts after the build day.

Changes credited by date only:
  - D.Lgs. 82/2005 2006-05-14: Struttura
  - Legge costituzionale 5/1948 1972-01-20: Art. 17
  - Legge costituzionale 5/1948 1972-01-20: Art. 46
  - Legge costituzionale 5/1948 1972-01-20: Art. 63
  - Legge costituzionale 5/1948 1972-01-20: Struttura
  - Legge costituzionale 1/1963 2022-01-01: Art. 12
  - Legge costituzionale 1/1963 2022-01-01: Art. 20
  - Legge costituzionale 1/1963 2022-01-01: Art. 34
  - Legge costituzionale 1/1963 2022-01-01: Art. 59
  - Legge 241/1990 2005-03-08: Struttura

Units credited as the only act of the version:
  - D.Lgs. 196/2003 2018-09-19: Intestazione
  - D.Lgs. 196/2003 2018-09-19: Preambolo
  - D.Lgs. 196/2003 2018-09-19: Struttura
  - D.Lgs. 82/2005 2016-09-14: Struttura
  - D.Lgs. 82/2005 2018-01-27: Struttura

Changes two or more acts could have made (credited to none):
  - D.Lgs. 196/2003 2019-04-09: Allegato A.3 Codice deontologia scopi statistici e ricerca scientifica Sistema Statistico Nazionale-art. 1 (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 196/2003 2019-04-09: Allegato A.3 Codice deontologia scopi statistici e ricerca scientifica Sistema Statistico Nazionale-art. 2 (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 196/2003 2019-04-09: Allegato A.3 Codice deontologia scopi statistici e ricerca scientifica Sistema Statistico Nazionale-art. 3 (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 196/2003 2019-04-09: Allegato A.3 Codice deontologia scopi statistici e ricerca scientifica Sistema Statistico Nazionale-art. 4 (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 196/2003 2019-04-09: Allegato A.3 Codice deontologia scopi statistici e ricerca scientifica Sistema Statistico Nazionale-art. 4 bis (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 196/2003 2019-04-09: Allegato A.3 Codice deontologia scopi statistici e ricerca scientifica Sistema Statistico Nazionale-art. 5 (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 196/2003 2019-04-09: Allegato A.3 Codice deontologia scopi statistici e ricerca scientifica Sistema Statistico Nazionale-art. 6 (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 196/2003 2019-04-09: Allegato A.3 Codice deontologia scopi statistici e ricerca scientifica Sistema Statistico Nazionale-art. 7 (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 196/2003 2019-04-09: Allegato A.3 Codice deontologia scopi statistici e ricerca scientifica Sistema Statistico Nazionale-art. 8 (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 196/2003 2019-04-09: Allegato A.3 Codice deontologia scopi statistici e ricerca scientifica Sistema Statistico Nazionale-art. 9 (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 196/2003 2019-04-09: Allegato A.3 Codice deontologia scopi statistici e ricerca scientifica Sistema Statistico Nazionale-art. 10 (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 196/2003 2019-04-09: Allegato A.3 Codice deontologia scopi statistici e ricerca scientifica Sistema Statistico Nazionale-art. 11 (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 196/2003 2019-04-09: Allegato A.3 Codice deontologia scopi statistici e ricerca scientifica Sistema Statistico Nazionale-art. 12 (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 196/2003 2019-04-09: Allegato A.3 Codice deontologia scopi statistici e ricerca scientifica Sistema Statistico Nazionale-art. 13 (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 196/2003 2019-04-09: Allegato A.3 Codice deontologia scopi statistici e ricerca scientifica Sistema Statistico Nazionale-art. 14 (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 196/2003 2019-04-09: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 1 (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 196/2003 2019-04-09: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 2 (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 196/2003 2019-04-09: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 3 (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 196/2003 2019-04-09: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 4 (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 196/2003 2019-04-09: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 5 (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 196/2003 2019-04-09: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 6 (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 196/2003 2019-04-09: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 7 (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 196/2003 2019-04-09: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 8 (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 196/2003 2019-04-09: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 9 (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 196/2003 2019-04-09: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 10 (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 196/2003 2019-04-09: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 11 (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 196/2003 2019-04-09: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 12 (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 196/2003 2019-04-09: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 13 (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 196/2003 2019-04-09: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 14 (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 196/2003 2019-04-09: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 15 (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 196/2003 2019-04-09: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 16 (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 196/2003 2019-04-09: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 17 (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 196/2003 2019-04-09: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 18 (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 196/2003 2019-04-09: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 19 (Decreto 15 marzo 2019 (G.U. 25 marzo 2019), Decreto 15 marzo 2019 (G.U. 26 marzo 2019))
  - D.Lgs. 82/2005 2011-01-25: Art. 72 (D.L. 225/2010, D.Lgs. 235/2010)
  - D.Lgs. 82/2005 2011-01-25: Art. 74 (D.L. 225/2010, D.Lgs. 235/2010)
  - D.Lgs. 82/2005 2011-01-25: Art. 76 (D.L. 225/2010, D.Lgs. 235/2010)
  - D.Lgs. 82/2005 2011-01-25: Struttura (D.L. 225/2010, D.Lgs. 235/2010)
  - D.Lgs. 82/2005 2022-01-01: Art. 62 (Legge 233/2021, Legge 234/2021)
  - Legge costituzionale 1/1963 2019-06-30: Art. 51 (D.L. 34/2019, Legge 58/2019)

Changes no act explains (credited to none):
  - D.Lgs. 196/2003 2004-10-01: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 1
  - D.Lgs. 196/2003 2004-10-01: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 2
  - D.Lgs. 196/2003 2004-10-01: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 3
  - D.Lgs. 196/2003 2004-10-01: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 4
  - D.Lgs. 196/2003 2004-10-01: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 5
  - D.Lgs. 196/2003 2004-10-01: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 6
  - D.Lgs. 196/2003 2004-10-01: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 7
  - D.Lgs. 196/2003 2004-10-01: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 8
  - D.Lgs. 196/2003 2004-10-01: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 9
  - D.Lgs. 196/2003 2004-10-01: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 10
  - D.Lgs. 196/2003 2004-10-01: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 11
  - D.Lgs. 196/2003 2004-10-01: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 12
  - D.Lgs. 196/2003 2004-10-01: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 13
  - D.Lgs. 196/2003 2004-10-01: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 14
  - D.Lgs. 196/2003 2004-10-01: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 15
  - D.Lgs. 196/2003 2004-10-01: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 16
  - D.Lgs. 196/2003 2004-10-01: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 17
  - D.Lgs. 196/2003 2004-10-01: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 18
  - D.Lgs. 196/2003 2004-10-01: Allegato A.4 Codice di deontologia per scopi statistici e scientifici-art. 19
  - D.Lgs. 196/2003 2005-01-01: Allegato A.5 Codice di deontologia per i sistemi informativi-art. 1
  - D.Lgs. 196/2003 2005-01-01: Allegato A.5 Codice di deontologia per i sistemi informativi-art. 2
  - D.Lgs. 196/2003 2005-01-01: Allegato A.5 Codice di deontologia per i sistemi informativi-art. 3
  - D.Lgs. 196/2003 2005-01-01: Allegato A.5 Codice di deontologia per i sistemi informativi-art. 4
  - D.Lgs. 196/2003 2005-01-01: Allegato A.5 Codice di deontologia per i sistemi informativi-art. 5
  - D.Lgs. 196/2003 2005-01-01: Allegato A.5 Codice di deontologia per i sistemi informativi-art. 6
  - D.Lgs. 196/2003 2005-01-01: Allegato A.5 Codice di deontologia per i sistemi informativi-art. 7
  - D.Lgs. 196/2003 2005-01-01: Allegato A.5 Codice di deontologia per i sistemi informativi-art. 8
  - D.Lgs. 196/2003 2005-01-01: Allegato A.5 Codice di deontologia per i sistemi informativi-art. 9
  - D.Lgs. 196/2003 2005-01-01: Allegato A.5 Codice di deontologia per i sistemi informativi-art. 10
  - D.Lgs. 196/2003 2005-01-01: Allegato A.5 Codice di deontologia per i sistemi informativi-art. 11
  - D.Lgs. 196/2003 2005-01-01: Allegato A.5 Codice di deontologia per i sistemi informativi-art. 12
  - D.Lgs. 196/2003 2005-01-01: Allegato A.5 Codice di deontologia per i sistemi informativi-art. 13
  - D.Lgs. 196/2003 2005-01-01: Allegato A.5 Codice di deontologia per i sistemi informativi-art. 14
  - D.Lgs. 196/2003 2005-01-01: Allegato A.5 Codice di deontologia per i sistemi informativi-Allegato
  - D.Lgs. 196/2003 2019-02-26: Allegato A.1 Codice di deontologia attività giornalistica-art. 1
  - D.Lgs. 196/2003 2019-02-26: Allegato A.1 Codice di deontologia attività giornalistica-art. 2
  - D.Lgs. 196/2003 2019-02-26: Allegato A.1 Codice di deontologia attività giornalistica-art. 3
  - D.Lgs. 196/2003 2019-02-26: Allegato A.1 Codice di deontologia attività giornalistica-art. 4
  - D.Lgs. 196/2003 2019-02-26: Allegato A.1 Codice di deontologia attività giornalistica-art. 5
  - D.Lgs. 196/2003 2019-02-26: Allegato A.1 Codice di deontologia attività giornalistica-art. 6
  - D.Lgs. 196/2003 2019-02-26: Allegato A.1 Codice di deontologia attività giornalistica-art. 7
  - D.Lgs. 196/2003 2019-02-26: Allegato A.1 Codice di deontologia attività giornalistica-art. 8
  - D.Lgs. 196/2003 2019-02-26: Allegato A.1 Codice di deontologia attività giornalistica-art. 9
  - D.Lgs. 196/2003 2019-02-26: Allegato A.1 Codice di deontologia attività giornalistica-art. 10
  - D.Lgs. 196/2003 2019-02-26: Allegato A.1 Codice di deontologia attività giornalistica-art. 11
  - D.Lgs. 196/2003 2019-02-26: Allegato A.1 Codice di deontologia attività giornalistica-art. 12
  - D.Lgs. 196/2003 2019-02-26: Allegato A.1 Codice di deontologia attività giornalistica-art. 13
  - D.Lgs. 196/2003 2019-04-10: Allegato A.2 Codice di deontologia per scopi storici-art. 1
  - D.Lgs. 196/2003 2019-04-10: Allegato A.2 Codice di deontologia per scopi storici-art. 2
  - D.Lgs. 196/2003 2019-04-10: Allegato A.2 Codice di deontologia per scopi storici-art. 3
  - D.Lgs. 196/2003 2019-04-10: Allegato A.2 Codice di deontologia per scopi storici-art. 4
  - D.Lgs. 196/2003 2019-04-10: Allegato A.2 Codice di deontologia per scopi storici-art. 5
  - D.Lgs. 196/2003 2019-04-10: Allegato A.2 Codice di deontologia per scopi storici-art. 6
  - D.Lgs. 196/2003 2019-04-10: Allegato A.2 Codice di deontologia per scopi storici-art. 7
  - D.Lgs. 196/2003 2019-04-10: Allegato A.2 Codice di deontologia per scopi storici-art. 8
  - D.Lgs. 196/2003 2019-04-10: Allegato A.2 Codice di deontologia per scopi storici-art. 9
  - D.Lgs. 196/2003 2019-04-10: Allegato A.2 Codice di deontologia per scopi storici-art. 10
  - D.Lgs. 196/2003 2019-04-10: Allegato A.2 Codice di deontologia per scopi storici-art. 11
  - D.Lgs. 196/2003 2019-04-10: Allegato A.2 Codice di deontologia per scopi storici-art. 12
  - D.Lgs. 196/2003 2019-04-10: Allegato A.2 Codice di deontologia per scopi storici-art. 13
  - D.Lgs. 196/2003 2019-04-10: Allegato A.2 Codice di deontologia per scopi storici-art. 14
  - D.Lgs. 196/2003 2019-04-10: Allegato A.6 Codice di deontologia per le investigazioni o la tutela in sede giudiziaria-art. 1
  - D.Lgs. 196/2003 2019-04-10: Allegato A.6 Codice di deontologia per le investigazioni o la tutela in sede giudiziaria-art. 2
  - D.Lgs. 196/2003 2019-04-10: Allegato A.6 Codice di deontologia per le investigazioni o la tutela in sede giudiziaria-art. 3
  - D.Lgs. 196/2003 2019-04-10: Allegato A.6 Codice di deontologia per le investigazioni o la tutela in sede giudiziaria-art. 4
  - D.Lgs. 196/2003 2019-04-10: Allegato A.6 Codice di deontologia per le investigazioni o la tutela in sede giudiziaria-art. 5
  - D.Lgs. 196/2003 2019-04-10: Allegato A.6 Codice di deontologia per le investigazioni o la tutela in sede giudiziaria-art. 6
  - D.Lgs. 196/2003 2019-04-10: Allegato A.6 Codice di deontologia per le investigazioni o la tutela in sede giudiziaria-art. 7
  - D.Lgs. 196/2003 2019-04-10: Allegato A.6 Codice di deontologia per le investigazioni o la tutela in sede giudiziaria-art. 8
  - D.Lgs. 196/2003 2019-04-10: Allegato A.6 Codice di deontologia per le investigazioni o la tutela in sede giudiziaria-art. 9
  - D.Lgs. 196/2003 2019-04-10: Allegato A.6 Codice di deontologia per le investigazioni o la tutela in sede giudiziaria-art. 10
  - D.Lgs. 196/2003 2019-04-10: Allegato A.6 Codice di deontologia per le investigazioni o la tutela in sede giudiziaria-art. 11
  - D.Lgs. 196/2003 2019-04-10: Allegato A.6 Codice di deontologia per le investigazioni o la tutela in sede giudiziaria-art. 12
  - D.Lgs. 196/2003 2019-04-10: Allegato A.6 Codice di deontologia per le investigazioni o la tutela in sede giudiziaria-art. 13
  - D.Lgs. 196/2003 2019-04-10: Allegato A.6 Codice di deontologia per le investigazioni o la tutela in sede giudiziaria-Allegato
  - D.Lgs. 82/2005 2015-05-21: Art. 58
  - D.Lgs. 82/2005 2015-05-21: Art. 71
  - Legge costituzionale 3/1948 1983-01-01: Art. 12

## Checks

1. `check_repo.py`: 340 versions checked (36506 files): **0 mismatches** byte for byte; 340 versions word for word (8008550 words) against every word of the official XML: **0 mismatches**. Against Normattiva's JSON export of the same versions (a second manifestation, with its own headings and numbering), the words agree as a multiset in 155 of 340 versions; the differences are in how the JSON repeats headings, prints the preamble inside article 1, escapes `<` and `>`, and spells a few identifiers (`nonies`/`novies`). It is information, not a pass/fail test.
2. Rebuild: A second build from the same cache into an empty folder gave the same history: the last law commit was `76bb450e2dec3403aadc1de75f2d29e0aebfa691` in both, and every one of the 242 law commits and 533 tags had the same hash.
3. `test_repo.py`: 6 of 6 passed
   - pass: blame names the amending acts: costituzione/art-117.md lines by Costituzione della Repubblica Italiana, Legge costituzionale 1/2012, Legge costituzionale 3/2001
   - pass: text before and after an amendment: costituzione/art-009.md 2022-03-08 != 2022-03-09; costituzione/art-117.md 2001-11-07 != 2001-11-08; decreto-legislativo/2003/196/art-013.md 2018-09-18 != 2018-09-19
   - pass: log --follow in date order: costituzione/art-117.md 3 commits; legge/1990/241/art-021-quater.md 2 commits; decreto-legislativo/2003/196/art-132.md 15 commits
   - pass: tags resolve, In-force on every law commit: 533 tags resolve; 242 law commits carry In-force, in order
   - pass: only the documentation commit is by Lexifina: only the documentation commit 00e9e3f338 is by Lexifina; 224 distinct authors
   - pass: README commands run: 11 README commands ran and printed output

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
