Allegato A

Disciplinare tecnico

La scheda di dimissione ospedaliera (SDO) deve essere compilata per tutti i pazienti dimessi dagli istituti di cura pubblici e privati.

La SDO e' parte integrante della cartella clinica di cui costituisce una rappresentazione sintetica e fedele, finalizzata a consentire la raccolta sistematica, economica e di qualita' controllabile delle principali informazioni contenute nella cartella stessa.

La cartella clinica ospedaliera costituisce lo strumento informativo individuale finalizzato a rilevare tutte le informazioni anagrafiche e cliniche rilevanti, che riguardano un singolo ricovero ospedaliero di un paziente.

Ciascuna cartella clinica ospedaliera deve rappresentare l'intero ricovero del paziente nell'istituto di cura; essa, conseguentemente, coincide con la storia della degenza del paziente all'interno dell'istituto di cura. La cartella clinica ospedaliera ha, quindi, inizio al momento dell'accettazione del paziente da parte dell'istituto di cura, segue il paziente nel suo percorso all'interno dell'istituto di cura ed ha termine al momento della dimissione del paziente dall'istituto di cura.

L'eventuale trasferimento interno del paziente da una unita' operativa all'altra dello stesso istituto di cura non deve comportare la sua dimissione e successiva riammissione. Il numero identificativo, caratteristico di ciascuna cartella clinica e della relativa SDO, deve, pertanto, essere il medesimo per tutta la durata del ricovero, indipendentemente dai trasferimenti interni allo stesso istituto di cura. Fanno eccezione i casi di passaggio dal ricovero ordinario al ricovero diurno, o viceversa, e il passaggio da ricovero acuto a riabilitazione o lungodegenza, o viceversa. In questi ultimi casi si dovra' procedere alla compilazione di una nuova cartella clinica e di una nuova SDO.

In caso di ricovero diurno, la cartella clinica, e la corrispondente SDO, devono raccogliere la storia e la documentazione del paziente relative all'intero ciclo di trattamento; ogni singolo accesso giornaliero del paziente e' conteggiato come giornata di degenza e la data di dimissione corrisponde alla data dell'ultimo contatto con l'istituto di cura in cui si e' svolto il ciclo assistenziale; la cartella clinica, e la corrispondente SDO, relative ai ricoveri diurni, devono essere chiuse convenzionalmente alla data del 31 dicembre di ciascun anno, salvo dar luogo a una nuova cartella, e a una nuova SDO, per i cicli di trattamento in ricovero diurno che dovessero proseguire l'anno successivo.

Nel caso di trasferimento del paziente dal regime di ricovero diurno ad altro regime di ricovero, o viceversa, il paziente deve essere dimesso e dovra' essere compilata una nuova cartella clinica e una nuova SDO.

1. Introduzione.

Il presente allegato descrive le modalita' di trasmissione dei dati al Nuovo Sistema Informativo Sanitario (NSIS) relativi al sistema informativo sui dimessi dagli istituti di cura pubblici e privati, ed il dettaglio dei contenuti informativi da trasmettere.

Ogni variazione significativa alle caratteristiche tecniche descritte nel presente disciplinare e in generale, le novita' piu' rilevanti, sono rese pubbliche sul sito internet del Ministero della salute (www.nsis.salute.gov.it), secondo le modalita' previste dall'art. 54 del Codice dell'amministrazione digitale.

Coerentemente con le indicazioni contenute nel modello concettuale del Nuovo sistema informativo sanitario, il flusso di dati sui dimessi dagli istituti di cura pubblici e privati deve intercettare l'informazione relativa al singolo evento sanitario per consentire diverse e articolate forme di aggregazione e di analisi dei dati, non essendo possibile prevedere a priori tutti i possibili criteri di aggregazione degli eventi stessi al fine del calcolo degli indicatori.

2. Definizioni.

Ai fini del presente disciplinare tecnico si intende:

a. per «crittografia», tecnica per rendere inintelligibili informazioni a chi non dispone dell'apposita chiave di decifrazione e dell'algoritmo necessario;

b. per «crittografia simmetrica», un tipo di crittografia in cui la stessa chiave viene utilizzata per crittografare e decrittografare il messaggio, ovvero una chiave nota sia al mittente che al destinatario;

c. per «crittografia asimmetrica», un tipo di crittografia in cui ogni soggetto coinvolto nello scambio di informazioni dispone di una coppia di chiavi, una privata, da mantenere segreta, l'altra da rendere pubblica. L'utilizzo combinato delle chiavi dei due soggetti permette di garantire l'identita' del mittente, l'integrita' delle informazioni e di renderle inintelligibili a terzi;

d. per «sito Internet del Ministero», il sito istituzionale del Ministero della salute www.salute.gov.it accessibile dagli utenti per le funzioni informative relative alla trasmissione telematica dei dati;

e. per «XML», il linguaggio di markup aperto e basato su testo che fornisce informazioni di tipo strutturale e semantico relative ai dati veri e propri. Acronimo di «eXtensible Markup Language» metalinguaggio creato e gestito dal World Wide Web Consortium (W3C);

f. per «Centro Elaborazione Dati» o «CED», l'infrastruttura dedicata ai servizi di Hosting del complesso delle componenti tecnologiche del NSIS, dove i servizi di sicurezza fisica logica e organizzativa sono oggetto di specifiche procedure e processi;

g. per «DGSISS», la Direzione Generale della Digitalizzazione, del Sistema Informativo Sanitario e della Statistica del Ministero della salute;

h. per «Codice dell'amministrazione digitale» o «CAD», il decreto legislativo 7 marzo 2005 n. 82 e successive modificazioni.

3. I soggetti.

Le regioni e le Province autonome di Trento e di Bolzano si attengono alle specifiche di trasmissione attualmente in uso delle informazioni previste dal sistema informativo sui dimessi dagli istituti di cura pubblici e privati.

Le regioni e le province autonome individuano, inoltre, un soggetto responsabile della trasmissione dei dati al sistema informativo sui dimessi dagli istituti di cura pubblici e privati (di seguito Sistema).

4. Descrizione del sistema informativo.

4.1 Caratteristiche infrastrutturali.

Date le caratteristiche organizzative, le necessita' di scambio di informazioni tra sistemi eterogenei e le caratteristiche dei dati trattati, il Sistema e' basato su un'architettura standard del mondo Internet:

utilizza lo standard XML per definire in modo unificato il formato e l'organizzazione dei dati scambiati nelle interazioni tra le applicazioni;

attua forme di cooperazione applicativa tra sistemi;

prevede una architettura di sicurezza specifica per la gestione dei dati personali trattati.

E' costituito, a livello nazionale, da:

un sistema che ospita il front-end web dell'applicazione (avente la funzione di web server);

un sistema che ospita l'applicazione (avente la funzione di application server);

un sistema dedicato alla memorizzazione dei dati (data server); un sistema dedicato alla autenticazione degli utenti e dei messaggi;

un sistema dedicato a funzioni di Business Intelligence.

Tutti i sistemi sono collegati in rete locale e connessi alle infrastrutture comunicative attraverso firewall opportunamente configurati. Inoltre, la sicurezza degli stessi e' incrementata mediante:

strumenti IPS/IDS (Intrusion Prevention System/Intrusion Detection System) collocati nei punti di accesso alla rete al fine di consentire l'identificazione di attivita' ostili, ostacolando l'accesso da parte di soggetti non identificati e permettendo una reazione automatica alle intrusioni;

aggiornamenti dei software, secondo la tempistica prevista dalle case produttrici ovvero, periodicamente, a seguito di interventi di manutenzione;

configurazioni delle basi di dati per consentire un ripristino completo delle informazioni senza causarne la perdita di integrita' e disponibilita';

gruppi di continuita' che, in caso di mancanza di alimentazione elettrica di rete, garantiscono la continuita' operativa;

un sistema di gestione degli accessi e di profilazione utenti, che prevede anche, ove opportuno, strumenti di autenticazione forte; un sistema di tracciatura delle operazioni di accesso ai sistemi (sia tramite funzioni applicative o tramite accesso diretto), al fine di permettere l'individuazione di eventuali anomalie.

Le operazioni di accesso al sistema, tramite funzioni applicative o tramite accesso diretto, sono tracciate al fine di poter individuare eventuali anomalie.

4.1.1 Gestione dei supporti di memorizzazione

I supporti di memorizzazione, che includono nastri magnetici, dischi ottici e cartucce, possono essere fissi o rimovibili. Sui supporti di memorizzazione non vengono, comunque, conservate informazioni in chiaro; cio' malgrado, per ridurre al minimo il rischio di manomissione delle informazioni, viene identificato un ruolo di custode dei supporti di memorizzazione, al quale e' attribuita la responsabilita' della gestione dei supporti di memorizzazione rimovibili.

Per la gestione dei supporti di memorizzazione sono state adottate, in particolare, le seguenti misure:

tutti i supporti sono etichettati a seconda della classificazione dei dati contenuti;

viene tenuto un inventario dei supporti di memorizzazione secondo controlli predefiniti;

sono state definite ed adottate misure di protezione fisica dei supporti di memorizzazione;

i supporti di memorizzazione non piu' utilizzati saranno distrutti e resi inutilizzabili.

4.1.2 Misure idonee a garantire la continuita' del servizio

A garanzia della corretta operativita' del servizio sono state attivate procedure idonee a definire tempi e modi per salvaguardare l'integrita' e la disponibilita' dei dati e consentire il ripristino del sistema in caso di eventi che lo rendano temporaneamente inutilizzabile.

In particolare, per quel che riguarda i dati custoditi presso il Centro Elaborazione Dati (CED), sono previste:

procedure per il salvataggio periodico dei dati (backup sia incrementale che storico);

procedure che regolamentano la sostituzione, il riutilizzo e la rotazione dei supporti ad ogni ciclo di backup;

procedure per il data recovery;

procedure per la verifica dell'efficacia sia del backup che del possibile, successivo, ripristino.

La struttura organizzativa del CED e le procedure adottate consentono, in caso di necessita', di operare ripristino dei dati in un arco di tempo inferiore ai sette giorni.

4.2 Modalita' di abilitazione degli utenti

Gli utenti accedono ai servizi del NSIS attraverso gli strumenti definiti dalla vigente normativa (art. 64 del Codice dell'amministrazione digitale) per l'autenticazione telematica ai servizi erogati in rete dalle pubbliche amministrazioni.

In fase di prima attuazione, qualora compatibile con la tipologia dei dati trattati, come meglio specificato nei paragrafi che seguono, gli utenti possono accedere al sistema tramite credenziali di autenticazione generate secondo le modalita' riportate sul sito del Ministero, in conformita' all'art. 64 del Codice dell'amministrazione digitale.

Il NSIS dispone di un sistema di gestione delle identita' digitali, attraverso il quale vengono definiti i profili di autorizzazione previsti per ogni sistema, definiti secondo le logiche del Controllo degli accessi basato sui ruoli, declinati nello specifico in relazione al ruolo istituzionale, alle funzioni svolte e all'ambito territoriale delle azioni di competenza. Gli amministratori dell'applicazione, nominati dal Ministero della salute, gestiscono la designazione degli utenti e l'assegnazione dei privilegi di accesso.

Per l'accesso, l'architettura prevede un'abilitazione in due fasi.

4.2.1 Fase A - Abilitazione alla piattaforma NSIS.

La prima fase consente la registrazione da parte dell'utente mediante l'inserimento delle generalita' e del proprio indirizzo di posta elettronica ove ricevere le credenziali di autenticazione nonche' dei dettagli inerenti la struttura organizzativa di appartenenza. Successivamente, il sistema di registrazione invia una e-mail contenente l'identificativo e la password che l'utente e' obbligato a cambiare al primo accesso e, periodicamente, con cadenza trimestrale.

La parola chiave dovra' avere le seguenti caratteristiche:

sara' composta da almeno otto caratteri;

non conterra' riferimenti facilmente riconducibili all'incaricato.

Le credenziali di autorizzazione non utilizzate da almeno sei mesi sono disattivate.

4.2.2 Fase B - Abilitazione ai servizi

Nella seconda fase, l'utente (che viene definito utente NSIS) puo' chiedere l'abilitazione ad un profilo del un sistema informativo censito nel NSIS (in questo caso il «sistema informativo sui dimessi dagli istituti di cura pubblici e privati»). Il sistema permette di formulare richieste solo per le applicazioni associate alla struttura organizzativa di appartenenza dell'utente.

L'amministratore dell'applicazione effettua un riscontro della presenza del nominativo nella lista di coloro che sono stati formalmente designati dal referente competente (ad es. della regione o provincia autonoma di appartenenza). Qualora questa verifica abbia esito negativo, la procedura di registrazione si interrompe; nel caso in cui questa verifica abbia esito positivo, l'utente e' abilitato all'utilizzo del sistema.

Per garantire l'effettiva necessita', da parte del singolo utente NSIS, di accedere alle informazioni per le quali ha ottenuto un profilo di accesso, le utenze vengono, periodicamente, sottoposte a revisione e l'amministratore verifica, con i referenti competenti, il permanere degli utenti abilitati nelle liste delle persone autorizzate ad accedere all'NSIS e ai sistemi ad esso riconducibili. 4.2.3 Fase B - Regole speciali per l'abilitazione ai servizi che prevedono l'accesso a dati riferiti ai singoli assistiti

Nel caso in cui, per comprovate e documentate esigenze di validazione dei dati, il servizio per il quale e' richiesta l'abilitazione, preveda l'accesso a dati riferiti ai singoli assistiti, il processo di autenticazione degli utenti avviene esclusivamente da postazioni identificate e attraverso strumenti di autenticazione forte, in conformita' all'art. 64 del Codice dell'amministrazione digitale e all'art. 34 del decreto legislativo 30 giugno 2003, n. 196 e successive modificazioni. L'accesso e' garantito tramite l'utilizzo di un protocollo sicuro.

L'amministratore dell'applicazione effettua uno specifico riscontro della presenza del nominativo nella lista di coloro che sono stati designati, la cui gestione e' a cura del Ministero della salute. Qualora questa verifica abbia esito negativo la procedura di registrazione si interrompe; nel caso in cui questa verifica abbia esito positivo viene confermata all'utente la possibilita' di accedere a tali servizi e gli viene chiesto di indicare la postazione da cui intende accedere al servizio.

Infine, per rendere piu' sicuro il processo di abilitazione, un altro amministratore dell'applicazione, distinto dall'amministratore che ha generato le credenziali, provvede all'eventuale consegna dello strumento di autenticazione forte (se non gia' in possesso dell'utente che richiede l'abilitazione) e, in ogni caso, alla sua associazione alle suddette credenziali.

In nessun caso i servizi consentono di effettuare piu' accessi contemporanei con le medesime credenziali.

Inoltre, ad ulteriore garanzia dell'effettiva titolarita' da parte del singolo utente di accedere alla procedura:

le Unita' organizzative competenti segnalano tempestivamente il venir meno di tale titolarita' per gli utenti;

le utenze vengono, trimestralmente, sottoposte a revisione e l'amministratore verifica con i referenti dell'Unita' organizzativa competente, il permanere degli utenti abilitati, nelle liste delle persone autorizzate.

4.2.4 Sistema di registrazione delle operazioni di trattamento

Nel caso lo specifico servizio preveda il trattamento di dati individuali comprensivi di codici assegnati in luogo del codice identificativo dell'assistito, tutte le operazioni di accesso degli utenti sono registrate e i dati vengono conservati in appositi file di log, al fine di evidenziare eventuali anomalie e/o utilizzi impropri, anche tramite specifici alert.

Le informazioni registrate in tali file di log sono le seguenti: i dati identificativi del soggetto che ha effettuato l'accesso; la data e l'ora dell'accesso;

l'operazione effettuata.

I predetti file di log sono conservati in modalita' sicura e vengono trattati in forma aggregata, salvo la necessita' di verificare la correttezza e la liceita' delle singole operazioni effettuate. I file di log sono conservati per 12 mesi e cancellati alla scadenza.

4.3 Modalita' di trasmissione

La regione o provincia autonoma fornisce al Sistema le informazioni nei formati stabiliti nelle successive sezioni, scegliendo fra tre modalita' alternative:

a) utilizzando le regole tecniche di cooperazione applicativa del Sistema Pubblico di Connettivita' (SPC);

b) utilizzando i servizi applicativi che il Sistema mette a disposizione tramite il protocollo sicuro https e secondo le regole per l'autenticazione di cui a punto 3.2;

c) ricorrendo alla autenticazione bilaterale fra sistemi basata su certificati digitali emessi da un'autorita' di certificazione ufficiale.

A supporto degli utenti, il Sistema rende disponibile un servizio di assistenza raggiungibile mediante un unico numero telefonico da tutto il territorio nazionale, ogni ulteriore dettaglio e' reperibile sul sito istituzionale del Ministero all'indirizzo www.nsis.salute.gov.it

Le tempistiche di trasmissione ed i servizi di cooperazione applicativa sono pubblicati a cura del Ministero all'indirizzo www.nsis.salute.gov.it

4.3.1 Sistema Pubblico di Connettivita'

Il Sistema Pubblico di Connettivita' (SPC) e' definito e disciplinato all'art. 73 e seguenti del Codice dell'amministrazione digitale.

Le trasmissioni telematiche devono avvenire nel rispetto delle regole tecniche del SPC, cosi' come definito agli articoli 51 e 71 del Codice dell'amministrazione digitale.

4.3.2 Garanzie per la sicurezza della trasmissione dei flussi informativi

Nel caso in cui la regione o la provincia autonoma disponga di un sistema informativo in grado di interagire secondo le logiche di cooperazione applicativa, l'erogazione e la fruizione del servizio richiedono come condizione preliminare che siano effettuate operazioni di identificazione univoca delle entita' (sistemi, componenti software, utenti) che partecipano, in modo diretto e indiretto (attraverso sistemi intermedi) ed impersonando ruoli diversi, allo scambio di messaggi e alla erogazione e fruizione dei servizi.

In particolare occorrera' fare riferimento alle regole tecniche individuate ai sensi dell'art. 71 del Codice dell'amministrazione digitale.

Nel caso in cui il sistema informativo della regione o provincia autonoma non risponda alle specifiche di cui sopra, l'utente che debba procedere all'inserimento delle informazioni potra' accedere al Sistema, nell'ambito del NSIS, e inviare le informazioni attraverso una connessione sicura.

4.3.3 Standard tecnologici per la predisposizione dei dati

L'utente deve provvedere alla creazione e alla predisposizione di documenti conformi alle specifiche dell'Extensible Markup Language (XML) 1.0 (raccomandazione W3C 10 febbraio 1998).

Gli schemi standard dei documenti in formato XML contenenti le definizioni delle strutture dei dati dei messaggi da trasmettere, sono pubblicati, nella loro versione aggiornata, sul sito Internet del Ministero all'indirizzo www.nsis.salute.gov.it.

4.4 Servizi di analisi

Il Sistema e' stato strutturato per perseguire, tra gli altri, i seguenti obiettivi:

monitoraggio dell'attivita' dei servizi sanitari, con analisi del volume di prestazioni e valutazioni epidemiologiche sulle caratteristiche dell'utenza e sui pattern di trattamento;

supporto alle attivita' gestionali dei Servizi, per valutare il grado di efficienza e di utilizzo delle risorse;

supporto alla costruzione di indicatori di struttura, processo ed esito sia a livello regionale che nazionale;

il Sistema consente di accedere ad un apposita funzionalita' di reportistica che prevede due tipologie di utenti:

utenti del Ministero della salute;

utenti delle regioni o province autonome.

5. Ambito della rilevazione.

Il Sistema e' alimentato con informazioni sintetiche e fedeli della cartella clinica per tutti i pazienti dimessi dagli istituti di cura pubblici e privati.

6. Le informazioni.

Le regioni e le province autonome inviano i dati di cui all'art. 3, comma 3, del decreto al Ministero della salute, esclusivamente in modalita' elettronica in due tracciati distinti, di seguito indicati:

Tracciato A - che contiene le informazioni di carattere anagrafico;

Tracciato B - che contiene le informazioni relative al ricovero.

I dati anagrafici e sanitari sono, quindi, archiviati separatamente e i dati sanitari sono trattati con tecniche crittografiche. Le informazioni di dettaglio contenute nei due tracciati sono indicate nelle tabelle di cui alla successiva sezione 5.1.

Si rimanda al documento di specifiche funzionali per il dettaglio delle regole che disciplinano i tracciati record, indicazioni di dettaglio circa la struttura dei file XML e gli schemi XSD di convalida a cui far riferimento e le procedure di controllo e verifica dei dati trasmessi.

I valori di riferimento da utilizzare nella predisposizione dei file XML sono contenuti nel documento di specifiche funzionali pubblicate sul sito Internet del Ministero all'indirizzo www.nsis.salute.gov.it.

6.1 Contenuti informativi dei tracciati

La seguente tabella riporta, per ciascuna informazione di carattere anagrafico prevista dal presente decreto (art. 1, comma 2, sezione A) la definizione, fermo restando che per il dettaglio del relativo sistema di codifica, riconosciuto come standard nazionale per le regole che disciplinano i tracciati record, per le indicazioni di dettaglio circa la struttura dei file XML e gli schemi XSD di convalida a cui far riferimento e le procedure di controllo e verifica dei dati trasmessi si rimanda al documento di specifiche funzionali pubblicate sul sito Internet del Ministero all'indirizzo www.nsis.salute.gov.it

Parte di provvedimento in formato grafico

La seguente tabella riporta, per ciascuna informazione relativa al ricovero, prevista dal presente decreto (art. 1, comma 2, sezione B), la definizione, fermo restando che per il dettaglio del relativo sistema di codifica, riconosciuto come standard nazionale per le regole che disciplinano i tracciati record, per le indicazioni di dettaglio circa la struttura dei file XML e gli schemi XSD di convalida a cui far riferimento e le procedure di controllo e verifica dei dati trasmessi si rimanda al documento di specifiche funzionali pubblicate sul sito Internet del Ministero all'indirizzo www.nsis.salute.gov.it

Parte di provvedimento in formato grafico

6.2 Specifiche disposizioni per il trattamento dei dati identificativi del chirurgo e dell'anestesista

Al livello regionale i codici identificativi relativi al chirurgo e all'anestesista (campi 30-quinquies, 30-sexies, 34 e 35 del Tracciato B) sono oggetto del seguente, specifico trattamento, precedente all'invio dei dati al Ministero della salute. Le regioni e province autonome, mediante procedure automatiche procedono:

alla verifica di validita' dei predetti codici identificativi, attraverso uno scambio informativo con il servizio fornito dal sistema Tessera sanitaria;

alla sostituzione dei predetti codici identificativi con i corrispettivi codici univoci prodotti da una funzione non invertibile e resistente alle collisioni

(1) . Tale funzione e' rappresentata da un algoritmo di hash (2) che, applicato ad un codice identificativo (dato in input), produce un codice univoco (digest di output) dal quale non e' possibile risalire al codice identificativo di origine. L'algoritmo di hash adottato e' definito dalla DGSISS del Ministero della salute ed e' condiviso tra tutti i soggetti alimentanti, al fine di rendere il codice univoco non invertibile cosi' ottenuto, a fronte del codice identificativo di input unico sul territorio nazionale.

6.3 Procedura di verifica della validita' del codice identificativo

La procedura di verifica della validita' del codice identificativo, di cui al paragrafo 6.2 prevede uno scambio informativo con il servizio fornito dal sistema Tessera sanitaria.

Il servizio viene invocato, preventivamente alla sostituzione del codice identificativo con il codice univoco non invertibile, dai Soggetti alimentanti il sistema.

Tale servizio, a fronte di un codice identificativo in ingresso, restituisce le informazioni inerenti la sua validita' (valido o errato in quanto inesistente nella banca dati del sistema Tessera sanitaria), utilizzando, limitatamente ai soli campi indicati di seguito, il tracciato definito nel disciplinare tecnico, allegato 1 del decreto 22 luglio 2005 del Ministero dell'economia e delle finanze, di concerto con il Ministero della salute, attuativo del comma 9 dell'art. 50 del decreto-legge 30 settembre 2003, n. 269, convertito con modificazioni dalla legge 24 novembre 2003, n. 326, e successive modificazioni, nella sezione «Trasmissione dei dati relativi agli assistiti», come esposto nella tabella «Variazioni anagrafiche trasmesse dal Ministero dell'economia e delle finanze», integrato, a cura del Ministero dell'economia e delle finanze, dal campo A descritto in tabella:

Progressivo campo

Descrizione campo

6

Codice fiscale attuale

A

Informazione relativa alla presenza in banca dati del codice di cui si verifica la validita': 0 = Codice identificativo valido (presente in banca dati) 1 = Codice identificativo errato (non presente in banca dati)

Tabella 1 - Informazioni restituite nella procedura di verifica del codice fiscale del chirurgo e dell'anestesista

7. Formato elettronico delle trasmissioni.

La trasmissione dei dati e' effettuata esclusivamente in modalita' elettronica secondo le specifiche funzionali pubblicate sul sito internet del Ministero (www.nsis.salute.gov.it).

Le regioni e le province autonome inviano al livello nazionale del NSIS i dati raccolti e controllati. L'invio delle informazioni da parte della regione/provincia autonoma viene effettuato secondo il tracciato unico nazionale, riportato nel documento di specifiche funzionali.

Si rimanda al suddetto documento di specifiche funzionali e per indicazioni di dettaglio circa la struttura dei file XML nonche', il relativo documento XSD di convalida a cui far riferimento per le procedure di controllo e verifica dei dati trasmessi e alle modalita' di segnalazione ai soggetti interessati riguardo le anomalie riscontrate sui dati trasmessi.

8. Tempi di trasmissione.

Il Sistema e' alimentato con le informazioni relative alle dimissioni effettuate dagli istituti di cura nel periodo di riferimento, secondo le tempistiche indicate all'art. 4 comma 1.c del presente decreto.

(1) Per il dominio rappresentato dalla totalita' dei codici identificativi teoricamente possibili.

(2) La funzione di Hash dipendera' da una chiave di lunghezza adeguata alla dimensione e al ciclo di vita dei dati. (Si vedano in proposito le raccomandazioni ENISA contenute nel rapporto "Algorithms, Key Sizes and Parameters Report", October 2013 (https://www.enisa.europa.eu/activities/identity-and-trust/librar y/deliverables/algorithms-key-sizes-and-parameters-report).
