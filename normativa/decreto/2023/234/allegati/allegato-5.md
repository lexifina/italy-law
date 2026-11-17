Articolo 10

Allegato 5

«Garanzie e misure di sicurezza»

1. Introduzione

Il presente allegato descrive le principali garanzie e misure di sicurezza dell'ANIST, in conformita' all'articolo 62-quater, comma 6, del CAD.

Per le predette finalita', l'ANIST e' dotata di:

- un sistema di Identity & Access Management per l'identificazione

dell'utente e della postazione, la gestione dei profili autorizzativi, la verifica dei diritti di accesso, il tracciamento delle operazioni;

- un sistema di tracciamento e di conservazione dei dati di accesso alle componenti applicative e di sistema;

- sistemi di sicurezza per la protezione delle informazioni e dei servizi erogati dalla base dati;

- un sistema di log analysis per l'analisi periodica dei file di log, in grado di individuare, sulla base di regole predefinite e formalizzate, eventi potenzialmente anomali e di segnalarli al Ministero dell'Istruzione e del merito tramite funzionalita' di alert;

- una Certification Authority;

- sistemi e servizi di backup per il salvataggio dei dati e delle applicazioni; - sistemi e servizi di Disaster Recovery.

Il piano di continuita' operativa esplicitera' le procedure relative ai sistemi ed ai servizi di backup e di Disaster Recovery.

2. Integrita' e riservatezza dei dati

L'integrita' (la protezione dei dati e delle informazioni nei confronti delle modifiche del contenuto, che siano accidentali oppure effettuate volontariamente da una terza parte) e la riservatezza dei dati presenti nelle banche dati sono garantite da opportune regole di profilazione e secondo il principio dei minimi privilegi necessari.

Tutti gli accessi, inoltre, sono tracciati e registrati in file di log.

La riservatezza dei dati e', inoltre, garantita attraverso l'adozione di misure di pseudonimizzazione tramite il disaccoppiamento dei dati e il mascheramento delle chiavi di correlazione. I dati ulteriori, necessari ai soli servizi di monitoraggio, sono memorizzati in forma pseudonimizzata in una sezione segregata e distinta della base dati ANIST.

Nel caso di servizi fruiti tramite il Portale ANIST, il non ripudio (condizione secondo la quale non si puo' negare la paternita' e la validita' del dato) e' garantito sia dalla non modificabilita' dei log di tracciamento, sia dall'identificazione certa dell'utente da parte del sistema informatico, mediante un meccanismo di autenticazione forte (metodo di autenticazione basato sull'utilizzo di piu' di un fattore di autenticazione) per l'accesso ai servizi.

L'integrita' e il non ripudio dei documenti scaricabili dal Portale ANIST sono garantiti attraverso l'apposizione di un sigillo elettronico ad ogni documento.

Per la fruizione dei servizi resi fruibili dalla PDND l'integrita' e il non ripudio sono garantiti dalle policy proprie della PDND.

3. Tracciamento delle operazioni effettuate

E' previsto un sistema di log analysis per l'analisi periodica delle informazioni registrate degli accessi applicativi, tale da individuare, sulla base di regole predefinite e formalizzate e attraverso l'utilizzo di indicatori di anomalie (alert), eventi potenzialmente anomali che possano configurare trattamenti illeciti.

I file di log registrano le informazioni riguardanti le operazioni per la verifica della correttezza e legittimita' del trattamento dei dati, presentando le caratteristiche di integrita' e inalterabilita', ed essendo protetti attraverso idonee misure contro ogni uso improprio.

Sono registrati anche i file di log relativi agli accessi e alle operazioni effettuate sulle basi dati, nonche' i log di servizio.

Sulla base di quanto monitorato dal sistema di log analysis, devono essere generati periodicamente dei report sintetici sullo stato di sicurezza del sistema (es. accessi ai dati, rilevamento delle anomalie, etc.).

Il periodo di retention dei dati e dei log sara' definito in apposita policy del Ministero dell'Istruzione e del merito e reso noto ai cittadini nelle informative che saranno rilasciate, rispettando il principio di non eccedenza e, piu' in generale, la normativa in materia di data protection.

4. Infrastruttura fisica

L'infrastruttura di ANIST e' installata nei locali individuati dal Ministero dell'istruzione e del merito aventi specifici requisiti di sicurezza che garantiscano la continuita' di servizio tramite soluzioni di alta affidabilita' (HA) e un rigido controllo dell'accesso anche fisico in ambienti ad accesso limitato e sottoposti a videosorveglianza continua.

Qualsiasi altra operazione manuale e' consentita solo a personale autorizzato dal Ministero dell'istruzione e del merito.

5. Protezione da attacchi informatici

Al fine di protezione dei sistemi operativi da attacchi informatici, eliminando le vulnerabilita', si utilizzano:

a) in fase di configurazione, procedure di hardening finalizzate a limitare l'operativita' alle sole funzionalita' necessarie per il corretto funzionamento dei servizi;

b) in fase di messa in esercizio, oltre che ad intervalli prefissati o in presenza di eventi significativi, processi di vulnerability assessment and mitigation nei software utilizzati e nelle applicazioni dei sistemi operativi;

c) piattaforma di sistemi firewall e sonde anti-intrusione;

d) ogni altra soluzione tecnologica aggiuntiva che sia utile all'innalzamento del livello di sicurezza e protezione del sistema.

Per proteggere i sistemi dagli attacchi informatici e' adottata una procedura di gestione degli incidenti informatici e sono, inoltre, rispettate le seguenti tecnologie e/o procedure:

a) aggiornamenti periodici dei sistemi operativi e dei software di sistema e hardening delle macchine;

b) adozione di una infrastruttura di sistemi firewall e sistemi IPS (Intrusion Prevention System), che consentono la rilevazione dell'esecuzione di codice non previsto nonche' di azioni in tempo reale quali il blocco del traffico proveniente da un indirizzo IP attaccante;

c) esecuzione di WAPT (Web Application Penetration Test), per la verifica della presenza di eventuali vulnerabilita' sul codice sorgente;

d) adozione di meccanismi, tipo captcha, sul Portale ANIST e di sistemi di rate-limit (limitanti il numero di transazioni nell'unita' di tempo), al fine di mitigare il rischio di accesso automatizzato alle applicazioni, che genererebbe un traffico finalizzato alla saturazione dei sistemi e quindi al successivo blocco del servizio;

e) presenza di sistemi di backup e disaster recovery. Il backup dovra' riguardare i seguenti elementi: dati, configurazioni dei sistemi, software applicativo, file di log e di alert.

6. Accesso

L'accesso all'ANIST avviene in condizioni di pieno isolamento operativo e di esclusivita', in conformita' ai principi di esattezza, disponibilita', accessibilita', integrita' e riservatezza dei dati, dei sistemi e delle infrastrutture di cui all'articolo 51 del CAD.

I sistemi di sicurezza garantiscono che l'infrastruttura di produzione sia logicamente distinta da altre infrastrutture, anche di competenza di soggetti terzi di cui il Ministero dell'istruzione e del merito si avvalga e che l'accesso alla stessa avvenga in modo sicuro, controllato, e costantemente tracciato, esclusivamente da parte di personale autorizzato dal Ministero dell'istruzione e del merito, e con il tracciamento degli accessi e di qualsiasi attivita' eseguita. L'ANIST invia e riceve le comunicazioni in modalita' sicura, su rete di comunicazione SPC ovvero, tramite Internet, mediante protocollo Transport Layer Security (TLS) per garantire la riservatezza dei dati su reti pubbliche secondo le pertinenti raccomandazioni AgID in materia (Determinazione n. 471 del 5 novembre 2020).
