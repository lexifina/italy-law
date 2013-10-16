Allegato

1. SCOPO DEL DOCUMENTO

Questo documento definisce le fasi progettuali con cui sara' istituita l'Anagrafe Nazionale della Popolazione Residente, base dati di interesse nazionale istituita dal decreto-legge 18 ottobre 2012, n. 179, convertito dalla legge 17 dicembre 2012, n. 221, che subentra all'INA, all'AIRE e, gradualmente, alle anagrafi della popolazione residente e dei cittadini italiani residenti all'estero tenute dai comuni, sulla base di un apposito piano da completarsi entro il 31 dicembre 2014.

Il documento descrive in particolare la soluzione relativa alle modalita' di scambio dei dati tra le anagrafi comunali e l'Anagrafe Nazionale della Popolazione Residente e tra quest'ultima e gli enti centrali della Pubblica Amministrazione interessati alla notifica delle informazioni anagrafiche.

Tale soluzione garantisce:

- l'integrita' e la riservatezza dei dati scambiati;

- la sicurezza dell'accesso ai servizi;

- il tracciamento delle operazioni effettuate.

Viene inoltre descritta la soluzione necessaria per gestire la fase transitoria fino alla realizzazione della soluzione definitiva.

2. GLOSSARIO

ANPR: Anagrafe Nazionale della Popolazione Residente

CNSD: Centro Nazionale per i Servizi Demografici

SOAP: Simple Object Access Protocol

SPC: Sistema Pubblico di Connettivita'

SSL: Secure Socket Layer

HTTPS: HyperText Transfer Protocol over Secure Socket Layer

WS-Security: Web Service Security

3. PREMESSA

Il CNSD costituito con decreto del Ministro dell'interno del 23 aprile 2002 presso la Direzione Centrale per i Servizi Demografici, e' un'infrastruttura tecnologica alla quale e' affidata la gestione unitaria delle infrastrutture informatiche che fanno capo alla stessa Direzione centrale.

Al predetto Centro sono affidate, in particolare, tutte le funzioni connesse alla gestione, all'aggiornamento e alla consultazione dell'ANPR.

Il progetto per la realizzazione dell'ANPR si articola in tre fasi, di cui le prime due sono necessarie per gestire il periodo transitorio che precede la completa implementazione della soluzione definitiva.

fase 1 - e' la fase di attuazione immediata che prevede esclusivamente la modifica dei sistemi di sicurezza mentre restano invariate le modalita' di accesso e di trasmissione dei dati;

fase 2 - e' la fase transitoria che prevede la progressiva migrazione delle banche dati relative alle anagrafi comunali della popolazione residente e dei cittadini italiani residenti all'estero nell'ANPR. In questa fase e' resa disponibile anche la nuova banca dati dell'ANPR contestualmente ai servizi resi dall'INA e dall'AIRE. fase 3 - e' la fase definitiva che decorre dal 1° gennaio 2015 in cui l'ANPR subentra alle anagrafi comunali.

Nel seguito del documento viene fornita una descrizione piu' dettagliata delle tre fasi suddette.

4. INFRASTRUTTURA TECNOLOGICA DELLA SOLUZIONE

L'infrastruttura e le misure di sicurezza descritte in questo paragrafo si riferiscono alla fase 3 cioe' alla soluzione definitiva sopraindicata, ad eccezione del paragrafo 4.6, descrittivo delle fasi transitorie.

4.1 CNSD

Dal punto di vista dell'architettura logica del sistema, l'infrastruttura del CNSD e' composta da:

1. sistema di servizi, realizzati tramite Web Services, per l'interoperabilita' con gli enti della Pubblica Amministrazione o degli organismi che erogano pubblici servizi interessati alla notifica delle variazioni anagrafiche, secondo le regole tecniche dell'SPC o esposti su Internet laddove non sia presente SPC;

2. sistema di servizi fruibili tramite Web Services o attraverso un'applicazione web. Tali servizi, esposti su Internet e/o su SPC, sono utilizzati dalle postazioni comunali per tutte le operazioni inerenti l'elaborazione delle informazioni anagrafiche di interesse;

3. banca dati ANPR;

4. banca dati delle utenze/profili associati;

5. banca dati delle postazioni;

6. banca dati dei dati di tracciamento delle operazioni;

7. Certification Authority utilizzata per l'emissione dei certificati.

4.2 Comuni

I comuni, sono dotati di apposite postazioni provviste di una connessione a SPC o, se questa non disponibile, ad Internet.

Ogni postazione e' dotata di:

1. lettore di smart-card necessario per l'identificazione certa dell'operatore e relativo certificato;

2. un certificato interno necessario per l'identificazione della postazione da cui viene effettuato l'accesso.

4.3 Altre Pubbliche Amministrazioni

Per accedere ai servizi resi disponibili dall'ANPR, le Pubbliche Amministrazioni o gli organismi che erogano pubblici servizi stipulano con il Ministero dell'interno apposite convenzioni ai sensi dell'art. 58, comma 2, del decreto legislativo n. 82/2005, nonche' specifici accordi di servizio.

4.4 Il sistema di accesso ai servizi e di scambio dati

L'amministrazione comunale usufruisce dei servizi di cui al punto 2 del paragrafo 4.1, utilizzando un software, che rispetti le specifiche tecniche fornite dal CNSD, connesso con i Web Services, messi a disposizione dal CNSD, oppure un'applicazione web fornita dallo stesso CNSD.

L'accesso ai servizi e' garantito dall'«autenticazione forte» dell'utente tramite l'uso di una smart-card che contiene il certificato di autenticazione dell'operatore autorizzato e dall'identificazione della postazione tramite il certificato memorizzato al suo interno; entrambi i certificati sono emessi dalla Certification Authority di cui al punto 7 del paragrafo 4.1.

L'identificazione e l'autorizzazione dell'operatore e della postazione viene effettuata mediante un servizio, esposto centralmente sull'ANPR, che controlla la validita' dei certificati e il profilo autorizzativo.

Le utenze e le postazioni sono censite all'interno di due database centrali, di cui ai punti 4 e 5 del paragrafo 4.1, corredati di opportuni strumenti per il loro popolamento.

Le informazioni scambiate viaggiano in modalita' sicura su rete di comunicazione SPC ovvero, se questa non disponibile, tramite Internet, in ogni caso mediante protocollo HTTPS per garantire la riservatezza del dato.

Per quanto riguarda il colloquio con gli enti della Pubblica Amministrazione interessati alla notifica delle variazioni anagrafiche, e' previsto un insieme di servizi che utilizzano SPC come rete di comunicazione o Internet laddove non presente SPC.

4.5 Misure di sicurezza

L'architettura sopradescritta consente l'esatta associazione tra la postazione, l'utente e i dati acceduti. Tali informazioni sono tracciate e conservate, includendo i riferimenti temporali e i soggetti i cui dati sono stati trattati. Tutte le informazioni relative al tracciamento dei dati sono accessibili solo dagli incaricati autorizzati su specifica richiesta da parte degli organi competenti.

Per il colloquio tra i comuni e il CNSD si adottano i meccanismi tipici dell'interoperabilita' quali i Web Services, il protocollo SOAP e la WS-Security. Quest'ultima garantisce l'applicazione delle policy di sicurezza previste per l'interscambio dati.

Il protocollo di comunicazione adottato e' SSL che garantisce la riservatezza dei dati su reti pubbliche.

L'identiticazione dell'utente e della postazione avviene attraverso due certificati distinti, il primo residente sulla smart-card, della cui gestione e conservazione e' responsabile l'operatore assegnatario, l'altro certificato memorizzato internamente alla postazione, della cui gestione e conservazione e' responsabile l'amministratore dei sistemi informativi comunali.

4.6 Fasi transitorie

Nelle more della completa implementazione della soluzione definitiva, sono previste due fasi transitorie gia' enunciate in premessa.

4.6.1 - Fase 1

In questa fase l'ANPR garantisce i servizi resi dall'INA e dall'AIRE (ai sensi dell'art. 2 del decreto-legge 18 ottobre 2012, n. 179, convertito dalla legge 17 dicembre 2012, n. 221) continuando ad operare secondo le attuali modalita' di cui all'allegato tecnico del decreto n. 32 del 19 gennaio 2012 e restano inalterate l'organizzazione ed i flussi dei dati nonche' i trattamenti che su di essi intervengono ad eccezione dei meccanismi di sicurezza a protezione del canale di comunicazione secondo quanto indicato nel presente allegato tecnico.

L'attuale meccanismo di sicurezza, che protegge il collegamento tra i comuni con il CNSD ed il CNSD con altri Enti, viene sostituito da un canale di comunicazione protetto dal protocollo HTTPS, con mutua autenticazione della postazione di lavoro del comune e del servizio esposto da ANPR.

I comuni continuano ad inviare le informazioni anagrafiche attraverso file corrispondenti agli attuali formati.

L'identificazione dell'utente continua ad essere effettuata secondo le modalita' indicate nell'allegato tecnico del decreto n. 32 del 19 gennaio 2012 che prevedono un meccanismo di autenticazione basato sull'uso di utente/password al fine di identificare l'operatore. Per il censimento degli utenti viene utilizzato il database delle utenze gia' presente presso il CNSD.

Le Amministrazioni/enti connessi al CNSD fruiscono dei servizi del Centro attraverso file corrispondenti agli attuati formati. Il collegamento e' assicurato attraverso le metodologie standard di cooperazione tra enti.

4.6.2. - Fase 2

In questa fase e' resa disponibile anche la nuova banca dati dell'ANPR contestualmente ai servizi resi dall'INA e dall'AIRE (quali ANPR) e si procede alla progressiva migrazione delle banche dati relative alle anagrafi comunali della popolazione residente e dei cittadini italiani residenti all'estero nell'ANPR.

Le informazioni anagrafiche sono registrate su entrambi i sistemi, quello comunale e quello centrale dell'ANPR.

A tale fine e' necessario adeguare le procedure di invio delle informazioni anagrafiche per realizzare un meccanismo di allineamento automatico tra le banche dati relative alle anagrafi comunali e quella centrale.

Il livello di sicurezza nella trasmissione dei dati dalla postazione comunale verso la nuova banca dati ANPR e' analogo a quello della fase 1 fermo restando che i meccanismi implementati saranno quelli di cui alla fase 3 descritti al paragrafo 4.5.

Effettuata la migrazione delle anagrafi comunali nell'ANPR, le banche dati relative alle anagrafi comunali vengono dismesse.
