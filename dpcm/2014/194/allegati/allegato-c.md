Allegato C

Misure di sicurezza

Il presente allegato descrive le caratteristiche della piattaforma e le misure adottate per garantire l'integrita' e la riservatezza dei dati scambiati e conservati, la sicurezza dell'accesso ai servizi, il tracciamento delle operazioni effettuate, in conformita' agli articoli 64, comma 2 e 65, comma 1, lettera c), del decreto legislativo 7 marzo 2005, n. 82.

Per le predette finalita', l'ANPR e' dotata di:

un sistema di Identity & Access Management per

l'identificazione dell'utente e della postazione, la gestione dei profili autorizzativi, la verifica dei diritti di accesso, il tracciamento delle operazioni;

un sistema di tracciamento e di conservazione dei dati di accesso alle componenti applicative e di sistema;

sistemi di sicurezza per la protezione delle informazioni e dei servizi erogati dalla base dati;

un sistema di log analysis per l'analisi periodica dei file di log, in grado di individuare, sulla base di regole predefinite e formalizzate eventi potenzialmente anomali e di segnalarli al Ministero dell'interno tramite funzionalita' di alert;

una Certification Authority;

sistemi e servizi di backup per il salvataggio dei dati e delle applicazioni;

sistemi e servizi di Disaster Recovery.

Il piano di continuita' operativa di cui all'articolo 50-bis del decreto legislativo 7 marzo 2005, n. 82, esplicitera' le procedure relative ai sistemi ed ai servizi di backup e di Disaster Recovery.

1. Infrastruttura fisica

L'infrastruttura di ANPR e' installata nella sede della Societa' di cui all'articolo 1, comma 306, della legge 24 dicembre 2012, n. 228 (nel seguito "la Societa'") ed e' gestita dalla Societa' stessa.

I locali sono sottoposti a videosorveglianza continua e sono protetti da qualsiasi intervento di personale esterno, ad esclusione degli accessi necessari a garantire la continuita' operativa del sistema.

Qualsiasi altra operazione manuale e' consentita solo a personale autorizzato dal Ministero dell'interno.

La suddetta infrastruttura, oltre alle componenti di sicurezza, comprende i sistemi e le basi dati di cui al punto 4.1 dell'allegato al decreto del Presidente del Consiglio di Ministri 23 agosto 2013, n. 109.

2. Accesso alla base dati

L'accesso nell'ANPR avviene in condizioni di pieno isolamento operativo e di esclusivita', in conformita' ai principi di esattezza, disponibilita', accessibilita', integrita' e riservatezza dei dati, dei sistemi e delle infrastrutture, di cui all'articolo 51 del decreto legislativo n. 82 del 2005.

I sistemi di sicurezza garantiscono che l'infrastruttura di produzione sia logicamente distinta dalle altre infrastrutture della Societa' e che l'accesso alla stessa avvenga in modo sicuro, controllato, e costantemente tracciato, esclusivamente da parte di personale autorizzato dal Ministero dell'interno, e con il tracciamento degli accessi e di qualsiasi attivita' eseguita.

L'ANPR invia e riceve le comunicazioni in modalita' sicura, su rete di comunicazione SPC ovvero, tramite Internet, mediante protocollo SSL per garantire la riservatezza dei dati su reti pubbliche.

Le modalita' di accesso da parte dei comuni, delle pubbliche amministrazioni e degli organismi che erogano pubblici servizi si applicano fino alla piena attuazione delle disposizioni di cui all'articolo 64 del decreto legislativo n. 82 del 2005.

2.1 Accesso dei comuni

L'accesso dei comuni all'ANPR avviene tramite sito web o mediante web service.

Accesso del comune tramite sito web dell'ANPR.

I requisiti di sicurezza prevedono il riconoscimento dell'operatore e della postazione, autorizzata dal comune, e dotata dei seguenti dispositivi:

certificato identificativo, riferito alla postazione, memorizzato al suo interno, emesso dalla Certification Authority;

smart-card dedicata e personale, e relativo lettore, con certificato client di autenticazione, intestato all'operatore, emesso dalla Certification Authority.

L'infrastruttura di Identity & Access Management garantisce

l'autenticazione dell'utente e la verifica dei diritti di accesso dello stesso alle varie risorse, in base al relativo profilo autorizzativo.

L'operatore accede dalla postazione certificata autenticandosi tramite certificato client.

La postazione e' identificata mediante la connessione del browser dell'utente a un indirizzo gestito da un apparato di sicurezza specializzato, che verifica la validita' del certificato identificativo della postazione e, in caso di esito positivo, la validita' del certificato client.

Il sistema di Identity & Access management autorizza l'utente in

base al profilo assegnato ed effettua i controlli formali sui messaggi ricevuti.

Il sistema di tracciamento conserva le informazioni relative alla associazione utente - postazione - dati acceduti, inclusi i riferimenti temporali.

Tutte le informazioni relative al tracciamento dei dati sono accessibili solo dagli incaricati autorizzati su specifica richiesta da parte degli organi competenti.

Tutte le operazioni effettuate sono tracciate e conservate.

Accesso del comune mediante web service.

I requisiti di sicurezza prevedono:

il certificato identificativo, riferito alla postazione, memorizzato al suo interno, emesso dalla Certification Authority;

il riconoscimento dell'operatore tramite la userid e password utilizzata per accedere ai servizi dei sistemi informativi comunali, che garantiscono l'autenticazione dell'utente e la verifica dei diritti di accesso dello stesso alle varie funzionalita' applicative;

il certificato identificativo, riferito al server ospitante l'applicazione che utilizza il web service, memorizzato al suo interno, emesso dalla Certification Authority.

L'operatore accede autenticandosi tramite la userid e la password utilizzata per accedere ai servizi dei sistemi informativi comunali.

Per garantire il riconoscimento dell'operatore e della postazione, autorizzata dal comune, nonche' l'integrita' dei dati, i messaggi inviati prevedono:

identificativo postazione firmato con il certificato di postazione;

identificativo utente;

firma dell'intero messaggio mediante il certificato che identifica il server comune secondo i meccanismi standard della ws security.

Alla ricezione del messaggio, ANPR verifica la firma del messaggio ed il sistema di Identity & Access management verifica la

validita' dell'identificativo della postazione, nonche' l'esistenza dell'utente e la rispondenza dell'operazione richiesta in base al profilo assegnato; in caso di esito positivo, ANPR elabora il messaggio.

Il sistema di tracciamento conserva le informazioni relative all'associazione utente - postazione - dati acceduti, inclusi i riferimenti temporali.

Tutte le informazioni relative al tracciamento dei dati sono accessibili solo dagli incaricati autorizzati su specifica richiesta da parte degli organi competenti.

Tutte le operazioni effettuate sono tracciate e conservate.

Il comune garantisce l'adeguamento delle applicazioni alle regole di sicurezza descritte.

2.1.1 Registrazione degli utenti ed assegnazione degli strumenti di sicurezza

L'infrastruttura di Identity e Access Management censisce direttamente le utenze, accogliendo flussi di autenticazione e di autorizzazione, per l'assegnazione delle credenziali, secondo la seguente procedura:

a) il sindaco o suo delegato individua gli operatori comunali preposti all'accesso all'ANPR e ne comunica i nominativi al Ministero dell'interno, evidenziando gli operatori che saranno titolari di smart-card;

b) sulla base della comunicazione di cui al punto a), la societa' registra nel sistema di Identity e Access Management gli operatori comunali ed emette le smart-card richieste, e le trasmette alle Prefetture;

c) la societa' predispone i plichi che contengono i PIN/PUK e li trasmette ai comuni;

d) le Prefetture consegnano al sindaco le smart-card;

e) il sindaco individua l'Amministratore locale della sicurezza e, tramite la propria smart-card personale ed una specifica applicazione, registra le generalita' della persona individuata, gli consegna la smart card e il plico con i PIN/PUK, associa alla persona il ruolo di Amministratore locale della sicurezza, in possesso delle autorizzazioni descritte di seguito;

f) il sindaco comunica al Ministero dell'interno il nominativo dell'Amministratore locale della sicurezza, assicurando l'avvenuta consegna dei dispositivi;

g) l'Amministratore locale della sicurezza accede con la propria smart-card ad un'apposita applicazione dedicata alla gestione degli operatori comunali, consegna le smart-card e le relative buste con i PIN/PUK a ciascuno dei soggetti indicati dal sindaco ai sensi della lettera a), assegna i profili per l'accesso alle applicazioni, revoca le autorizzazioni, blocca le smart-card, richiede nuove smart-card in caso di impossibilita' di utilizzo di quella assegnata, registra nuovi operatori comunali, prenotando contestualmente la relativa smart-card che sara' successivamente recapitata dalla societa', con modalita' analoghe a quelle descritte al punto d);

h) il sindaco accede alla stessa applicazione, puo' effettuare tutte le operazioni previste per l'Amministratore locale della sicurezza nonche' la revoca delle autorizzazioni.

Tutte le funzionalita' di sicurezza descritte ai punti precedenti sono disponibili all'interno di un'apposita Web application, cui si accede con autenticazione forte e canale sicuro: la smart-card, pertanto, deve essere necessariamente richiesta per l'Amministratore locale della sicurezza, oltre che per gli operatori comunali che avranno accesso al sito Web di ANPR.

Tramite la suddetta applicazione sono distribuiti i certificati che saranno utilizzati per il riconoscimento delle postazioni.

La gestione e la conservazione della smart-card e' di esclusiva responsabilita' dell'operatore cui e' assegnata, mentre la gestione e la conservazione del certificato che identifica la postazione, memorizzato internamente ad essa, e' di responsabilita' di un dipendente del Comune appositamente individuato quale responsabile del certificato stesso. La non esportabilita' di questo certificato dalla postazione e' garantita dalla presenza di un codice PIN, generato in fase di installazione sulla specifica postazione destinataria, la cui conservazione e' di esclusiva responsabilita' del suddetto dipendente.

Per la gestione dei processi autorizzativi, sono previsti i seguenti ruoli amministrativi, suddivisi tra gli attori del sistema:

a) Amministratore di Infrastruttura;

b) Amministratore Applicativo;

c) Amministratore Centrale della Sicurezza;

d) Amministratori locali;

e) Amministratore di primo livello (Sindaco o suo delegato);

f) Amministratore di secondo livello (Amministratore locale della sicurezza);

g) Amministratore della postazione (responsabile dei certificati di postazione).

I primi due ruoli sono attribuiti a personale della Societa' dalla stessa individuato e comunicato al Ministero dell'interno.

Il terzo ruolo e' attribuito al personale del Ministero dell'interno.

2.2 Accesso delle pubbliche amministrazioni e degli organismi che erogano pubblici servizi

L'accesso delle pubbliche amministrazioni e degli organismi che erogano pubblici servizi all'ANPR avviene tramite sito web o mediante web service.

Per l'accesso tramite sito web, i requisiti di sicurezza prevedono il riconoscimento dell'operatore e della postazione, autorizzata dalla pubblica amministrazione o dall'ente, sulla base del Sistema di Identita' Federata, (che contempla anche l'identificativo dell'operatore e l'indirizzo IP della postazione), che consente il controllo degli accessi ai soli servizi di consultazione ed estrazione.

Nel modello di sicurezza dell'Identita' Federata, nell'ambito dell'Access & Facility Management, alle pubbliche amministrazioni e

agli enti che erogano pubblici servizi sono demandate le funzioni di autenticazione e di autorizzazione, all'interno di profili prestabiliti, assumendo rispettivamente i ruoli di Identity Provider e Attribute Authority, in conformita' al modello GFID dell'Agenzia per l'Italia Digitale e mediante l'adozione di soluzioni tecnologiche che garantiscano il tracciamento sia dell'Identity Provider sia dell'operatore.

Le operazioni effettuate presso la postazione sono registrate nel sistema di Identity e Access Management, che registra le informazioni di autenticazione e gli attributi e li utilizza per verificare i diritti di accesso all'informazione e per alimentare il sistema di tracciamento.

Per l'accesso tramite web service, si utilizzano i meccanismi propri del pattern di sicurezza che consente, ove richiesto, di trasferire, ai fini del tracciamento, oltre all'identificativo dell'ente anche l'identificativo dell'utente finale e l'indirizzo IP della sua postazione. Il server applicativo viene identificato tramite apposito certificato.

3. Sistema di monitoraggio dei servizi

Il Ministero dell'interno, attraverso l'infrastruttura di cui al paragrafo 1, eroga i servizi di cui all'allegato D e assolve le funzionalita' di sicurezza descritte nel presente allegato, nel rispetto delle specifiche tecniche elaborate dalla Societa' e approvate dal Ministero.

Per il monitoraggio dei servizi, il Ministero dell'interno si avvale di uno specifico sistema, ubicato nel Centro Nazionale per i Servizi Demografici del Ministero dell'interno (CNSD), presso il quale sono installate apposite consolle di controllo, utilizzate esclusivamente da personale autorizzato dal Ministero dell'interno per l'accesso in sola visualizzazione.

La visualizzazione completa dello stato del servizio e dell'infrastruttura tecnologica che lo supporta avviene mediante:

a) vista c.d. "ad albero" dei servizi che rendono disponibili le seguenti informazioni:

lista dei servizi erogati (nome, descrizione, codifica, etc.);

infrastruttura tecnologica che ospita i servizi erogati con il dettaglio dei servizi tecnici che li compongono;

allarmi associati alle risorse infrastrutturali dei servizi tecnici che hanno impatto sui servizi erogati;

eventuali ticket di incidenti aperti dalla Societa' di cui all'articolo 1, comma 306, della legge 24 dicembre 2012, n. 228, per la gestione e la risoluzione degli allarmi.

b) vista di alto livello con rappresentazione, sia real time sia giornaliera, dell'andamento dello stato dei servizi erogati e dei relativi indicatori di disponibilita' (eventi di infrastruttura, eventi da sonde end-to-end, ticket di incidenti);

c) rappresentazione dell'andamento della produzione dei servizi, in funzione dei livelli di autorizzazione definiti dal Ministero dell'interno, anche in termini di analisi delle interazioni del sistema con i soggetti che accedono (comuni, pubbliche amministrazioni, ed altri enti) e degli scostamenti dal trend, compresi report sintetici sullo stato di sicurezza del sistema.

4. Protezione da attacchi informatici

Al fine di protezione dei sistemi operativi da attacchi informatici, eliminando le vulnerabilita', si utilizzano:

a) in fase di configurazione, procedure di hardening finalizzate a limitare l'operativita' alle sole funzionalita' necessarie per il corretto funzionamento dei servizi;

b) in fase di messa in esercizio, oltre che ad intervalli prefissati o in presenza di eventi significativi, processi di vulnerability assessment and mitigation nei software utilizzati e nelle applicazioni dei sistemi operativi;

c) piattaforma di sistemi firewall e sonde anti-intrusione.
