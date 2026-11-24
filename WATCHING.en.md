<!-- lawwatch: written from data/checks by the check trail; edit the records, not this page -->

# Watching the sources: what is watched for Italy

[Italiano](WATCHING.md)

How global-law watches every country's sources: [global-law WATCHING.md](https://github.com/lexifina/global-law/blob/main/WATCHING.md). This page is the same for Italy only: every official source this repository takes text from, what is read on it, how often and when it was last read. Every read and what came of it: [monitoring/](monitoring/README.en.md).

| Source | What is read | Folders | How often | Last read | State |
| --- | --- | --- | --- | --- | --- |
| [Normattiva (Istituto Poligrafico e Zecca dello Stato)](https://www.normattiva.it) | the Gazzetta Ufficiale's feed of the Serie Generale and Normattiva's home page (new acts), then on Normattiva the text in force (AKN export) of each new act, of each held act a new act amends, of the four codes held with every version, and of a slice of the held acts each day (every held act within the sweep's cycle) | `normativa/`, `costituzione/` | daily | 2026-11-24 00:48 UTC | watched: dati.normattiva.it and api.normattiva.it (the open-data API) answer IPZS's protection page (HTTP 409) to this laptop and to the EU egress: not requested. Only legislation (normativa/, costituzione/) is checked against Normattiva; parlamento/, giurisprudenza/, autorita/ and eu-nim/ come from other sources and are not read by this check. |

Sources are read within their robots.txt and terms, with pauses between requests.
