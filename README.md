# Italian law, change by change

The Constitution of the Italian Republic, every constitutional law (leggi costituzionali), and four much-amended
statutes as a git repository: the Statuto dei lavoratori (Legge 300/1970), the law on administrative procedure (Legge
241/1990), the personal data protection code (D.Lgs. 196/2003) and the digital administration code (D.Lgs. 82/2005).
Each amending act is one commit, credited to that act and dated the day it took effect, at noon in Rome. The text is
Normattiva's consolidated text "in multivigenza" (every version over time), from Normattiva Open Data.

*In italiano: [sotto](#in-italiano).*

## The questions, as git commands

| Question | Command |
| --- | --- |
| What did art. 117 of the Constitution say on 1 January 2000? | `python tools/vigente.py 2000-01-01 costituzione 117` |
| The whole Constitution as it stood on 1 January 2023 | `python tools/vigente.py 2023-01-01 costituzione` |
| Art. 13 of the privacy code on 1 June 2015 | `python tools/vigente.py 2015-06-01 decreto-legislativo/2003/196 13` |
| Which act wrote each line of art. 117? | `git blame costituzione/art-117.md` |
| Every change to art. 9 of the Constitution, with the act and the day | `git log --follow costituzione/art-009.md` |
| Everything one act changed | `git show --stat atto/legge-costituzionale-2001-3` |
| The Constitution on the day a revision took effect | `git show --stat costituzione/2022-03-09` |
| Every act that changed Legge 241/1990 in 2005 | `git log --format="%ad %an" --date=short --since=2005-01-01 --until=2005-12-31 -- legge/1990/241` |
| Judgments of the Constitutional Court that changed the text | `git log --format="%ad %an | %s" --date=short --author=sentenza` |
| Changes no act explains, or that two acts could have made | `git log --format="%ad %s" --date=short --author=Normattiva` |
| Changes credited by date only | `git log --format="%h %an | %s" --grep="Evidence: .*by date only"` |
| The amending acts with all their dates | [`atti.csv`](atti.csv) |

## The dates, and which one we use

An Italian act has the day it was enacted (`Enacted:`), the day it was published in the Gazzetta Ufficiale
(`Published:`), and the day the change took effect (`In-force:`). **Commits are dated the day the change took effect**,
at noon in Rome: that is the day Normattiva gives as the start of the version ("vigenza dal"). All the dates are in
every commit message. Git cannot record a date before 1970: commits in force before then (the Constitution from 1948,
its revisions up to 1967, the early regional statutes) are dated 1 January 1970, one second apart in the order they
took effect, and the real day is in `In-force:`. Tools should read `In-force:`, as `tools/vigente.py` does.

Bare dates given to git's `--since`, `--until` and `--before` are read in your local time zone; commits are at noon in
Rome, so a day's change falls inside that day everywhere, but for an exact cut use a full time,
`--before="2022-03-09T23:59:59+01:00"`. In PowerShell, `$(...)` inside `git show $(...):path` splits into two
arguments; use `$r = git rev-list -1 ...; git show "$($r):path"`.

A tag names each act's state on each day it changed (`costituzione/2022-03-09`, `legge/1990/241/2005-03-08`) and each
amending act's first commit (`atto/legge-costituzionale-2022-1`, `atto/sentenza-2025-156`). After a rebuild of this
repository, fetch with `git fetch --force --tags`: a plain fetch keeps old tags.

## What "author" means

The author of a commit is the act that made the change: `Legge costituzionale 1/2022`, `D.L. 207/2008`,
`D.Lgs. 101/2018`, with an address ending `@normattiva.invalid`, which cannot exist, so `git blame` names the act.
Judgments of the Constitutional Court that struck words out are authors too (`Corte costituzionale, sentenza 231/2013`,
`@cortecostituzionale.invalid`), as are corrections published in the Gazzetta Ufficiale (errata corrige, avvisi di
rettifica), which are labelled as corrections, not amendments. A decree-law is credited under its own number even
when its conversion law amended it; Normattiva records the pair under the decree-law.

How a change is credited, each labelled in the commit's `Evidence:` trailer:
- **Normattiva's per-article record.** For each article of each version, Normattiva's JSON export lists the provisions
  of other acts that produced the article's current wording ("articoliAggiornanti"), with the day that wording applies
  from. When the article changed in this version, that wording starts on this day, and one act is named, the change is
  that act's. Where two acts of the same Gazzetta are named, their codice redazionale tells them apart.
- **By date only.** An article Normattiva's record does not cover (a provision inserted, removed or renumbered, an
  annex), in a version whose update history adds exactly one act: that act.
- Units with no per-article record (the title, the preamble, the structure headings) in a version whose recorded
  changes all come from one act: that act.

A change no record explains is committed by `Normattiva (IPZS)`, labelled "modifica senza atto", and credited to no
act. Where two or more acts are possible it is labelled "atto non determinato" and names them in `Candidate:` trailers.
Where only Normattiva's presentation changed (the `(( ))` marks it puts around amended words, spacing, letter case) the
commit is labelled "redazionale" (`Editorial: yes`). The committer is always `Lexifina`.

## How it is checked

`tools/check_repo.py` reads every version of every act back from git on the day it took effect and compares it with
the official data: file by file, byte for byte, with the text the version's Akoma Ntoso file renders to, and word for
word with every word of that XML, read independently of the renderer. As a further check it compares the words with
Normattiva's JSON export of the same version. `tools/test_repo.py` checks that the commands above work. The results
are in [`REPRODUCE.md`](REPRODUCE.md).

## Files

Each act is a folder named by its type, year and number (`legge/1990/241/`, `decreto-legislativo/2003/196/`,
`legge-costituzionale/2001/3/`); the Constitution is `costituzione/`. Each article is one file named after Normattiva's
identifier: `art-117.md` is `art_117`, `art-002-quater.md` is `art_2-quater`. The first line is the article's number,
then its heading, then one line per paragraph (comma), letter and point. Normattiva's own notes on the article
("AGGIORNAMENTO (5)", the `((5))` references) stay where Normattiva prints them, at the end of the article, and the
`(( ))` marks around amended words are kept as Normattiva prints them. `intestazione.md` is the title and Normattiva's
note on entry into force, `preambolo.md` the enacting words, `conclusioni.md` the signatures, `allegati/` the annexes
(the Constitution's transitional and final provisions are `allegati/allegato-i.md` to `allegato-xviii.md`), and
`struttura.md` the headings of the parts, titles, chapters and sections, with the first article of each. Spacing is
normalised to single spaces; no word is changed.

## What it does not show

- Versions Normattiva does not publish. The record of each act starts with the text as published (the "originale"),
  in force on the day Normattiva gives.
- Which of two acts made a change when Normattiva's record cannot tell (above).
- Words unchanged does not mean law unchanged: a judgment, a transitional rule elsewhere, or a later act's
  interpretation can change what a provision means without changing its words. Normattiva's notes record some of these.
- Any act beyond these. The same build works for any act Normattiva Open Data exports: add it to `SOURCES` in
  `tools/build.py`.

Normattiva's text is not the official text: "L'unico testo ufficiale e definitivo è quello pubblicato sulla Gazzetta
Ufficiale Italiana a mezzo stampa, che prevale in casi di discordanza."

## How it is built

`tools/build.py` downloads the exports through the Normattiva Open Data API and writes this repository from scratch;
the same data gives the same hashes. Every step, the software, the decisions made by hand and what an AI model did are
in [`REPRODUCE.md`](REPRODUCE.md). Each act's folder has a `README.md` listing its provisions with how often each
changed. [`corpus.json`](corpus.json) describes the corpus for tools that read several of Lexifina's law repositories.

## Licence

The data comes from Normattiva Open Data and is used under the Creative Commons Attribution 4.0 International licence
(CC BY 4.0), which since 1 January 2026 covers every act on Normattiva in its original, point-in-time and multivigente
versions. Attribution: **Fonte: Normattiva (www.normattiva.it) - Istituto Poligrafico e Zecca dello Stato S.p.A.,
dati.normattiva.it, licenza CC BY 4.0. Testo non ufficiale e a titolo gratuito.** Changes made: the consolidated text
of each version is split into one file per provision with spacing normalised, and the versions are recorded as git
commits credited to the acts that made them. The whole repository is released under [CC BY 4.0](LICENSE) with the same
attribution.

---

## In italiano

La Costituzione, tutte le leggi costituzionali, lo Statuto dei lavoratori (L. 300/1970), la legge sul procedimento
amministrativo (L. 241/1990), il Codice in materia di protezione dei dati personali (D.Lgs. 196/2003) e il Codice
dell'amministrazione digitale (D.Lgs. 82/2005) come repository git, dal testo multivigente di Normattiva.

- **Ogni commit è un atto modificativo**, registrato come autore (`Legge costituzionale 1/2022`), così `git blame`
  mostra quale atto ha scritto ogni comma. L'atto è quello che Normattiva indica per l'articolo ("aggiornamenti").
- **Ogni commit porta la data di entrata in vigore della modifica**, a mezzogiorno a Roma. Nel messaggio ci sono anche
  la data dell'atto e quella di pubblicazione in Gazzetta Ufficiale.
- **Ogni articolo è un file**, ogni comma una riga.
- **Le modifiche che nessun atto spiega non sono attribuite a nessun atto**: il commit è di Normattiva e lo dice.

`python tools/vigente.py 2000-01-01 costituzione 117` stampa l'art. 117 della Costituzione com'era in vigore il
1 gennaio 2000. L'unico testo ufficiale e definitivo è quello pubblicato sulla Gazzetta Ufficiale.
