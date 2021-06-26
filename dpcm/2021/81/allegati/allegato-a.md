Allegato A

(articolo 2)

Tassonomia degli incidenti

((TABELLA 1))

((

=====================================================================

| Identificativo | | |

| (incidente con | | |

| impatto ICP) | Categoria | Descrizione |

+================+==============+===================================+

| | |Infezione (Initial exploitation). |

| | |Il soggetto ha evidenza |

| | Infezione |dell'effettiva esecuzione non |

| ICP-A-1 | (Initial |autorizzata di codice o malware |

| |exploitation) |veicolato attraverso vettori di |

| | |infezione o sfruttando |

| | |vulnerabilita' di risorse esposte |

| | |in rete. |

+----------------+--------------+-----------------------------------+

| | |Violazione del livello di servizio |

| | |atteso, definito dal soggetto |

| | |incluso nel perimetro ai sensi di |

| ICP-A-2 | |quanto previsto nelle misure di |

| | |sicurezza di cui all'allegato B, in|

| | |termini di risorse di calcolo, |

| | |memoria e/o banda passante. |

+----------------+ +-----------------------------------+

| | |Violazione del livello di servizio |

| | |atteso, definito dal soggetto |

| | |incluso nel perimetro ai sensi di |

| ICP-A-3 | |quanto previsto nelle misure di |

| | |sicurezza di cui all'allegato B, di|

| | |hot-replica e/o cold-replica e/o |

| | |sito(i) di disaster recovery, se |

| | |previsti. |

+----------------+ +-----------------------------------+

| | |Violazione del livello di servizio |

| | |atteso, definito dal soggetto |

| | |incluso nel perimetro ai sensi di |

| | |quanto previsto nelle misure di |

| ICP-A-4 | |sicurezza di cui all'allegato B, in|

| | |termini di indisponibilita', di |

| | |perdita irreversibile o di |

| | |corruzione irreversibile dei dati |

| | |provenienti dalle componenti di |

| | |campo (attuatori e sensori). |

+----------------+Guasto (Fault)+-----------------------------------+

| | |Dati hot-replica e/o cold-replica |

| | |e/o sito(i) di disaster recovery |

| ICP-A-5 | |e/o backup, se previsti, persi o |

| | |corrotti in modo irreversibile. |

+----------------+ +-----------------------------------+

| | |Perdita di confidenzialita' o |

| ICP-A-6 | |integrita'. |

+----------------+ +-----------------------------------+

| | |Perdita e/o corruzione dati |

| ICP-A-7 | |irreversibile. |

+----------------+ +-----------------------------------+

| | |Perdita e/o compromissione di |

| ICP-A-8 | |chiavi di cifratura e/o |

| | |certificati. |

+----------------+ +-----------------------------------+

| | |Perdita e/o compromissione di |

| ICP-A-9 | |credenziali utenti. |

+----------------+ +-----------------------------------+

| | |Violazione del livello di servizio |

| | |atteso, definito dal soggetto |

| | |incluso nel perimetro ai sensi di |

| ICP-A-10 | |quanto previsto dalle misure di |

| | |sicurezza di cui all'allegato B, in|

| | |termini di impossibilita' di |

| | |accesso fisico alle componenti. |

+----------------+--------------+-----------------------------------+

| | |Ottenimento di privilegi di livello|

| | |superiore (Privilege Escalation). |

| | |Il soggetto ha evidenza |

| ICP-A-11 | |dell'impiego non autorizzato di |

| | |tecniche, condotte dall'interno |

| | |della rete, utili ad ottenere |

| | |permessi di livello superiore. |

+----------------+ +-----------------------------------+

| | |Persistenza (Persistence). Il |

| | |soggetto ha evidenza dell'impiego |

| | |non autorizzato di tecniche, |

| ICP-A-12 |Installazione |condotte dall'interno della rete, |

| | (Establish |utili ad ottenere persistenza di |

| | Persistence) |codice malevolo o d'accesso. |

+----------------+ +-----------------------------------+

| | |Evasione delle difese (Defence |

| | |Evasion). Il soggetto ha evidenza |

| | |dell'impiego non autorizzato di |

| ICP-A-13 | |tecniche attraverso cui sono stati |

| | |effettivamente elusi i sistemi di |

| | |sicurezza. |

+----------------+ +-----------------------------------+

| | |Comando e Controllo (Command and |

| | |Control). Il soggetto ha evidenza |

| ICP-A-14 | |di comunicazioni non autorizzate |

| | |verso l'esterno della rete. |

+----------------+--------------+-----------------------------------+

| | |Esplorazione (Discovery). Il |

| | |soggetto ha evidenza dell'impiego |

| | |non autorizzato di tecniche, |

| ICP-A-15 | |condotte dall'interno della rete, |

| | |utili a effettuare attivita' di |

| | |ricognizione. |

+----------------+ +-----------------------------------+

| | |Raccolta di credenziali (Credential|

| | |Access). Il soggetto ha evidenza |

| | Movimenti |dell'impiego non autorizzato di |

| | laterali |tecniche utili ad acquisire, |

| ICP-A-16 | (Lateral |dall'interno della rete, |

| | Movement) |credenziali valide per |

| | |l'autenticazione alle risorse di |

| | |rete o ne rinviene copie non |

| | |autorizzate. |

+----------------+ +-----------------------------------+

| | |Movimenti laterali (Lateral |

| | |Movement). Il soggetto ha evidenza |

| | |dell'impiego non autorizzato di |

| ICP-A-17 | |tecniche utili ad accedere o |

| | |eseguire codice tra risorse interne|

| | |della rete. |

+----------------+--------------+-----------------------------------+

| | |Raccolta (Collection). Il soggetto |

| | |ha evidenza dell'impiego non |

| | |autorizzato di tecniche utili a |

| ICP-A-18 | |raccogliere, dall'interno della |

| | |rete, dati di interesse di terze |

| | |parti o ne rinviene copie non |

| | |autorizzate. |

+----------------+ +-----------------------------------+

| | Azioni sugli |Esfiltrazione (Exfiltration). Il |

| | obiettivi |soggetto ha evidenza dell'impiego |

| ICP-A-19 | (Action on |non autorizzato di tecniche utili |

| | objs) |ad esfiltrare dati dall'interno |

| | |della rete verso risorse esterne. |

+----------------+ +-----------------------------------+

| | |Accesso non autorizzato o con abuso|

| | |dei privilegi concessi. Il soggetto|

| | |ha evidenza, anche sulla base di |

| | |parametri quali-quantitativi, |

| ICP-A-20 | |dell'accesso non autorizzato o con |

| | |abuso dei privilegi concessi, |

| | |dall'interno della rete, a dati |

| | |digitali. |

+----------------+--------------+-----------------------------------+

))

TABELLA 2

====================================================================+

|Identificativo| Categoria | Descrizione |

+==============+=============+======================================+

| ICP-B-1 | |Inibizione delle funzioni di risposta |

| | |(Inhibit Response Function). Il |

| | |soggetto ha evidenza dell'impiego non |

| | |autorizzato di tecniche utili a |

| | |inibire l'intervento delle funzioni di|

| | |sicurezza, di protezione e di "quality|

| | |assurance" dei sistemi di controllo |

| | |industriale predisposte per rispondere|

| | |a un disservizio o a uno stato |

| | |anomalo. |

+--------------+ +--------------------------------------+

| | |Compromissione dei processi di |

| |Azioni sugli |controllo (Impair Process Control). Il|

| | obiettivi |soggetto ha evidenza dell'impiego non |

| ICP-B-2 | (Actions on |autorizzato di tecniche utili a |

| | objectives) |manipolare, disabilitare o danneggiare|

| | |i processi di controllo fisico di |

| | |sistemi di controllo industriale. |

+--------------+ +--------------------------------------+

| ICP-B-3 | |Disservizio intenzionale (Impact). Il |

| | |soggetto ha evidenza dell'impiego non |

| | |autorizzato di tecniche utili a |

| | |manipolare, degradare, interrompere o |

| | |distruggere i sistemi, i servizi o i |

| | |dati. In tale ambito rientrano ad |

| | |esempio gli eventi di tipo Denial of |

| | |Service/Distributed Denial of Service |

| | |che hanno impatto sui beni ICT. |

+--------------+-------------+--------------------------------------+

| ICP-B-4 | |Violazione del livello di servizio |

| | |atteso, definito dal soggetto incluso |

| | |nel perimetro ai sensi di quanto |

| | |previsto nelle misure di sicurezza di |

| | |cui all'allegato B, specie in termini |

| | Disservizio |di disponibilita', del bene ICT. |

+--------------+ (Failure) +--------------------------------------+

| ICP-B-5 | |Divulgazione di dati corrotti o |

| | |esecuzione operazioni corrotte tramite|

| | |il bene ICT. |

+--------------+ +--------------------------------------+

| ICP-B-6 | |Divulgazione non autorizzata di dati |

| | |digitali relativi ai beni ICT. |

+--------------+-------------+--------------------------------------+
