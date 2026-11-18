# Italian law in 20 charts

[Italiano](README.md)

Charts on every country's law, from the whole of global-law: [global-law visualisations/](https://github.com/lexifina/global-law/tree/main/visualisations). These are the charts on Italy alone.

Twenty charts on Italian law, drawn only from the data in this repository: the state acts in force as Normattiva publishes them, with the history of every version of the Constitution and of the four codes; the laws, bills and votes of the Camera and the Senate; the decisions of the Constitutional Court and the administrative courts; and the measures by which Italy transposes the directives of the European Union.

Open [`il-diritto-italiano-in-20-grafici.html`](il-diritto-italiano-in-20-grafici.html) in a browser. The page is one file with all its data inside; it loads only the d3 library and its fonts from the web. The controls at the top right switch the language (Italian or English) and the theme (light or dark). Each chart names its data path in the repository, its record count and its limits, and has a table of every number under it. Hover over a mark for the exact values.

The charts are descriptive: they show what the sources record, not why.

## The charts

### I. The law in force

#### 1. What is in force

The state acts in force by year of signature and kind: 64% date from before 1970; the oldest is from 1861.

![What is in force](stills/en/01.png)

#### 2. What remains in force

What the acts in force do, read from their titles: 47% concern a single body, from a parish to a foundation.

![What remains in force](stills/en/02.png)

#### 3. From signature to the Gazzetta

Days from signature to the Gazzetta Ufficiale, by kind of act and decade: 108 for presidential decrees of the 1980s, 8 for laws of the 2020s.

![From signature to the Gazzetta](stills/en/03.png)

#### 4. The next day or the fifteenth

When acts since 1988 take effect: 71% of ordinary laws on the fifteenth day, conversions and ratifications the next day.

![The next day or the fifteenth](stills/en/04.png)

### II. The Government as legislator

#### 5. Decrees to convert

Decrees presented to the Camera for conversion, year by year, and those reissued: 51% in 1993–1996, until judgment 360 of 1996.

![Decrees to convert](stills/en/05.png)

#### 6. Sixty days

Days between a decree-law and the law converting it: 59% of conversions come in the last ten of the sixty days.

![Sixty days](stills/en/06.png)

#### 7. Decree-laws by government

Decree-laws and lapses by government since 2006: 3.2 a month under the Meloni government, 35% lapsed under Conte II.

![Decree-laws by government](stills/en/07.png)

#### 8. The Milleproroghe

The year-end decree extending deadlines: in 21 of the last 25 years, always converted 38 to 65 days later.

![The Milleproroghe](stills/en/08.png)

### III. Parliament

#### 9. What Parliament passes

Each legislature's laws by subject: conversions of decree-laws go from 2% in the I to 35% in the XIX.

![What Parliament passes](stills/en/09.png)

#### 10. Who proposes and who gets passed

Bills presented and passed since 2006, by proposer: 52% of the Government's, 1.6% of members'.

![Who proposes and who gets passed](stills/en/10.png)

#### 11. The questione di fiducia

Every confidence vote in the Camera since 2001, by half-year and subject: 270 votes, 61 under the Meloni government.

![The questione di fiducia](stills/en/11.png)

#### 12. The calendar of laws

The day of the year of every law since 1948: 204 are dated 23 December, 195 fall on any day in September.

![The calendar of laws](stills/en/12.png)

#### 13. The budget and provisional budgets

Days from the start of the financial year to the State budget: a provisional budget for 33 of 41 budgets up to 1988, never since.

![The budget and provisional budgets](stills/en/13.png)

### IV. The Constitution and the codes

#### 14. The Constitution article by article

Every article and its last amendment: 98 of the 139 articles keep the 1948 text.

![The Constitution article by article](stills/en/14.png)

#### 15. The four codes over time

The versions of the four codes by decade: the Criminal Code has had 98 since 2020, 9 in the 1950s.

![The four codes over time](stills/en/15.png)

#### 16. The codes article by article

Every article of the four codes, amended or not: 73% of the Civil Code's original articles have never been amended.

![The codes article by article](stills/en/16.png)

### V. The courts and Europe

#### 17. The Constitutional Court

Judgments and orders by year, and the days from decision to deposit: 1,165 decisions in 1988; 35 days since 2015, 7 in 2005–2014.

![The Constitutional Court](stills/en/17.png)

#### 18. The Court's proceedings

The Court's decisions by kind of proceedings: direct actions go from 7% in 1990–2001 to 34% since 2012.

![The Court's proceedings](stills/en/18.png)

#### 19. Administrative courts

How long the appeals decided by the TARs had waited, by seat and region: five years or more for 30% in L'Aquila, 0.4% in Trento.

![Administrative courts](stills/en/19.png)

#### 20. EU directives

Measures transposing EU directives by kind of act: since 2000, 34% are legislative decrees; up to 1989, 0.3%.

![EU directives](stills/en/20.png)

## Data

As of commit `4b8df16640` (17 November 2026).

| Dataset | Where in the repository | Records | Coverage |
| --- | --- | ---: | --- |
| Git history | branch `main` | 4,052,201 commits | the date of each commit is the day in its `In-force:` trailer (1 January 1970 for earlier days, which the trailer keeps) |
| Acts in force | `normativa/<tipo>/<anno>/<numero>/` | 74,238 acts | Normattiva's text in force, acts from 1861 to 2026; every version of the Constitution and the four codes |
| Laws | `parlamento/schede/leggi/` | 17,037 laws | 1946–2026, the Camera's records |
| Camera bills | `parlamento/schede/camera/` | 105,842 bills | from the Kingdom (in part) to the XIX legislature |
| Senate bills | `parlamento/schede/senato/` | 56,425 phases | 1996 to 7 May 2024 |
| Camera votes | `parlamento/atti-parlamentari/camera/votazioni/` | 94,603 votes | 1996–2026 |
| Constitutional Court | `giurisprudenza/corte-costituzionale/` | 22,441 decisions | 1956–2026 |
| Administrative courts | `giurisprudenza/giustizia-amministrativa/` | 1,069,924 decisions | 2017–2026, metadata only |
| Transposition of directives | `eu-nim/` | 5,465 measures | 1958–2026, the European Commission's metadata |

## Limits

- **Only what is in force.** Normattiva publishes the text in force: repealed acts are not in the repository, so charts 1–4 count the acts in force today, not every act ever made.
- **Version dates.** The date of a version of the Constitution or a code is the first day Normattiva shows the new text, which can follow the entry into force by a few days; the amending act is given only as a candidate (charts 14–16).
- **Categories are read from titles.** The subject of the acts in force (chart 2), of laws (9) and of the deadline decrees (8), and the kind of transposition measure (20), come from words in titles, by the rules in `src/prep.py`. Whatever no rule recognises stays in "Other".
- **Gaps in the parliamentary sources.** The Senate's data stop on 7 May 2024 and give the initiative only from the XV legislature (charts 7 and 10); in the XIII legislature the Camera never marks the request for confidence (chart 11).
- **Administrative courts: metadata only.** The year of an appeal is read from its general register number (chart 19).
- **Partial periods** (2026, the XIX legislature) are drawn lighter and labelled as such.
- **Not used:** the Court of Audit (scattered years), the competition authority (a single data release date), the Senate's documents and votes, the Camera's speeches and motions.

## Rebuilding

```sh
python visualisations/src/make.py            # git history + trees + files -> src/.build/ -> il-diritto-italiano-in-20-grafici.html
node visualisations/src/stills.cjs           # images for these READMEs (needs Playwright; PLAYWRIGHT=<path> if not global)
```

`make.py` reads everything from git objects, so it also works in a blobless or `--no-checkout` clone: in a blobless clone it fetches the roughly 248,000 small files it reads, in batches. It reads `origin/main` (or `HEAD`) by default; `--ref` picks another branch or commit. It writes nothing into the repository except the page and the `src/.build/` folder (which git ignores).

| File | What it does |
| --- | --- |
| `src/make.py` | extracts the history, the trees and the files it needs into `src/.build/`, then runs `prep.py` and `build.py` |
| `src/prep.py` | computes every number for the 20 charts and the data profile into `src/.build/data.json` |
| `src/page.tpl.html` | the page: text in both languages, the charts (d3), the tables |
| `src/build.py` | puts `data.json` into the template and writes the page |
| `src/stills.cjs` | draws each chart as a PNG into `stills/it/` and `stills/en/` |
