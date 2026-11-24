<!-- lawwatch: written from data/checks by the check trail; edit the records, not this page -->

# Sorveglianza delle fonti: che cosa si sorveglia per Italia

[English](WATCHING.en.md)

Come global-law sorveglia le fonti di ogni paese: [global-law WATCHING.md](https://github.com/lexifina/global-law/blob/main/WATCHING.md). Questa pagina fa lo stesso per Italia soltanto: ogni fonte ufficiale da cui questo repository prende il testo, che cosa vi si legge, con quale frequenza e quando è stata letta l'ultima volta. Ogni lettura e il suo esito: [monitoring/](monitoring/README.md).

| Fonte | Che cosa si legge | Cartelle | Frequenza | Ultima lettura | Stato |
| --- | --- | --- | --- | --- | --- |
| [Normattiva (Istituto Poligrafico e Zecca dello Stato)](https://www.normattiva.it) | il feed della Serie Generale della Gazzetta Ufficiale e la home page di Normattiva (atti nuovi), poi su Normattiva il testo vigente (export AKN) di ogni atto nuovo, di ogni atto presente qui che un atto nuovo modifica, dei quattro codici presenti con ogni versione e di una parte degli atti presenti qui ogni giorno (ogni atto entro il ciclo della rilettura) | `normativa/`, `costituzione/` | ogni giorno | 2026-11-24 00:48 UTC | sorvegliata: dati.normattiva.it e api.normattiva.it (l'API dei dati aperti) rispondono con la pagina di protezione dell'IPZS (HTTP 409) a questo computer e all'uscita UE: non sono interrogati. Solo la normativa (normativa/, costituzione/) è confrontata con Normattiva; parlamento/, giurisprudenza/, autorita/ ed eu-nim/ provengono da altre fonti e non sono letti da questo controllo. |

Le fonti si leggono nel rispetto del loro robots.txt e delle loro condizioni, con pause tra le richieste.
