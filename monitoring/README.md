<!-- lawwatch: written from data/checks by the check trail; edit the records, not this page -->

# Monitoraggio: che cosa si legge e con quale esito

[English](README.en.md)

Come global-law monitora ogni paese: [global-law monitoring/](https://github.com/lexifina/global-law/tree/main/monitoring). Questa pagina fa lo stesso per Italia soltanto: ogni lettura di una fonte ufficiale, quando è avvenuta e con quale esito (atti aggiunti, modificati e rimossi). La forma leggibile dalle macchine è [data/checks/](../data/checks/) (JSON Lines, schema `lexifina-check/1`), in `git log` come commit `Kind: check`, e mese per mese in [checks/](checks/).

**Ultimo controllo:** 2026-11-24 01:21 UTC, Normattiva (Istituto Poligrafico e Zecca dello Stato): 638 indirizzi letti; 0 aggiunti, 0 modificati, 0 rimossi; modifiche trovate; 2 non pubblicati, di cui 0 senza motivo.

## Fonti

| Fonte | Cartelle | Frequenza | Ultimo controllo riuscito | Ultimo esito | Stato |
| --- | --- | --- | --- | --- | --- |
| [Normattiva (Istituto Poligrafico e Zecca dello Stato)](https://www.normattiva.it) | `normativa/`, `costituzione/` | ogni giorno | 2026-11-24 01:21 UTC | modifiche trovate | sorvegliata: dati.normattiva.it e api.normattiva.it (l'API dei dati aperti) rispondono con la pagina di protezione dell'IPZS (HTTP 409) a questo computer e all'uscita UE: non sono interrogati. Solo la normativa (normativa/, costituzione/) è confrontata con Normattiva; parlamento/, giurisprudenza/, autorita/ ed eu-nim/ provengono da altre fonti e non sono letti da questo controllo. |

## Gli ultimi 30 giorni

| Inizio (UTC) | Fonte | Letti | Aggiunti | Modificati | Rimossi | Non pubblicati (senza motivo) | Esito | Commit |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| [2026-11-24 00:48](checks/2026-11.md#it-normattiva-20261124t004800z) | normattiva | 638 | 0 | 0 | 0 | 2 (0) | modifiche trovate | [4](https://github.com/lexifina/italy-law/compare/01737bf672e9...4cbeeb39dbdd) |

## Verificalo da te

```
python tools/checktrail.py                      # l'ultimo controllo di ogni fonte
python tools/checktrail.py --day 2026-11-23     # tutti i controlli di un giorno
python tools/checktrail.py --act <id>           # quando un atto è stato visto e pubblicato
git log --grep='^Kind: check' --format='%ci %s'  # i controlli nella cronologia
```

Ha valore legale solo la pubblicazione ufficiale; i testi qui sono copie per la lettura e la ricerca.
