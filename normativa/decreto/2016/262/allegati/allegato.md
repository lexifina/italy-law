Allegato

Disciplinare tecnico

Sommario

1 Introduzione e obiettivi del documento

2 Definizioni

3 I soggetti

4 Descrizione della piattaforma NSIS

4.1 Caratteristiche infrastrutturali

4.1.1 Gestione dei supporti di memorizzazione

4.1.2 Misure idonee a garantire la continuita' del servizio

4.2 Modalita' di abilitazione degli utenti

4.2.1 Fase A - Abilitazione alla piattaforma NSIS

4.2.2 Fase B - Abilitazione ai servizi

4.2.3 Fase B - Regole speciali per l'abilitazione ai servizi che prevedono l'accesso a informazioni riferite ai singoli assistiti

4.2.4 Abilitazione alla piattaforma codice univoco nazionale assistito

4.3 Sistema di registrazione delle operazioni di trattamento

4.4 Modalita' di trasmissione dei dati dei sistemi informativi alimentanti il NSIS

4.5 Garanzie per la sicurezza delle basi dati

4.6 Servizi applicativi (reportistica ed analisi)

5 La procedura di assegnazione del codice univoco nazionale dell'assistito

5.1 Assegnazione del codice univoco non invertibile ("CUNI") da parte dei soggetti alimentanti il NSIS

5.2 Assegnazione del codice univoco non invertibile (CUNI) da parte del Ministero della salute per il flusso SDO

5.3 Assegnazione del codice univoco nazionale dell'assistito (CUNA)

5.4 Procedure per il trattamento dei dati di specifiche coorti di assistiti

6 Procedura di verifica della validita' del codice identificativo

7 Schema logico del Sistema di Integrazione delle Informazioni Sanitarie Individuali

1 Introduzione e obiettivi del documento

Nel contesto di profonda evoluzione del Servizio sanitario nazionale, la Conferenza permanente per i rapporti tra lo Stato, le regioni e le province autonome di Trento e di Bolzano ha siglato, il 22 febbraio 2001, l'Accordo quadro per lo sviluppo del Nuovo Sistema Informativo Sanitario Nazionale (NSIS). Il disegno di un nuovo sistema informativo sanitario si propone quale strumento essenziale per il governo della sanita' a livello nazionale, regionale e locale e per migliorare l'accesso alle strutture e la fruizione dei servizi da parte dei cittadini - utenti.

Il protocollo d'intesa del 23 marzo 2005 e, successivamente, il Patto per la Salute del 28 settembre 2006 hanno ribadito l'utilizzo del NSIS per le misure di qualita', efficienza ed appropriatezza del Servizio sanitario nazionale, evidenziando il conferimento dei dati al Nuovo Sistema Informativo Sanitario «fra gli adempimenti a cui sono tenute le regioni».

Il Sistema di integrazione delle Informazioni Sanitarie Individuali (SIISI), inserito nell'ambito del NSIS, e' il sistema di supporto ai diversi livelli del Servizio sanitario nazionale (locale/regionale e nazionale), ideato ed implementato secondo il principio che e' necessario intercettare l'informazione relativa al singolo evento sanitario, su base individuale, per consentire diverse e articolate forme di aggregazione e di analisi dei dati, non essendo possibile prevedere a priori tutti i possibili criteri di aggregazione degli eventi stessi al fine del perseguimento delle finalita' del NSIS.

In considerazione della rilevanza delle procedure derivanti dall'attuazione delle disposizioni di cui al presente decreto, il Ministero della salute (di seguito Ministero) adotta il presente disciplinare tecnico che descrive le caratteristiche tecniche del NSIS, le modalita' di trattamento e le misure di sicurezza previste, con particolare riferimento alla gestione dei sistemi informativi su base individuale.

Ogni variazione significativa alle caratteristiche descritte nel presente disciplinare e' resa pubblica sul sito Internet del Ministero (www.nsis.salute.gov.it), secondo le modalita' previste dall'art. 54 del Codice dell'amministrazione digitale.

Il presente disciplinare tecnico definisce:

la procedura di verifica della validita' del codice identificativo, in attuazione di quanto gia' indicato nell'art. 3, comma 1, lettera a) e nell'art. 8, comma 4, lettera a);

la procedura di assegnazione del codice univoco non invertibile (CUNI), in attuazione di quanto gia' indicato nell'art. 3, comma 1, lettera b);

le specificazioni per l'invio dei dati al NSIS, in attuazione di quanto gia' indicato nell'art. 3, comma 2;

la procedura di assegnazione del codice univoco non invertibile (CUNI) da parte del Ministero della salute per il flusso SDO, in attuazione di quanto gia' indicato nell'art. 8, comma 3;

la procedura di assegnazione del codice univoco nazionale dell'assistito (CUNA), in attuazione di quanto gia' indicato nell'art. 3, comma 3;

la procedura di verifica della validita' del codice identificativo e di aggiornamento dei dati, in attuazione di quanto gia' indicato nell'art. 3, comma 4 e nell'art. 8, comma 4;

la procedura di selezione, estrazione ed elaborazione di dati riferiti ad individui presenti in specifici elenchi o coorti, in attuazione di quanto gia' indicato nell'art. 4, comma 3;

le misure di sicurezza adottate per gli accessi al NSIS, quali: le modalita' di abilitazione degli utenti, il sistema di tracciatura degli accessi ai dati personali, le modalita' di trasmissione dei dati dei sistemi informativi alimentanti il NSIS e le garanzie per la sicurezza delle basi dati, in attuazione di quanto gia' indicato nell'art. 6, comma 6.

2 Definizioni

Ai fini del presente disciplinare tecnico si intende per:

a) crittografia: tecnica per rendere inintelligibili informazioni a chi non dispone dell'apposita chiave di decifrazione e dell'algoritmo necessario;

b) crittografia simmetrica: un tipo di crittografia in cui la stessa chiave viene utilizzata per crittografare e decrittografare il messaggio, ovvero una chiave nota sia al mittente che al destinatario;

c) crittografia asimmetrica: un tipo di crittografia in cui ogni soggetto coinvolto nello scambio di informazioni dispone di una coppia di chiavi, una privata, da mantenere segreta, l'altra da rendere pubblica. L'utilizzo combinato delle chiavi dei due soggetti permette di garantire l'identita' del mittente, l'integrita' delle informazioni e di renderle inintelligibili a terzi;

d) sito Internet del Ministero: il sito istituzionale del Ministero della salute www.salute.gov.it accessibile dagli utenti per le funzioni informative relative alla trasmissione telematica dei dati;

e) XML: il linguaggio di markup aperto e basato su testo che fornisce informazioni di tipo strutturale e semantico relative ai dati veri e propri. Acronimo di "eXtensible Markup Language" metalinguaggio creato e gestito dal World Wide Web Consortium (W3C);

f) Centro Elaborazione Dati o CED: l'infrastruttura dedicata ai servizi di Hosting del complesso delle componenti tecnologiche del NSIS, dove i servizi di sicurezza fisica logica e organizzativa sono oggetto di specifiche procedure e processi;

g) DGSISS: la Direzione Generale della Digitalizzazione, del Sistema Informativo Sanitario e della Statistica del Ministero della salute;

h) CUNI: il codice univoco non invertibile;

i) CUNA: il codice univoco nazionale dell'assistito;

l) SDO, le schede di dimissione ospedaliera di cui al decreto del Ministro della sanita' del 27 ottobre 2000, n. 380, e successive modificazioni.

3 I soggetti

I soggetti che alimentano il NSIS e che effettuano le procedure di cui agli articoli 3 e 8 sono i seguenti:

le regioni e le province autonome di Trento e di Bolzano (art. 3, commi 1 e 2 e art. 8, commi 3 e 4, lettera a));

il Ministero dell'economia e delle finanze (art. 3, commi 1, 2, e 4 nelle more dell'attivazione dell'Anagrafe nazionale degli assistiti, istituita ai sensi dell'art. 62-ter del CAD, art. 8, comma 4);

Il Ministero della salute (art. 3, commi 3 e 4, e art. 8, commi 3 e 4, lettera b).

4 Descrizione della piattaforma NSIS

4.1 Caratteristiche infrastrutturali

Date le caratteristiche organizzative, le necessita' di scambio di informazioni tra sistemi eterogenei e le caratteristiche dei dati trattati, il NSIS e' basato su un'architettura standard del mondo Internet:

utilizza lo standard XML per definire in modo unificato il formato e l'organizzazione dei dati scambiati nelle interazioni tra le applicazioni;

attua forme di cooperazione applicativa tra sistemi;

prevede un'architettura di sicurezza specifica per la gestione dei dati personali trattati.

Ogni sistema informativo che ne fa parte, e' costituito, a livello nazionale, da:

un sistema che ospita il front-end web del sistema informativo (avente la funzione di web server);

un sistema che ospita il sistema informativo (avente la funzione di application server);

un sistema dedicato alla memorizzazione dei dati (data server);

un sistema dedicato alla autenticazione degli utenti e dei messaggi;

un sistema dedicato a funzioni di Business Intelligence.

In aggiunta a questi sistemi esiste un sistema infrastrutturale trasversale denominato "piattaforma codice univoco nazionale dell'assistito", dedicato alla procedura di cui all'art. 3, che provvede alla generazione ed assegnazione del codice univoco nazionale dell'assistito, che non consente la identificazione diretta dell'interessato, utilizzato per l'interconnessione dei sistemi informativi su base individuale. Le specifiche caratteristiche e modalita' di trattamento che si applicano a tale sistema sono riportate nella sezione 0.

Tutti i succitati sistemi sono collegati in rete locale e connessi alle infrastrutture comunicative attraverso firewall opportunamente configurati. Inoltre, la sicurezza degli stessi e' incrementata mediante:

strumenti IPS/IDS (Intrusion Prevention System/Intrusion Detection System) collocati nei punti di accesso alla rete al fine di consentire l'identificazione di attivita' ostili, ostacolando l'accesso da parte di soggetti non identificati e permettendo una reazione automatica alle intrusioni;

aggiornamenti dei software, secondo la tempistica prevista dalle case produttrici ovvero, periodicamente, a seguito di interventi di manutenzione;

configurazioni delle basi di dati per consentire un ripristino completo delle informazioni senza causarne la perdita di integrita' e disponibilita';

gruppi di continuita' che, in caso di mancanza di alimentazione elettrica di rete, garantiscono la continuita' operativa;

un sistema di gestione degli accessi e di profilazione utenti, che prevede anche, ove opportuno, strumenti di autenticazione forte e certificazione digitale delle postazioni;

un sistema di tracciatura delle operazioni di accesso ai sistemi (sia tramite funzioni applicative o tramite accesso diretto), al fine di permettere l'individuazione di eventuali anomalie.

4.1.1 Gestione dei supporti di memorizzazione

I supporti di memorizzazione, che includono nastri magnetici, dischi ottici e cartucce, possono essere fissi o rimovibili. Sui supporti di memorizzazione non vengono, comunque, conservate informazioni in chiaro; cio' malgrado, per ridurre al minimo il rischio di manomissione delle informazioni, viene identificato un ruolo di custode dei supporti di memorizzazione, al quale e' attribuita la responsabilita' della gestione dei supporti di memorizzazione rimovibili.

Per la gestione dei supporti di memorizzazione sono state adottate, in particolare, le seguenti misure:

tutti i supporti sono etichettati a seconda della classificazione dei dati contenuti;

viene tenuto un inventario dei supporti di memorizzazione secondo controlli predefiniti;

sono state definite ed adottate misure di protezione fisica dei supporti di memorizzazione.

I supporti di memorizzazione non piu' utilizzati saranno distrutti e resi inutilizzabili.

4.1.2 Misure idonee a garantire la continuita' del servizio

A garanzia della corretta operativita' del servizio sono state attivate procedure idonee a definire tempi e modi per salvaguardare l'integrita' e la disponibilita' dei dati e consentire il ripristino del sistema in caso di eventi che lo rendano temporaneamente inutilizzabile.

In particolare, per quel che riguarda i dati custoditi presso il Centro Elaborazione Dati (CED), sono previste:

procedure per il salvataggio periodico dei dati (backup sia incrementale che storico);

procedure che regolamentano la sostituzione, il riutilizzo e la rotazione dei supporti ad ogni ciclo di backup;

procedure per il data recovery;

procedure per la verifica dell'efficacia sia del backup che del possibile, successivo ripristino.

La struttura organizzativa del CED e le procedure adottate consentono, in caso di necessita', di operare il ripristino dei dati in un arco di tempo inferiore ai sette giorni.

4.2 Modalita' di abilitazione degli utenti

Gli utenti accedono ai servizi del NSIS attraverso gli strumenti definiti dalla vigente normativa (art. 64 del Codice dell'amministrazione digitale) per l'autenticazione telematica ai servizi erogati in rete dalle pubbliche amministrazioni.

In fase di prima attuazione, qualora compatibile con la tipologia dei dati trattati, come meglio specificato nei paragrafi che seguono, gli utenti possono accedere al sistema tramite credenziali di autenticazione generate secondo le modalita' riportate sul sito del Ministero, in conformita' all'art. 64 del Codice dell'amministrazione digitale.

Il NSIS dispone di un sistema di gestione delle identita' digitali, attraverso il quale vengono definiti i profili di autorizzazione previsti per ogni sistema, definiti secondo le logiche del Controllo degli accessi basato sui ruoli, declinati nello specifico in relazione al ruolo istituzionale, alle funzioni svolte e all'ambito territoriale delle azioni di competenza. Gli amministratori del sistema, nominati dal Ministero della salute, gestiscono la designazione degli utenti e l'assegnazione dei privilegi di accesso.

Per l'accesso, l'architettura prevede un'abilitazione in due fasi.

4.2.1 Fase A - Abilitazione alla piattaforma NSIS

La prima fase consente la registrazione da parte dell'utente mediante l'inserimento delle generalita' e del proprio indirizzo di posta elettronica ove ricevere le credenziali di autenticazione nonche' dei dettagli inerenti la struttura organizzativa di appartenenza. Successivamente, il sistema di registrazione invia una e-mail contenente l'identificativo e la password che l'utente e' obbligato a cambiare al primo accesso e, periodicamente, con cadenza trimestrale.

La parola chiave dovra' avere le seguenti caratteristiche:

sara' composta da almeno otto caratteri;

non conterra' riferimenti facilmente riconducibili all'incaricato.

Le credenziali di autorizzazione non utilizzate da almeno sei mesi sono disattivate.

4.2.2 Fase B - Abilitazione ai servizi

Nella seconda fase, l'utente (che viene definito utente NSIS) puo' chiedere l'abilitazione ad un profilo di un sistema informativo censito nel NSIS. Il sistema permette di formulare richieste solo per le applicazioni associate alla struttura organizzativa di appartenenza dell'utente.

L'amministratore del sistema effettua un riscontro della presenza del nominativo nella lista di coloro che sono stati formalmente designati dal referente competente (ad es. della regione o provincia autonoma di appartenenza). Qualora questa verifica abbia esito negativo, la procedura di registrazione si interrompe; nel caso in cui questa verifica abbia esito positivo, l'utente e' abilitato all'utilizzo del sistema.

Per garantire l'effettiva necessita', da parte del singolo utente NSIS, di accedere alle informazioni per le quali ha ottenuto un profilo di accesso, le utenze vengono, periodicamente, sottoposte a revisione e l'amministratore verifica, con i referenti competenti, il permanere degli utenti abilitati nelle liste delle persone autorizzate ad accedere all'NSIS e ai sistemi ad esso riconducibili. 4.2.3 Fase B - Regole speciali per l'abilitazione ai servizi che prevedono l'accesso a informazioni riferite ai singoli assistiti

Nel caso il servizio per il quale e' richiesta l'abilitazione, preveda l'accesso a informazioni riferite ai singoli assistiti (art. 4, comma 2) sono previste ulteriori misure specifiche (art. 6, comma 4).

Il processo di autenticazione degli utenti avviene esclusivamente da postazioni identificate e attraverso strumenti di autenticazione forte, in conformita' all'art. 64 del decreto legislativo 7 marzo 2005, n. 82 e successive modificazioni e all'art. 34 del decreto legislativo 30 giugno 2003, n. 196 e successive modificazioni.

L'accesso e' garantito tramite l'utilizzo di un protocollo sicuro.

L'amministratore del sistema effettua uno specifico riscontro della presenza del nominativo nella lista di coloro che sono stati designati, la cui gestione e' a cura del Ministero della salute. (1) Qualora questa verifica abbia esito negativo la procedura di registrazione si interrompe; nel caso in cui questa verifica abbia esito positivo viene confermata all'utente la possibilita' di accedere a tali servizi e gli viene chiesto di indicare la postazione da cui intende accedere al servizio.

La postazione viene censita nell'elenco delle postazioni abilitate e vengono predisposti gli opportuni certificati digitali, emessi da un'autorita' di certificazione ufficiale, da adottare per abilitare l'accesso.

Infine, per rendere piu' sicuro il processo di abilitazione, un altro amministratore del sistema, distinto dall'amministratore che ha generato le credenziali, provvede all'eventuale consegna dello strumento di autenticazione forte (se non gia' in possesso dell'utente che richiede l'abilitazione) e, in ogni caso, alla sua associazione alle suddette credenziali.

In nessun caso i servizi consentono di effettuare piu' accessi contemporanei con le medesime credenziali.

Al collegamento dell'utente al servizio, vengono visualizzati:

una informativa per l'assunzione di responsabilita' circa il trattamento dei dati acceduti;

gli estremi dell'ultima sessione effettuata, indicativa di: data e ora, indirizzo ip/nome macchina da cui e' stata effettuata la precedente connessione, anche al fine di evidenziare eventuali abusi.

Inoltre, ad ulteriore garanzia dell'effettiva titolarita' da parte del singolo utente di accedere alla procedura:

le Unita' organizzative competenti segnalano tempestivamente il venir meno di tale titolarita' per gli utenti;

le utenze vengono, trimestralmente, sottoposte a revisione e l'amministratore verifica con i referenti dell'Unita' organizzativa competente, il permanere degli utenti abilitati, nelle liste delle persone autorizzate.

4.2.4 Abilitazione alla piattaforma codice univoco nazionale assistito

Con riferimento alla piattaforma codice univoco nazionale assistito, di cui al paragrafo 5.3, date le caratteristiche e le finalita' della piattaforma, che prevede esclusivamente procedure automatizzate, gli utenti incaricati al trattamento del dato ricoprono la funzione di amministratori di sistemi applicativi complessi e accedono al sistema esclusivamente per finalita' di gestione e manutenzione.

Pertanto trova integrale applicazione il Provvedimento dell'Autorita' Garante per la protezione dei dati personali in materia di "Misure e accorgimenti prescritti ai titolari dei trattamenti effettuati con strumenti elettronici relativamente alle attribuzioni delle funzioni di amministratore di sistema" del 27 novembre 2008 e successive modificazioni.

Il processo di autenticazione degli utenti avviene esclusivamente attraverso strumenti di autenticazione forte, in conformita' all'art. 64 del decreto legislativo 7 marzo 2005, n. 82 e successive modificazioni e all'art. 34 del decreto legislativo 30 giugno 2003, n. 196 e successive modificazioni. L'accesso e' garantito tramite l'utilizzo di un protocollo sicuro.

L'amministratore della piattaforma codice univoco nazionale assistito effettua uno specifico riscontro della presenza del nominativo utente da abilitare nella lista di coloro che sono stati designati, la cui gestione e' a cura del Ministero della salute.

Qualora questa verifica abbia esito negativo, la procedura di registrazione si interrompe; nel caso in cui questa verifica abbia esito positivo, l'utente e' abilitato all'utilizzo della piattaforma e gli vengono assegnate le credenziali di autenticazione digitali (utenza e password).

Al fine di rendere piu' sicuro il processo di abilitazione, un altro amministratore della piattaforma codice univoco nazionale assistito, distinto dall'amministratore che ha generato le credenziali, provvede all'eventuale consegna dello strumento di autenticazione forte e, in ogni caso, alla sua associazione alle suddette credenziali.

Per quel che riguarda la variazione della password e le caratteristiche che la devono contraddistinguere, si vedano i paragrafi 4.2.1 e 4.2.2.

Inoltre, per garantire l'effettiva titolarita' da parte del singolo utente, di accedere alla piattaforma, le utenze vengono, trimestralmente, sottoposte a revisione e l'amministratore della piattaforma codice univoco nazionale assistito verifica con i referenti del Ministero della salute, il permanere degli utenti abilitati, nelle liste delle persone autorizzabili.

L'abilitazione a questo specifico trattamento e' incompatibile con ogni altro servizio o funzionalita' di amministrazione del NSIS.

Qualora l'utente fosse in precedenza abilitato ad uno o piu' dei suddetti servizi, l'incompatibilita' cessa decorsi sei mesi dalla revoca dell'abilitazione dell'ultimo servizio.

4.3 Sistema di registrazione delle operazioni di trattamento

Nel caso lo specifico servizio preveda il trattamento di dati comprensivi del codice univoco, le operazioni di accesso degli utenti sono registrate e i dati vengono conservati in appositi file di log, al fine di evidenziare eventuali anomalie e/o utilizzi impropri, anche tramite specifici alert.

Le informazioni registrate in tali file di log sono le seguenti: i dati identificativi del soggetto che ha effettuato l'accesso;

la data e l'ora dell'accesso;

l'operazione effettuata.

I predetti file di log sono conservati in modalita' sicura e vengono trattati in forma aggregata, salvo la necessita' di verificare la correttezza e la liceita' delle singole operazioni effettuate. I file di log sono conservati per dodici mesi e cancellati alla scadenza.

4.4 Modalita' di trasmissione dei dati dei sistemi informativi alimentanti il NSIS

I soggetti alimentanti il NSIS forniscono le informazioni secondo le modalita' stabilite nei decreti di istituzione dei singoli sistemi informativi, con le seguenti specifiche ed integrazioni ai tracciati di anagrafica:

utilizzo del codice CUNI di cui all'art. 3, comma 1, lettera b) in luogo del codice univoco assegnato a ciascun soggetto, in applicazione di quanto previsto dai regolamenti per il trattamento dei dati sensibili e giudiziari adottati dalle regioni e province autonome in conformita' alla scheda 12 dell'allegato A dello schema tipo di regolamento volto a disciplinare i trattamenti dei dati sensibili e giudiziari effettuati presso le regioni e le province autonome, le aziende sanitarie, gli enti e agenzie regionali/provinciali, gli enti vigilati dalle regioni e dalle province autonome, ai sensi degli articoli 20 e 21 del decreto legislativo 30 giugno 2003, n. 196;

utilizzo del codice CUNI di cui all'art. 3, comma 1, lettera b) in luogo del codice fiscale previsto dal decreto del Ministro della sanita' 16 luglio 2001, n. 349;

integrazione dell'informazione relativa alla presenza nella banca dati del sistema Tessera Sanitaria del codice identificativo dell'assistito (codice fiscale, STP, ENI, TEAM) corrispondente al codice CUNI (cfr. paragrafo 6, tabella 1, campo A);

integrazione dell'informazione relativa alla tipologia del codice identificativo dell'assistito (codice fiscale, STP, ENI, TEAM) corrispondente al codice CUNI (cfr. paragrafo 6, tabella 1, campo B).

4.5 Garanzie per la sicurezza delle basi dati

I dati dei sistemi informativi su base individuale cui si applica il presente decreto sono archiviati previa separazione dei dati sanitari dagli altri dati ed i dati sanitari sono trattati con tecniche crittografiche. Le tecniche crittografiche applicate sono tali da rendere inintelligibili i dati sanitari ai soggetti preposti alla funzione di amministratore di sistema.

Le procedure di interconnessione vengono applicate ai predetti archivi di norma mediante elaborazioni software. Tuttavia, in funzione delle specifiche esigenze e tipologie di elaborazioni, e' prevista anche la memorizzazione temporanea di porzioni di dati interconnessi in appositi, specifici archivi cui vengono applicate tecniche di cifratura e che sono protetti con idonee misure contro ogni uso improprio o non conforme alle finalita' per cui sono predisposti. Tali archivi vengono cancellati al termine delle analisi che ne hanno richiesto la creazione.

Il NSIS e' inoltre concepito in modo tale da mettere a disposizione basi dati derivate, aggregate o anonime, ottenute attraverso trattamenti eseguiti esclusivamente con modalita' automatizzate dei dati comprensivi del codice univoco al fine di minimizzare l'utilizzo dei dati individuali, comprensivi del codice univoco, ai soli casi di effettiva necessita'.

4.6 Servizi applicativi (reportistica ed analisi)

Nell'ambito del NSIS sono previsti servizi di reportistica e di analisi sui dati dei singoli sistemi informativi e sui dati derivanti dall'interconnessione dei suddetti sistemi. Tali funzionalita' sono riconducibili a tre tipologie distinte, in base ai tipi di dati trattati ed alle tipologie di elaborazioni, e rispondono alle necessita' di trattamento derivanti dal perseguimento delle diverse finalita' di cui al presente decreto:

Funzionalita' di reportistica ed analisi

Descrizione

Finalita' perseguita

1. Servizi basati su dati aggregati o su dati anonimi

Elaborazioni ottenute a partire da basi di dati che sono gia' risultato di processi automatizzati che aggregano o, comunque, rendono il dato disponibile in forma anonima

Tutte le finalita' di cui all'art. 2, comma 1

2. Servizi che richiedono l'utilizzo di dati individuali, con utilizzo del CUNA (di cui all'art. 3 comma 3 del decreto) nelle procedure automatizzate strumentali all'esecuzione delle analisi

Elaborazioni ottenute a partire da basi di dati contenenti dati individuali (codice univoco), tuttavia interrogabili solo attraverso chiavi di ricerca o altre funzioni applicative che non consentono in alcun modo la selezione o l'estrazione di informazioni riferite a singoli individui o codici univoci. In nessun caso e' consentita la consultazione e l'analisi di informazioni che rendano l'interessato identificabile ai sensi del codice di deontologia e di buona condotta a scopi statistici e di ricerca scientifica effettuati nell'ambito del Sistema statistico nazionale, di cui all'allegato A3 del decreto legislativo 30 giugno 2003, n. 196

Le finalita' di cui all'art. 2, comma 1, lettere a) e b)

3. Servizi che accedono a dati individuali, con utilizzo del CUNA (di cui all'art. 3 comma 3 del decreto)

Elaborazioni anche non automatiche ottenute a partire da basi di dati contenenti dati individuali (codice univoco), che prevedono la consultazione, la selezione o l'estrazione di informazioni riferite a singoli individui o codici univoci

Le finalita' di cui all'art. 2, comma 1, lettera a)

5 La procedura di assegnazione del codice univoco nazionale dell'assistito

La procedura di cui all'art. 3 prevede un processo complesso, articolato su piu' fasi eseguite da soggetti diversi, al fine di garantire la massima sicurezza per il trattamento di dati personali e viene dettagliata nel seguito.

5.1 Assegnazione del codice univoco non invertibile ("CUNI") da parte dei soggetti alimentanti il NSIS

Ai sensi delle disposizioni dell'art. 3, comma 1, lettera b), i sistemi informativi dei soggetti alimentanti il NSIS, mediante procedure automatiche eseguite successivamente alla verifica di validita' del codice identificativo di cui alla successiva sezione 6 e preliminarmente alla trasmissione dei dati anagrafici al NSIS, sostituiscono i codici identificativi presenti nei tracciati di origine con i corrispettivi codici univoci prodotti da una funzione non invertibile e resistente alle collisioni. (2) Tale funzione e' rappresentata da un algoritmo di hash (3) che, applicato ad un codice identificativo (dato in input), produce un codice univoco (digest di output) dal quale non e' possibile risalire al codice identificativo di origine. L'algoritmo di hash adottato e' definito dalla DGSISS ed e' condiviso tra tutti i soggetti alimentanti, al fine di rendere il codice univoco non invertibile (CUNI) cosi' ottenuto, a fronte del codice identificativo dell'assistito, unico sul territorio nazionale, anche in caso di mobilita' di questi ultimi (ad es. trattamenti sanitari fuori regione, cambi di residenza, etc.).

5.2 Assegnazione del codice univoco non invertibile (CUNI) da parte del Ministero della salute per il flusso SDO

Ai sensi delle disposizioni dell'art. 8, comma 3, i soggetti alimentanti trasmettono al NSIS il tracciato anagrafico del flusso SDO, contenente, in luogo del codice identificativo, un codice cifrato ottenuto applicando un algoritmo asimmetrico (4) , a chiave pubblica nota, al codice identificativo originario.

Il predetto algoritmo di cifratura di tipo asimmetrico, definito dalla DGSISS e abilitato da chiavi diverse da quelle adottate da ogni altro algoritmo utilizzato nel NSIS, viene reso noto a tutti i soggetti alimentanti il NSIS.

Il Ministero della salute mediante procedure automatiche procede:

alla decifratura del codice cifrato, applicando all'algoritmo asimmetrico la propria chiave privata;

alla verifica di validita' del codice identificativo di cui alla successiva sezione 6;

alla sostituzione dei codici identificativi presenti nei tracciati di origine con i corrispettivi codici univoci (CUNI) prodotti dalla stessa funzione non invertibile e resistente alle collisioni, di cui alla sezione 5.1.

Ai fini di garantire il massimo livello di sicurezza nel trattamento dei dati, le suddette procedure vengono effettuate dal Ministero della salute mediante il dispositivo in alta affidabilita' denominato Hardware Security Module (HSM), descritto piu' diffusamente nella sezione 5.3.

5.3 Assegnazione del codice univoco nazionale dell'assistito (CUNA) Le procedure di cui agli articoli 3, commi 3 e 4 e art. 8, commi 3 e 4, lettera b) sono attuate in modo centralizzato nel NSIS e sono abilitate dall'adozione di una componente infrastrutturale tecnologica denominata "piattaforma codice univoco nazionale assistito" che effettua la generazione ed assegnazione del codice univoco nazionale dell'assistito (CUNA) agli assistiti rappresentati dal codice identificativo non invertibile (CUNI).

Tale operazione avviene contestualmente all'acquisizione dei tracciati dei dati anagrafici contenenti i codici univoci non invertibili (5) , con le seguenti modalita' operative:

il CUNA e' generato mediante l'adozione di una funzione di Hash, rappresentata da un algoritmo (6) definito dalla DGSISS, del codice identificativo non invertibile CUNI ricevuto nei tracciati anagrafici;

il CUNA e' assegnato attraverso la diretta sostituzione del codice identificativo non invertibile CUNI all'interno del tracciato anagrafico di pertinenza con il CUNA;

il CUNA e' utilizzato come unico elemento identificativo dell'assistito nel corso di tutti i successivi trattamenti operati sul NSIS.

La "piattaforma codice univoco nazionale dell'assistito" si avvale per la funzionalita' di cifratura di un dispositivo in alta affidabilita' denominato Hardware Security Module (HSM) e presenta le seguenti caratteristiche:

prevede una gestione esclusivamente automatizzata delle procedure di generazione, assegnazione ed utilizzo del codice univoco;

dispone di algoritmi di hashing e di cifratura simmetrica o asimmetrica volti all'elaborazione del codice univoco a partire dal codice univoco non invertibile ed alla cifratura e decifratura dei codici identificativi per le deroghe concesse;

gestisce esclusivamente in un'area protetta della memoria i dati di input, rimuovendoli dalla stessa una volta applicate le tecniche crittografiche di pertinenza e calcolato pertanto i corrispettivi dati di output. Tale accorgimento preclude la potenziale costruzione di matrici di associazione 'dato di input - dato di output' che consentirebbero di rendere invertibili le elaborazioni eseguite senza conoscere la chiave degli algoritmi;

genera, memorizza e protegge per l'intero ciclo di vita, le chiavi che consentono il calcolo del codice univoco e la cifratura e decifratura dei codici identificativi per le deroghe concesse;

prevede l'autenticazione forte per gli amministratori della piattaforma che accedono al sistema esclusivamente per finalita' di gestione e manutenzione (il sistema di autenticazione e' integrato con il sistema di autenticazione del NSIS) e per gli utenti autorizzati ad accedere direttamente od indirettamente alle funzionalita' di hashing, cifratura e decifratura.

Le operazioni di accesso da parte degli amministratori sono registrate e i dati relativi sono registrati in appositi file di log, al fine di evidenziare eventuali anomalie e/o utilizzi impropri, anche tramite specifici allarmi.

Le informazioni registrate in tali file di log sono le seguenti: i dati identificativi del soggetto che ha effettuato l'accesso;

la data e l'ora dell'accesso;

l'operazione effettuata.

I predetti file di log sono conservati in modo sicuro e trattati in forma aggregata, salvo la necessita' di verificare la correttezza e la liceita' delle singole operazioni effettuate. I file di log sono conservati per dodici mesi e cancellati alla scadenza.

5.4 Procedure per il trattamento dei dati di specifiche coorti di assistiti

Nei casi di cui all'art. 4, comma 3, il Ministero della salute applica le procedure di assegnazione dei codici univoci a elenchi o coorti di assistiti identificati dal codice identificativo (codice fiscale, STP, ENI o TEAM), procedendo alla sostituzione dei predetti codici identificativi con i corrispettivi codici univoci (CUNI) prodotti dalla stessa funzione non invertibile e resistente alle collisioni, di cui alla sezione 5.1, nonche' all'assegnazione del codice univoco nazionale dell'assistito (CUNA), di cui alla sezione 5.3.

Gli elenchi di assistiti cosi' ottenuti sono utilizzati esclusivamente per collegare al medesimo assistito le diverse informazioni sanitarie che lo riguardano. Tali elenchi vengono cancellati al termine delle analisi che ne hanno richiesto la creazione.

6 Procedura di verifica della validita' del codice identificativo

Nelle more dell'attivazione dell'Anagrafe nazionale degli assistiti, istituita ai sensi dell'art. 62-ter del CAD, la procedura di verifica della validita' del codice identificativo, di cui all'art. 3, comma 1, lettera a) prevede uno scambio informativo con il servizio fornito dal sistema Tessera Sanitaria (art. 8, comma 4).

Il servizio viene invocato, preventivamente alla sostituzione del codice identificativo con il codice univoco non invertibile, da:

soggetti alimentanti NSIS, per le procedure di cui all'art. 8, comma 4, lettera a);

Ministero della salute, per le procedure di cui all'art. 8, commi 3 e 4, lettera b).

Tale servizio, a fronte di un codice identificativo in ingresso, restituisce le informazioni inerenti la sua validita' (valido, non valido - in quanto variato - o errato in quanto inesistente nella banca dati del sistema Tessera Sanitaria), utilizzando, limitatamente ai soli campi indicati di seguito, il tracciato definito nel disciplinare tecnico, allegato 1 del decreto 22 luglio 2005 del Ministero dell'economia e delle finanze, di concerto con il Ministero della salute, attuativo del comma 9 dell'art. 50 del decreto-legge 30 settembre 2003, n. 269, convertito, con modificazioni, dalla legge 24 novembre 2003, n. 326, e successive modificazioni, nella sezione "Trasmissione dei dati relativi agli assistiti", come esposto nella tabella "Variazioni anagrafiche trasmesse dal Ministero dell'economia e delle finanze", integrato, a cura del Ministero dell'economia e delle finanze, da due ulteriori campi A e B descritti in tabella:

Progressivo campo

Descrizione campo

Note

6

Codice fiscale attuale

Da intendersi come codice identificativo, ovvero: codice fiscale, STP, ENI o TEAM

9

Sesso

10

Data di nascita

20

Indicatore di soggetto deceduto

21

Data di decesso

A

Validita' del codice identificativo dell'assistito (codice fiscale, STP, ENI, TEAM)

Informazione relativa alla presenza in banca dati del codice di cui si verifica la validita': 0 = Codice identificativo valido (presente in banca dati) 1 = Codice identificativo errato (non presente in banca dati)

B

Tipo di codice identificativo

Informazione relativa alla tipologia del codice identificativo di cui si verifica la validita': 0 = Codice fiscale 1 = Codice STP 2 = Codice ENI 3 = Codice TEAM 99 = Codice non presente in banca dati

Tabella 1 - Informazioni restituite nella procedura di verifica del codice identificativo

Inoltre, ai sensi dell'art. 8, comma 4, lettera b), il sistema Tessera Sanitaria, nelle more dell'attivazione dell'Anagrafe nazionale degli assistiti, istituita ai sensi dell'art. 62-ter del CAD, attiva verso il Ministero della salute un flusso, con periodicita' non superiore al mese, contenente le variazioni di validita' dei codici univoci, secondo il formato esposto nella citata tabella "Variazioni anagrafiche trasmesse dal Ministero dell'economia e delle finanze", valorizzando con dati significativi solamente i seguenti campi:

Progressivo campo

Descrizione campo

Note

1

Tipo variazione

Devono essere inviate tutte le variazioni ad eccezione del tipo = 3, con i corrispondenti tipo variazione

4

Data evento

5

Codice fiscale precedente

Contiene il codice univoco non invertibile (CUNI) corrispondente al codice identificativo precedente (codice fiscale, STP, ENI o TEAM)

6

Codice fiscale attuale

Contiene il codice univoco non invertibile (CUNI) corrispondente al codice identificativo attuale (codice fiscale, STP, ENI o TEAM)

9

Sesso

10

Anno di nascita

20

Indicatore di soggetto deceduto

21

Data di decesso

Tabella 2 - Informazioni nella procedura di inoltro variazioni del codice univoco

Le informazioni cosi' ricevute vengono acquisite nel NSIS e assoggettate alle procedure di cui alla sezione 5.3, al fine di mantenere aggiornate le informazioni in merito alla validita' del codice identificativo, anche in tempi successivi all'acquisizione dei dati dei sistemi informativi di cui all'art. 2, comma 2, lettere b) e c).

Le predette informazioni di cui alle tabelle 1 e 2 sono conservate per il tempo strettamente necessario a completare le operazioni tecniche di verifica della validita' del codice identificativo e di variazione del codice univoco e, al termine delle operazioni, sono cancellate irreversibilmente.

7 Schema logico del Sistema di Integrazione delle Informazioni Sanitarie Individuali

Lo schema seguente rappresenta, in forma semplificata, i flussi dati, i blocchi logico-funzionali e le tipologie di servizi che il NSIS implementa, con riferimento al Sistema di Integrazione delle Informazioni Sanitarie Individuali, evidenziando gli elementi che attuano le disposizioni del presente decreto in materia di interconnessione.

Parte di provvedimento in formato grafico

(1) Si prevede infatti che la gestione della lista di nominativi autorizzati a tali specifici servizi sia accentrata presso il Ministero della salute. Le diverse unita' organizzative del Ministero, di AGENAS e delle regioni comunicheranno al referente del Ministero preposto a tale funzione i nominativi degli incaricati che necessitano dell'accesso a tali servizi.

(2) Per il dominio rappresentato dalla totalita' dei codici identificativi teoricamente possibili.

(3) La funzione di Hash dipendera' da una chiave di lunghezza adeguata alla dimensione e al ciclo di vita dei dati. (Si vedano in proposito le raccomandazioni ENISA contenute nel rapporto "Algorithms, Key Sizes and Parameters Report", October 2013 (https://www.enisa.europa.eu/activities/identity-and-trust/librar y/deliverables/algorithms-key-sizes-and-parameteres-report).

(4) L'algoritmo asimmetrico dipendera' da una coppia di chiavi di lunghezza adeguata alla dimensione e al ciclo di vita dei dati. (Si vedano in proposito le raccomandazioni ENISA contenute nel rapporto "Algorithms, Key Sizes and Parameters Report", October 2013

(https://www.enisa.europa.eu/activities/identity-and-trust/librar y/deliverables/algorithms-key-sizes-and-parameteres-report).

(5) In luogo dei codici identificativi.

(6) La funzione di Hash dipendera' da una chiave di lunghezza adeguata alla dimensione e al ciclo di vita dei dati. (Si vedano in proposito le raccomandazioni ENISA contenute nel rapporto "Algorithms, Key Sizes and Parameters Report", October 2013 (https://www.enisa.europa.eu/activities/identity-and-trust/librar y/deliverables/algorithms-key-sizes-and-parameteres-report).
