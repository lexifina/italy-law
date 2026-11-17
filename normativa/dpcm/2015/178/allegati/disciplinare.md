Allegato

DISCIPLINARE TECNICO

1. Obiettivi del documento.

Il presente disciplinare tecnico definisce:

i dati necessari per la corretta identificazione dell'assistito per l'alimentazione del FSE e i dati amministrativi necessari per la corretta individuazione della posizione amministrativa dell'assistito nei confronti del SSN, in attuazione di quanto indicato nell'articolo 21 (Dati identificativi e amministrativi dell'assistito) del decreto;

le modalita' di accesso al FSE, i profili di accesso in funzione dei ruoli professionali e le modalita' di gestione delle politiche di accesso, in attuazione di quanto indicato negli articoli 22 (Accesso ai soggetti abilitati) e 23 (Misure di sicurezza) del decreto;

i formati standard per la rappresentazione delle informazioni, dei sistemi di codifica dei dati e del loro corretto utilizzo all'interno del Fascicolo Sanitario Elettronico, in attuazione di quanto indicato nell'art. 24 (Sistemi di codifica dei dati) del decreto;

i criteri di interoperabilita' tra le soluzioni di Fascicolo Sanitario Elettronico adottate dalle Regioni o Province Autonome, in attuazione di quanto indicato nell'articolo 25 (Interoperabilita' del FSE) del decreto;

i dati essenziali che compongono il referto di laboratorio, di cui all'articolo 27, comma 1, lettera d), del decreto;

i dati essenziali che compongono il profilo sanitario sintetico, di cui all'articolo 3 del decreto.

2. Definizioni.

Ai fini del presente disciplinare tecnico si intende per:

a) "Codifica dei dati", la rappresentazione, mediante un opportuno insieme di stringhe o di simboli, di un insieme di oggetti materiali o un insieme di informazioni tendenzialmente piu' complesse delle stringhe o dei simboli che vengono usate per rappresentarle;

b) "Sistema di codifica", un sistema che assegna un identificativo univoco (alfabetico, numerico o alfanumerico) a ciascun oggetto di un dato insieme. La codifica puo' avere finalita' di classificazione;

c) "Sistema di classificazione", un sistema che ripartisce gli oggetti dati in classi o raggruppamenti ordinandoli sulla scorta di un principio di ordinamento;

d) "Mapping o mappatura", il collegamento fra i contenuti di una terminologia o sistema di codifica di partenza e quelli di una terminologia o sistema di codifica di destinazione, ai fini dell'interoperabilita' tra i sistemi.

e) "Porta di Dominio", componente architetturale del SPC attraverso il quale si accede al dominio applicativo dell'amministrazione per l'utilizzo dei servizi applicativi;

f) "Asserzione", insieme di dati aggregati in modo strutturato trasferibile per lo scambio di informazioni di sicurezza rilasciato da una autorita' competente, che puo' contenere informazioni che attestino l'identita', gli attributi e le informazioni a supporto della decisione di autorizzazione;

g) "Portafoglio di asserzioni", insieme di asserzioni logicamente correlate;

h) "Credenziali di autenticazione", i dati e i dispositivi in possesso di una persona, da questa conosciuti o ad essa univocamente correlati, utilizzati per l'autenticazione informatica;

i) "Profilo di autorizzazione", l'insieme delle informazioni, univocamente associate a una persona, che consente di individuare a quali dati essa puo' accedere, nonche' i trattamenti ad essa consentiti.

j) "ADT", Accettazione/Dimissione/Trasferimento, l'acronimo si riferisce alle operazioni di gestione dell'assistito all'interno delle strutture sanitarie.

3. Dati identificativi e amministrativi dell'assistito.

Come specificato nelle Linee guida nazionali sul FSE, i dati anagrafici non fanno parte del FSE ma sono gestiti in archivi separati alimentati dalle anagrafi di cui all'articolo 21, comma 1, del decreto.

In particolare i dati necessari per la corretta identificazione dell'assistito in fase di alimentazione del FSE sono i seguenti:

Dati identificativi - Descrizione

Codice Fiscale

Cognome (alla nascita)

Nome

Sesso

Data di Nascita

Comune di Nascita

Provincia di nascita

Indirizzo di Residenza

Indirizzo di Domicilio

Data di Decesso (data di chiusura del fascicolo)

Per quanto riguarda i dati amministrativi necessari per la corretta individuazione della posizione amministrativa dell'assistito nei confronti del SSN sono i seguenti:

Dati amministrativi - Descrizione

ASL Assistenza

Data Inizio del periodo di assistenza presso la ASL

Data scadenza del periodo di assistenza presso la ASL (valorizzata solo se prevista)

Codice Fiscale Medico

Cognome Medico

Nome Medico

Data Inizio periodo di assistenza presso il medico

Data Fine periodo di assistenza presso il medico (valorizzata solo se prevista)

Tipo Assistenza (generici / pediatri, altro)

Recapiti medico (indirizzo, telefono, etc.)

Esenzioni per patologia e relative eventuali scadenze

4. Gestione degli accessi.

La gestione degli accessi alle informazioni presenti nel FSE, richiede l'individuazione di adeguati livelli di visibilita' per ciascuna categoria di professionisti ed operatori sanitari. Tali livelli possono essere espressi definendo in dettaglio l'insieme dei profili da associare ai ruoli dei soggetti che si prevede possano accedere al sistema di FSE (per esempio medico di medicina generale, farmacista, assistito, etc.).

L'attivita' di profilazione deve essere effettuata da un sistema di gestione dei privilegi di natura modulare che, basandosi su una preventiva classificazione delle informazioni presenti nel FSE, attribuisca al soggetto autorizzazioni e diritti di accesso adatti.

Tale sistema di gestione dei privilegi puo' prevedere a livello regionale, in correlazione ai ruoli, l'abbinamento con i contesti applicativi di esercizio del ruolo (es. emergenza, continuita' assistenziale, etc.) tali da garantire un livello maggiormente specifico di accesso ai dati.

Ciascuna Regione e Provincia Autonoma puo' specificare profili piu' specifici rispetto a quelli indicati nel presente disciplinare, tuttavia e' essenziale che, in caso di comunicazione con i sistemi di altre Regioni o Province Autonome, un soggetto venga associato a un profilo di accesso univocamente definito a livello nazionale, attraverso tecniche di mappatura.

L'operazione di profilazione deve essere effettuata preventivamente all'accesso alle funzionalita' del FSE, in modo tale da rendere disponibili tali funzionalita' a chine abbia il diritto, derivante dal ruolo ricoperto.

I soggetti che accedono al FSE sono tenuti ad utilizzare idonee modalita' di accesso al FSE per essere autenticati dal sistema.

Infine, la verifica dei diritti di autorizzazione per l'accesso a specifiche informazioni presenti nel FSE deve essere svolta analizzando politiche di accesso opportunamente predefinite che tengano conto anche del consenso indicato dal paziente.

4.1. Modalita' di accesso al FSE.

L'accesso al FSE prevede le seguenti fasi sequenziali:

1. preliminare registrazione del soggetto, che comprende l'identificazione personale e i contesti operativi;

2. attribuzione delle credenziali e profilazione;

3. autenticazione del soggetto nel FSE, attraverso le modalita' di accesso definite.

Una volta completati i passi 1 e 2 il soggetto puo' accedere al FSE. Gli impatti derivanti da eventuali variazioni dei contesti operativi e di ruolo del soggetto vengono gestite attraverso procedure di modifica dei dati definiti nei passi 1 e 2.

Un soggetto che intende accedere alle informazioni disponibili nel FSE deve in primo luogo essere registrato a sistema. Questa operazione richiede l'individuazione della identita' del soggetto e di ulteriori attributi (quali ad esempio il suo ruolo, l'organizzazione a cui afferisce, ecc.). A valle di tale processo, il soggetto riceve le credenziali di accesso e, preliminarmente a ogni altra azione, deve essere associato ad uno specifico profilo di accesso.

La fase di autenticazione, e quindi della determinazione dell'identita', del ruolo e degli attributi integrativi del soggetto, deve essere svolta nella Regione o Provincia Autonoma di appartenenza di quest'ultimo, adoperando esclusivamente le modalita' di accesso e gli strumenti di cui all'articolo 64 del CAD.

4.2. Profili di accesso.

Di seguito sono elencate le classi di dati, necessarie alla definizione dei livelli di accesso per i soggetti abilitati:

Dati anagrafici: corrispondono ai dati personali che identificano l'assistito.

Dati amministrativi: riguardano eventuali esenzioni e i dati che identificano il medico di base.

Dati prescrittivi: sono i dati relativi alla prescrizioni mediche.

Dati clinici: corrispondono alle informazioni cliniche presenti in documenti riguardanti l'assistito, ivi incluse, a mero titolo esemplificativo, le informazioni relative a diagnosi, terapie, interventi, accessi, servizi, procedure, od ogni altro evento clinico di interesse, nonche' i piani di cura riabilitativi o terapeutici.

Dati di consenso: sono le informazioni che regolano l'accesso ai dati sulla base del consenso reso dal cittadino.

Laddove il documento che afferisce al FSE non e' in formato strutturato, non e' possibile trattare in modo indipendente i dati in esso contenuti. Ne consegue che le politiche di accesso saranno applicate all'intero documento a seconda della tipologia del documento stesso.

Le disposizioni relative all'oscuramento dei dati e dei documenti sanitari e socio-sanitari, di cui all'articolo 8, sono soddisfatte attraverso la messa a disposizione di funzionalita' che permettano l'oscuramento dei dati di cui l'assistito richiede l'oscuramento o dell'intero documento che contiene i predetti dati.

Con riferimento alle finalita' di governo, di cui all'articolo 20, comma 2, del decreto, si rimanda alle disposizioni attuative dell'articolo 15, comma 25-bis, del decreto-legge 6 luglio 2012, n. 95, convertito, con modificazioni, dalla legge 7 agosto 2012, n. 135, per quanto concerne le specifiche disposizioni atte a garantire la tutela dei dati personali durante il trattamento dei dati.

I profili di accesso alle informazioni disponibili nel FSE sono definiti in funzione del ruolo che ciascun soggetto assume. Tali ruoli, in sede di prima applicazione, sono elencati di seguito:

Farmacista: operatore sanitario della farmacia abilitato alla professione.

Operatore Amministrativo: persona che opera presso le strutture del sistema sanitario e socio-sanitario (es. AO, ASL, MMG) con mansioni amministrative.

Direttore Sanitario: medico che svolge attivita' direttive all'interno di una Direzione Sanitaria delle strutture del sistema sanitario e socio-sanitario.

Medico di Medicina Generale / Pediatra di Libera Scelta: medico convenzionato con la ASL per svolgere attivita' di MMG/PLS.

Direttore Amministrativo: persona che svolge attivita' direttive all'interno della Direzione Amministrativa di strutture del sistema sanitario e socio-sanitario.

Medico ed altri dirigenti sanitari (biologo, psicologo, chimico, fisico): professionisti che operanonell'ambito dei servizi sanitari delle strutture del sistema sanitario e socio-sanitario.

Medico RSA: medico che opera presso una struttura che eroga assistenza di tipo residenziale.

Infermiere o altro Professionista Sanitario: professionista sanitario che opera nell'ambito delle strutture del sistema sanitario e socio-sanitario.

Medico Rete di Patologia: medico che opera nel contesto di una rete di patologia.

Professionista del sociale: professionista che svolge la sua attivita' sia nel settore sociale che in quello sanitario, in servizi di tipo socio-assistenziale e socio-sanitario, residenziali o semiresidenziali, in ambiente ospedaliero e al domicilio dell'utente.

Assistito: cittadino che usufruisce di servizi sanitari e socio-sanitari.

La matrice presentata di seguito indica le operazioni di accesso alle diverse classi di dati, in termini di lettura e scrittura, da parte dei soggetti abilitati sulla base del ruolo assunto. Con particolare riferimento all'operazione di scrittura, i soggetti che concorrono all'alimentazione del FSE sono specificati all'articolo 12 del decreto. Eventuali variazioni e aggiornamenti dei ruoli e delle operazioni di accesso alle diverse classi di dati, rispetto a quanto specificato nel presente Disciplinare, saranno disciplinati con successivi decreti, da adottarsi ai sensi dell'articolo 12, comma 7, del decreto-legge 18 ottobre 2012, n. 179, convertito dalla legge 17 dicembre 2012, n. 221, e successive modificazioni.

Parte di provvedimento in formato grafico

In aggiunta, l'assistito puo' inserire nel proprio taccuino personale dati, documenti ed informazioni personali e relative ai propri percorsi di cura, cosi' come specificato all'articolo 4 del decreto. E' altresi' opportuno prevedere un meccanismo efficiente che consenta all'assistito di esprimere o aggiornare i criteri di accesso puntuali ad ogni informazione clinica presente nel FSE.

L'accesso al FSE, da parte di un operatore abilitato, deve essere subordinato alle operazioni di ADT dello specifico assistito, per la durata della presa in carico, di cui si chiede la consultazione del FSE; ove non possibile applicare la precedente prescrizione e nei casi di accesso in emergenza, la consultazione del FSE deve essere subordinata ad un'autocertificazione telematica da parte dell'operatore, con compilazione del motivo codificato per il quale l'operatore medesimo richiede la consultazione.

4.3. Gestione delle politiche di accesso.

A valle della fase di autenticazione, il soggetto viene identificato ed associato ad un profilo di accesso, al quale sono assegnati specifici privilegi di accesso a categorie di dati coerentemente con le classificazioni descritte nel paragrafo 4.2. In tal modo, nella successiva fase di autorizzazione, e' possibile verificare che il soggetto acceda solo alle informazioni di sua competenza. Il processo di autorizzazione deve essere effettuato nella Regione o Provincia Autonoma che detiene le informazioni di autorizzazione e, in particolare, consiste nel valutare se:

1. il soggetto che intende accedere alle informazioni possiede un profilo autorizzato dall'assistito;

2. l'identita' e gli attributi relativi ad un soggetto soddisfano le politiche di accesso locali.

Con riferimento alle politiche di accesso, ciascuna Regione o Provincia Autonoma puo' definire proprie politiche, le quali devono essere federate con i gestori dei privilegi degli altri sistemi di FSE, attraverso operazioni di mappatura dei profili di accesso.

Al fine di garantire la tracciabilita' delle operazioni svolte sul sistema e di chi le ha eseguite, in modo da abilitare funzionalita' di auditing e di certificazione sulle attivita' svolte per le diverse finalita' previste, devono essere registrate tutte le operazioni, sia quelle andate a buon fine che quelle annullate.

5. Sistemi di codifica dei dati.

Ai sensi delle disposizioni dell'articolo 24 del decreto, ciascuna Regione e Provincia Autonoma ha il compito di redigere i documenti sanitari e socio-sanitari utilizzando i sistemi di codifica definiti nel presente decreto per rappresentare, comunicare ed interpretare le informazioni scambiate tra i diversi FSE regionali, assicurando in tal modo l'interoperabilita' semantica. Per quanto concerne le strutture informative complesse che costituiscono il nucleo minimo del FSE si adotta lo standard HL7 (Health Level 7) per descrivere le definizioni dei dati da scambiare in termini di messaggi e documenti costituenti il FSE, e in particolare e' prescritto l'utilizzo del CDA (Clinical Document Architecture) release 2 (ISO/HL7 27932:2009). I sistemi di codifica adottati per i documenti di cui all'articolo 27, comma 1, lettere d), e), del decreto sono:

ICD 9-CM (International Classification of Diseases 9th revision - Clinical Modification);

LOINC® (Logical Observation Identifiers Names and Codes);

AIC (Autorizzazione all'immissione in commercio di un farmaco);

ATC (Classificazione Anatomica Terapeutica Chimica).

Allo scopo di favorire il corretto interscambio dei dati, gli stessi dovranno, inoltre, essere trasmessi secondo le modalita' indicate nell'articolo 25 del decreto e nel presente disciplinare tecnico.

Le procedure necessarie ad implementare i suddetti sistemi di codifica, sia in termini di formazione all'utilizzo da parte del personale che di predisposizione dei sistemi informativi, devono essere espletate dalle Regioni e dalle Province Autonome, secondo le forme e le modalita' ritenute piu' idonee.

5.1. ICD-9-CM.

La International Classification of Diseases (ICD) e' un sistema di classificazione internazionale che organizza le malattie ed i traumatismi in gruppi sulla base di criteri definiti.

L'Organizzazione Mondiale della Sanita' (OMS) si occupa dello sviluppo e della diffusione della classificazione. La traduzione italiana, inizialmente curata dall'ISTAT, e' dal 2010 demandata al Centro Collaboratore italiano dell'Organizzazione Mondiale della Sanita' per la Famiglia delle Classificazioni Internazionali.

La classificazione ICD-9-CM adottata per i documenti del FSE e' la versione 2007 in lingua italiana.

5.2. LOINC.

LOINC e' un sistema di nomi e codici universali che identificano in maniera univoca osservazioni cliniche e di laboratorio al fine di facilitare la condivisione e lo scambio di risultati di indagini diagnostiche fra sistemi elettronici di strutture sanitarie differenti. Il Regenstrief Institute si occupa dell'aggiornamento dello standard terminologico con release semestrali.

La classificazione LOINC adottata per i documenti del FSE e' la versione 2.3.4 in lingua italiana.

5.3. AIC.

Nessun medicinale puo' essere immesso in commercio sul territorio nazionale senza aver ottenuto un'autorizzazione dell'AIFA o un'autorizzazione comunitaria a norma del regolamento (CE) n. 726/2004 in combinato disposto con il regolamento (CE) n. 1394/2007.

Le attivita' connesse all'autorizzazione all'immissione in commercio di farmaci con procedura nazionale, sono finalizzate ad assicurare l'assistenza farmaceutica su tutto il territorio nazionale, l'accesso ai farmaci innovativi e per le malattie rare.

Attualmente, in Italia, per l'autorizzazione all'immissione in commercio dei medicinali e' prevista, oltre alla modalita' di registrazione nazionale, quella comunitaria. Quest'ultima prevede l'autorizzazione all'immissione in commercio dei medicinali secondo procedure che coinvolgono tutti i Paesi membri dell'Unione europea (procedura centralizzata) o parte di essi (procedura di mutuo riconoscimento e decentrata).

5.4. ATC.

Il sistema di classificazione ATC prevede che i farmaci siano suddivisi in gruppi sulla base degli organi o apparati su cui agiscono e delle loro proprieta' chimiche, farmacologiche e terapeutiche. La classificazione e' articolata in cinque livelli gerarchici. Al primo livello, i farmaci sono divisi in quattordici gruppi anatomici principali e, all'interno di questi, in gruppi terapeutici principali (II livello). I livelli III e IV sono sottogruppi chimici/farmacologici/terapeutici, mentre al V e ultimo livello sono classificati i singoli principi attivi.

Le prestazioni farmaceutiche aventi ad oggetto le formulazioni magistrali, le formule officinali, nonche' i medicinali esteri non autorizzati all'immissione in commercio in Italia ed utilizzati ai sensi del decreto del Ministro della salute 11 febbraio 1997, vengono individuati attraverso il codice ATC al maggior livello di dettaglio possibile.

6. Criteri di interoperabilita'.

6.1. Modello di riferimento.

Ciascuna Regione o Provincia Autonoma ha il compito di rendere disponibili i documenti sanitari e socio-sanitari conservati nella propria infrastruttura di FSE, previo consenso del cittadino, alle persone autorizzate appartenenti anche a domini differenti che ne fanno richiesta.

Allo scopo di favorirne la ricerca, la localizzazione e la selezione dei documenti del FSE, devono inoltre essere resi disponibili specifici metadati che descrivono i documenti stessi.

Le richieste per la ricerca ed il recupero dei documenti, cosi' come quelle per la comunicazione dei metadati di indicizzazione dei documenti del FSE prodotti per gli assistiti provenienti da altre Regioni o Province Autonome, devono essere espletate da specifici servizi esposti da queste ultime. Il trasferimento dei dati deve avvenire mediante protocolli di comunicazione sicuri basati sull'utilizzo di standard crittografici. Le interfacce dei servizi, indicate nel paragrafo 6.3, devono essere esposte tramite Porta di Dominio nel rispetto delle regole tecniche del Sistema Pubblico di Connettivita' (SPC).

Le richieste provenienti da domini differenti devono essere soddisfatte solo dopo aver verificato i diritti di accesso ai servizi ed il consenso del cittadino. A tal proposito, le richieste devono contenere un portafoglio di asserzioni digitalmente firmate attestanti specifici attributi, in maniera conforme al modello di sicurezza illustrato nel paragrafo 6.4.

6.2. Contenuti informativi minimi dei documenti al fine di garantire l'interoperabilita'.

I documenti contenuti nel FSE devono contenere almeno le seguenti informazioni:

Tipologia del documento: e' un codice derivato dal sistema di classificazione LOINC che rappresenta il tipo di documento descritto (ad es. referto, lettera di dimissione, profilo sanitario sintetico).

Identificativo del paziente: rappresenta il codice univoco del paziente a cui il documento fa riferimento.

Data del documento: rappresenta la data di creazione del documento.

Stato del documento: indica lo stato corrente del documento.

Identificativo della Regione o Provincia Autonoma: e' rappresentato dal codice a tre caratteri definito con DM 17 settembre 1986, pubblicato nella Gazzetta Ufficiale n.240 del 15 ottobre 1986, e successive modificazioni, utilizzato anche nei modelli per le rilevazioni delle attivita' gestionali ed economiche delle Aziende unita' sanitarie locali, che identifica, univocamente su base nazionale, la Regione o Provincia Autonoma responsabile del documento.

Identificativo della struttura sanitaria: e' rappresentato dal codice delle strutture sanitarie, di cui al decreto del Ministro della sanita' 23 dicembre 1996, pubblicato nella Gazzetta Ufficiale n. 22 del 28 gennaio 1997 e successive modificazioni, riguardante modelli di rilevazione dei flussi informativi sulle attivita' gestionali ed economiche delle aziende sanitarie locali e delle aziende ospedaliere (modelli HSP.11 e HSP.11bis, STS.11 e RIA.11) che identifica, univocamente su base nazionale, la struttura sanitaria responsabile del documento.

Identificativo del documento: corrisponde ad un codice locale che identifica il documento.

Tali informazioni devono essere codificate adottando un modello condiviso.

6.3. Interfacce dei servizi.

La soluzione di FSE adottata da ciascuna Regione o Provincia Autonoma deve esporre i seguenti servizi:

servizio per la ricerca dei documenti del FSE disponibili nel proprio dominio;

servizio per il recupero di uno specifico documento del FSE;

servizio per la comunicazione dei metadati di indicizzazione dei documenti del FSE prodotti per gli assistiti provenienti da altre Regioni o Province Autonome.

6.3.1. Servizio per la ricerca dei documenti.

Il servizio per la ricerca dei documenti del FSE, la cui interfaccia e' illustrata in Tabella 1, deve essere in grado di ricevere una richiesta contenente un nucleo di parametri che rappresentano i criteri di ricerca specificati. La richiesta deve altresi' contenere un portafoglio di asserzioni per la verifica dei diritti di accesso al servizio, cosi' come specificato nel paragrafo 6.4.

Il servizio deve restituire l'elenco dei documenti corrispondenti ai criteri di ricerca, ove esistenti, congiuntamente ad opportune asserzioni di autorizzazione per il recupero dei documenti stessi.

Parte di provvedimento in formato grafico

6.3.2. Servizio per il recupero di un documento.

Il servizio per il recupero di un documento del FSE, la cui interfaccia e' mostrata in Tabella 2, deve essere invocato dopo aver ottenuto dal servizio per la ricerca dei documenti, di cui al paragrafo 6.3.1, i riferimenti necessari per localizzazione dello stesso (quali gli identificativi della Regione o Provincia Autonoma e della struttura sanitaria in cui il documento e' memorizzato e l'identificativo del documento) e la corrispondente asserzione di autorizzazione.

Il servizio per il recupero di un documento deve essere pertanto in grado di ricevere una richiesta contenente i riferimenti necessari alla localizzazione del documento e l'asserzione di autorizzazione, cosi' come specificato nel paragrafo 6.4.

Il servizio deve restituire il documento richiesto.

Parte di provvedimento in formato grafico

6.3.3. Servizio per la comunicazione dei metadati.

Il servizio per la comunicazione dei dati di indicizzazione dei documenti del FSE, la cui interfaccia e' mostrata in Tabella 3, consente ad un'altra regione o provincia autonoma di comunicare alla Regione titolare del FSE l'elenco dei dati che descrivono i documenti in essa prodotti. Il servizio deve restituire una risposta contenente l'esito della richiesta.

Parte di provvedimento in formato grafico

6.4. Modello di sicurezza.

Il modello di sicurezza prevede le fasi di autenticazione ed autorizzazione dell'utente. La fase di autenticazione deve essere svolta nella Regione o Provincia Autonoma fruitrice del servizio, mentre la fase di autorizzazione deve essere realizzata nella Regione o Provincia Autonoma che eroga il servizio richiesto.

Per quanto riguarda i servizi per la ricerca dei documenti e per la comunicazione dei metadati, un utente che intende inviare una richiesta deve autenticarsi adoperando le proprie credenziali di autenticazione e gli strumenti offerti dalla Regione o Provincia Autonoma a cui appartiene. A valle della fase di autenticazione, devono essere prodotte opportune asserzioni digitalmente firmate, che attestano l'identita', il ruolo e l'ente a cui l'utente afferisce.

Ciascuna Regione o Provincia Autonoma deve quindi fungere da garante dell'identita' e degli attributi del proprio utente. Le asserzioni summenzionate devono essere allegate alle richieste di accesso ai servizi, congiuntamente ad un'ulteriore asserzione prodotta e firmata dall'utente contenente una serie di attributi contestuali, quali ad esempio l'indicazione del tipo di trattamento (ordinario o in emergenza) o il tipo di documento in esame.

Gli attributi contenuti nelle asserzioni ricevute, con particolare riferimento al ruolo dell'utente, devono essere analizzati dai servizi esposti per la fase di autorizzazione, che consiste nel verificare se il profilo di autorizzazione dell'utente fornisce a quest'ultimo il diritto di accesso al servizio richiesto.

In particolare, l'accesso al servizio deve essere concesso all'utente se sono soddisfatte le seguenti condizioni:

il cittadino ha espresso esplicito consenso all'accesso alle proprie informazioni;

la richiesta soddisfa le specifiche politiche locali.

Dopo aver verificato che l'utente possiede i diritti di accesso e soddisfatto la richiesta, il servizio per la ricerca dei documenti deve restituire un'opportuna asserzione di autorizzazione, la quale deve contenere specifici attributi, quali l'identita' ed il ruolo dell'utente.

Per quanto concerne il servizio per il recupero di un documento, la richiesta deve contenere l'asserzione di autorizzazione rilasciata dal servizio per la ricerca dei documenti. L'accesso a questo servizio deve essere concesso se la richiesta soddisfa le politiche locali.

7. Contenuti del profilo sanitario sintetico.

Ai sensi dell'articolo 3, comma 1, del decreto, il profilo sanitario sintetico e' il documento socio sanitario informatico redatto e aggiornato dal medico di medicina generale/pediatra di libera scelta, che riassume la storia clinica del paziente e la sua situazione corrente conosciuta.

I contenuti informativi minimi del profilo sanitario sintetico sono descritti nella Tabella 4 che segue.

Note:

l'indicazione che l'informazione e' gestita come "testo libero" si applica esclusivamente nei casi in cui nella regione o provincia autonoma non siano vigenti disposizioni che disciplinano per le medesime informazioni l'utilizzo di codifiche e/o classificazioni: in tali casi le informazioni devono essere redatte in forma codificata, coerentemente con le disposizioni regionali;

nei casi in cui l'informazione sia obbligatoria ma non applicabile o pertinente per lo specifico soggetto (es. nessuna patologia, non appartenenza a reti di patologia, nessuna allergia nota riferita dall'assistito, etc.), deve essere comunque esplicitamente registrata tale condizione, che nel caso di informazioni codificate assume un valore convenzionale definito ad hoc (es. nessuno/a, non riferito/non riferita);

per "fonte di riferimento" si intende la fonte da cui l'informazione viene tratta, intesa sia come sistema informativo (Anagrafe assistiti) che come informazione inserita dal medico di medicina generale/pediatra di libera scelta.

Parte di provvedimento in formato grafico

8. Contenuti del referto di laboratorio.

Ai sensi dell'articolo 27, comma 1, lettera d), del decreto, il referto di laboratorio e' il documento redatto dal medico di medicina di laboratorio.

I contenuti informativi del referto di laboratorio sono descritti nella Tabella 5 che segue.

Note:

per "fonte di riferimento" si intende la fonte da cui l'informazione viene fornita, intesa sia come sistema informativo (Anagrafe assistiti) che come informazione inserita dal medico di medicina di laboratorio.

Parte di provvedimento in formato grafico

(1) ((2))

---------------

AGGIORNAMENTO (1)

Il Decreto 18 maggio 2022 (in G.U. 11/07/2022, n. 160) ha disposto (con l'art. 2, commi 2 e 3) che in luogo dei paragrafi 7 e 8 del presente disciplinare tecnico trovano applicazione i paragrafi 7 e 8 di cui al medesimo Decreto 18 maggio 2022.

Ha inoltre disposto (con l'art. 2, comma 4) che in aggiunta alle previsioni del presente disciplinare tecnico trovano altresi' applicazione i paragrafi 9, 10, 11, 12, 13, 14, 15, 16 e 17 del medesimo Decreto 18 maggio 2022.

--------------

AGGIORNAMENTO (2)

Il Decreto 7 settembre 2023 (in G.U. 24/10/2023, n. 249), ha disposto (con l'art. 27, comma 5) che "Il decreto del Presidente del Consiglio dei ministri 29 settembre 2015, n. 178, pubblicato nella Gazzetta Ufficiale della Repubblica italiana 11 novembre 2015, n. 263, cessa di avere efficacia dal giorno dell'entrata in vigore del presente decreto, ad eccezione dei Capi III e IV, che rimangono in vigore fino all'adozione, con successivi decreti ai sensi del comma 7 dell'art. 12 del decreto-legge 18 ottobre 2012, n. 179, convertito, con modificazioni, dalla legge 17 dicembre 2012, n. 221, e successive modificazioni, di specifiche disposizioni per i trattamenti dei dati e dei documenti del FSE per le finalita' di ricerca e di Governo".
