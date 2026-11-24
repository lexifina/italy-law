<!-- lawwatch: written from data/checks by the check trail; edit the records, not this page -->

# Monitoring: what is read and what came of it

[Italiano](README.md)

How global-law monitors every country: [global-law monitoring/](https://github.com/lexifina/global-law/tree/main/monitoring). This page is the same for Italy only: every time an official source is read, when, and what came of it (acts added, changed and removed). The machine-readable form is [data/checks/](../data/checks/) (JSON Lines, schema `lexifina-check/1`), in `git log` as `Kind: check` commits, and month by month in [checks/](checks/).

**Last check:** 2026-11-24 01:21 UTC, Normattiva (Istituto Poligrafico e Zecca dello Stato): 638 addresses read; 0 added, 0 changed, 0 removed; changes found; 2 not published, 0 of them with no reason.

## Sources

| Source | Folders | How often | Last successful check | Last result | State |
| --- | --- | --- | --- | --- | --- |
| [Normattiva (Istituto Poligrafico e Zecca dello Stato)](https://www.normattiva.it) | `normativa/`, `costituzione/` | daily | 2026-11-24 01:21 UTC | changes found | watched: dati.normattiva.it and api.normattiva.it (the open-data API) answer IPZS's protection page (HTTP 409) to this laptop and to the EU egress: not requested. Only legislation (normativa/, costituzione/) is checked against Normattiva; parlamento/, giurisprudenza/, autorita/ and eu-nim/ come from other sources and are not read by this check. |

## The last 30 days

| Started (UTC) | Source | Read | Added | Changed | Removed | Not published (no reason) | Result | Commits |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| [2026-11-24 00:48](checks/2026-11.md#it-normattiva-20261124t004800z) | normattiva | 638 | 0 | 0 | 0 | 2 (0) | changes found | [4](https://github.com/lexifina/italy-law/compare/01737bf672e9...4cbeeb39dbdd) |

## Check it yourself

```
python tools/checktrail.py                      # the latest check of every source
python tools/checktrail.py --day 2026-11-23     # every check of a day
python tools/checktrail.py --act <id>           # when an act was seen and published
git log --grep='^Kind: check' --format='%ci %s'  # the checks in the history
```

Only the official publication has legal force; the texts here are copies for reading and searching.
