Raccomandazione 1

Logotipo EMS

Si raccomanda alle Amministrazioni postali:

1. di utilizzare le specifiche tecniche del logotipo EMS figurante nel Manuale EMS al fine della commercializzazione e utilizzazione del loro servizio EMS, ivi compresa l'eventuale elaborazione di un sistema d'imballaggio uniformato per gli invii EMS;

2. di adottare le misure necessarie al fine di proteggere a livello nazionale, il nome ed il logotipo EMS.

Raccomandazione 2

Modalita' d'identificazione unica

Si raccomanda alle Amministrazioni postali di utilizzare la specifica in appresso per l'identificazione unica degli invii EMS e dei sacchi dei contenitori o dei recipienti contenenti invii EMS.

Specifica delle modalita' d'identificazione unica EMS

Numero di caratteri: 13

Disposizione a partire da sinistra:

- posizioni 1 e 2: ossia i caratteri "EE" (o, se necessario i caratteri "EA", "EB", "EC" ecc. fino a "EM") per indicare gli invii (1) EMS, ossia i caratteri "ES" per indicare un sacco/contenitore/recipiente EMS;

- posizioni 3 a 10 compresa: numeri d'ordine;

- posizione 11: numero di controllo generato dall'elaboratore, conforme al "modulo 11 ponderato"; (2)

- posizioni 12 e 13: codice ISO Alfa-2 per designare l'Amministrazione di origine (3).

(1) Nella sua raccomandazione iniziale relativa ai mezzi di

identificazione unica (CCEP 1/1988), il CCEP del 1988 aveva

previsto delle serie di prefissi a due caratteri, da "EA" a

"EM", riservati all'uso futuro del servizio postale

internazionale dopo assegnazione da parte del CCEP. Di

conseguenza, il CCEP del 1992 ha deciso di attribuire

queste serie di prefissi (in quanto prefissi da utilizzare

oltre al prefisso "EE") per l'identificazione degli invii

EMS nelle Amministrazioni che spediscono quantita' di posta

EMS abbastanza importanti da giustificare l'uso di prefissi

addizionali. Le Amministrazioni che non hanno ancora

previsto nei loro sistemi di monitoraggio e di

localizzazione l'eventuale utilizzazione dei prefissi

riservati, da "EA" e "EM", dovrebbero sin d'ora procedere

ai necessari adeguamenti.

(2) La norma iniziale consentiva alle Amministrazioni di

utilizzare un carattere alfabetico "X" senza significato

particolare. Il CCEP ha convenuto che tutti i codici a

barre utilizzati nel servizio EMS devono essere conformi a

tale norma modificata entro la fine del 1992 (vedere anche

la formulazione del modulo 11 ponderato all'annesso 1).

(3) I codici Alfa-2 di paesi e di territori essendo di

competenza dell'Unione, sono pubblicati nella Raccolta

operativa EMS in due liste, una secondo l'ordine alfabetico

dei paesi e dei territori, l'altra secondo l'ordine

alfabetico degli stessi codici.

Esempio:

________________________________________________

E E 4 7 3 1 2 4 8 2 9 G B

_______________________________________________ 1 2 3 4 5 6 7 8 9 10 11 12 13

_____ _______________________ ___ _______ | | | |

Invio EMS______________| | | |

| | |

Numero__________________________________| | |

| |

Numero di controllo_____________________________________| |

|

"Gran Bretagna"_________________________________________________|

Quando occorre un codice a barre come mezzo di identificazione unica di un invio EMS internazionale, si utilizza il sistema di simboli Codice 39, conforme alla norma europea EN 800 ed alla norma "Uniform Symbology Specification Code 39" (Codice 39 di specifica di simbologia uniforme) dell'AIM. Tuttavia, questo codice deve corrispondere ai parametri di seguito citati. Il simbolo del codice a barre deve comprendere, nella posizione 11 (a partire da sinistra) un numero di controllo generato mediante elaboratore e conforme al modulo 11 ponderato. Le lettere ed i numeri del codice a barre devono essere stampati nella forma abituale, sopra o sotto il simbolo del codice a barre.

Parametri per i simboli del codice 39 (1)

Dimensione X (larghezza nominale dell'elemento stretto): tra 0,25 mm e 0,43 mm.

Dimensione N (rapporto tra la larghezza di un elemento largo ed un elemento stretto): minimo 2,5 a 1; massimo 3,0 a 1. Ogni qualvolta cio' sia possibile e' preferibile scegliere il rapporto 3,0 a 1.

Spazio tra i caratteri: minimo 1X; massimo 1,524 mm. quando X maggiore o uguale 0,287 mm. oppure 5,3 X quando X minore 0,287 mm.

Altezza delle barre: 15% della larghezza del simbolo nel suo insieme o 0,90 mm. con preferenza per il valore piu' alto.

La qualita' della stampa si valuta in funzione della norma ANSI X3 182-1990, secondo la quale il diametro del fascio luminoso del lettore deve essere di 0,127 mm e la lunghezza d'onda di tale fascio di 630 o 660 nanometri. Il livello minimo di qualita' della stampa deve corrispondere alla lettera B secondo la notazione di tale norma.

(1) Gli esempi di dimensioni per questi parametri figurano

nell'annesso 3 alla presente Raccomandazione.

Annesso 4 alla Raccomandazione 2

Caratteristiche del codice 39

1. Nel codice 39 le barre e le spaziature sono codificate binariamente in larghezza: le barre/spaziature strette sono interpretate come valore binario 0 (zero) e le barre/spaziature larghe come valore binario 1.

2. Ogni carattere si compone di nove elementi: cinque barre e quattro spaziature. Tre di questi elementi sono larghi e sei sono stretti, donde il nome di Codice 39 (3 da 9). La figura di seguito descrive la struttura dei caratteri.

3. L'algoritmo primario e' binario; si applica sia alle barre sia alle spaziature del codice. Le barre o le spaziature strette sono interpretate come valore binario 0 (zero), le barre o le spaziature larghe come valore binario 1.

Codice a barre 39

Parte di provvedimento in formato grafico

Formulazione del modulo 11 ponderato

La formulazione e' la seguente:

1. applicare i fattori di ponderazione ai numeri di base utilizzando i seguenti numeri: 86423597;

2. calcolare la somma di questi numeri;

3. dividere questa somma per 11 (undici);

4. se il resto e' uguale a 0 (zero) utilizzare 5 (cinque) come numero di controllo. Se il resto e' 1 (uno) utilizzare 0 (zero) come numero di controllo;

5. se del caso, sottrarre il resto di 11. La cifra ottenuta corrisponde al numero di controllo.

Esempio:

Numeri 4 7 3 1 2 4 8 2

Fattori

di ponderazione x 8 x 6 x 4 x 2 x 3 x 5 x 9 x 7

_____________________________________________

32 +42 +12 +2 +6 +20 +72 +14 = 200

200 : 11 = 18 Resto 2

11 - 2 = 9 Numero di controllo

Numero di autocontrollo completo: 473124829

Annesso 2 alla Raccomandazione 2

Esempi di dimensioni per i parametri del Codice 39

Nota: Nelle colonne (3) a (7) i valori minimi sono stampati a caratteri ordinari ed i valori massimi in corsivo.

_____________________________________________________________________ (1) (2) (3) (4) (5) (6) (7) (8

Dimens. Dimens. Spazio Largh. Num. Largh. Altezza Tolleranz X N tra i caratt. caratt. simbolo minima stampag.

caratt. per barre (+ o -)

pollice

_______ _______ _______ ________ ________ _______ _______ _________ 0.25 2.5 0.250 3.625 7.01 54.13 9.0 0.068

1.325 4.700 5.40 69.18 10.4

3.0 0.250 4.000 6.35 59.75 9.0 0.086

1.325 5.075 5.00 74.80 11.2

0.30 2.5 0.300 4.350 5.84 64.95 9.8 0.082

1.524 5.574 4.56 82.09 12.3

3.0 0.300 4.800 5.29 71.70 10.8 0.104

1.524 6.024 4.22 88.84 13.3

0.33 2.5 0.330 4.785 5.31 71.45 10.7 0.090

1.524 5.979 4.25 88.16 13.2

3.0 0.330 5.280 4.81 78.87 11.8 0.114

1.524 6.474 3.92 95.59 14.3

0.43 2.5 0.430 5.805 4.38 86.65 13.0 0.117

1.524 6.899 3.68 101.96 15.3

3.0 0.430 6.450 3.94 96.32 14.4 0.148

1.524 7.544 3.37 111.64 16.7

_____________________________________________________________________

Note:

Tutte le dimensioni sono in millimetri.

La dimensione X rappresenta la larghezza nominale

dell'elemento stretto.

La dimensione N rappresenta il rapporto tra la larghezza

di un elemento largo e quella di un elemento stretto.

La larghezza del carattere indicato comprende lo spazio

tra i caratteri.

La larghezza del simbolo comprende 13 caratteri oltre al

carattere iniziale e finale ma non tiene conto delle zone

vergini che dovrebbero essere di 5 mm al minimo su ciascun

lato del simbolo.

L'altezza delle barre e' il 15% della larghezza del

simbolo o 9 mm., con preferenza per il valore piu' alto.

La "tolleranza di stampa" fa riferimento alla tolleranza

di larghezza di un elemento per consentire varianti in

materia di stampaggio.

Raccomandazione 3

Etichettatura

Oltre a quanto stabilito all'art. 103 del Regolamento-quadro EMS, si raccomanda alle Amministrazioni postali:

1. di numerare ciascuna casella utilizzata per le etichette EMS secondo il sistema indicato in appresso;

2. di prendere nota della localizzazione delle caselle numerate figuranti nel modulo E 1 - in allegato;

3. di utilizzare le etichette EMS "manifold" (multiformi) in modo da disporre di copie sufficienti per soddisfare alle esigenze di sdoganamento e di monitoraggio, di localizzazione e di conferma e di prova della distribuzione.

Sistema di numerazione delle caselle per le etichette EMS

N. Designazione

1 - Logotipo EMS

- Nome dell'Amministrazione di origine

- Nome del servizio EMS nazionale (a scelta)

2 Identificazione alfanumerica EMS in 13 caratteri, sotto forma di codice a barre

3 Identificazione alfanumerica EMS in 13 caratteri tipografici

4 Data d'impostazione

5 Ora d'impostazione

6 Numero di conto del mittente

7 Numero telefonico del mittente

8 Nome ed indirizzo del mittente

9 Codice postale del mittente

10 Numero di conto del destinatario

11 Numero telefonico del destinatario

12 Numero ed indirizzo del destinatario

13 Punto di scambio (da utilizzare solo se un'Amministrazione distingue tra un numero di conto ed il numero d'identificazione di un determinato collegamento)

14 Codice postale del destinatario

15 Numero di articoli nell'invio

16 Numero dell'articolo

17 Tipo di prodotto

18 Modalita' di pagamento

19 Diritti di assicurazione

20 Tassa di spedizione

21 Descrizione del contenuto (si raccomanda di utilizzare il numero doganale)

22 Regalo

(oppure)

23 Campione merci

24 Valore del contenuto

25 Peso in kg. Numero arrotondato al mezzo-chilogrammo (p. es. 3,2 kg si legge 3,5 kg)

26 Direttive speciali

27 Nome a caratteri tipografici della persona che riceve l'invio

28 Firma

29 Data di consegna

30 Ora di consegna

31 Nome dell'ufficio d'origine

32 Recapitato, o tentativo di recapito

33 Numero dell'autorizzazione (porto franco in anticipo in contanti) 34 Numero di serie (porto franco in anticipo in contanti)

35 Diritti di raccolta

36 Importo totale delle tasse

37 Firma dell'agente che accetta l'invio

38 Numero dell'ufficio di origine

39 Firma del mittente

Ogni casella addizionale eventualmente selezionata dal CCEP dovra' essere numerata secondo la sequenza adottata (vale a dire 40, 41, ecc.). Il numero corrispondente ad una casella che e' stata eliminata diviene privo di effetti e le altre caselle conservano il loro numero.

Raccomandazione 4

Sistemi di monitoraggio e di localizzazione computerizzati

Si raccomanda alle Amministrazioni di insediare a livello locale un sistema di monitoraggio e di localizzazione EMS computerizzato e collegarlo al sistema di monitoraggio e di localizzazione internazionale (cassetta postale elettronica), in considerazione delle seguenti specifiche (1)

Specifiche dei sistemi di monitoraggio e di localizzazione EMS

A. Obiettivi

Grazie alla registrazione di informazioni precise sugli avvenimenti verificatisi nella trasmissione degli invii EMS dall'impostazione fino alla distribuzione, i sistemi di monitoraggio e di localizzazione computerizzati mirano a:

1. permettere alle Amministrazioni di rispondere alle richieste di informazione ed ai reclami relativi agli invii EMS individuali avanzati dai clienti;

2. segnalare alle altre Amministrazioni collegate, gli eventuali incidenti nel flusso di traffico, ad esempio scioperi, chiusura di aeroporti per causa d'intemperie ecc.

3. fornire a fini di gestione e di commercializzazione del servizio EMS, statistiche relative alla misura dell'esecuzione del servizio nonche' alla composizione del traffico e della clientela.

(1) Tali specifiche si applicano sia alle Amministrazioni

postali, sia ai soci esterni della posta che hanno un

contratto d'ingaggio per la distribuzione degli invii EMS B. Caratteristiche generali

1. Le Amministrazioni che dispongono di sistemi di monitoraggio e di localizzazione EMS computerizzati collegati alla cassetta postale elettronica possono effettuare ricerche solo per gli invii impostati o distribuiti sul loro territorio.

2. La riservatezza delle informazioni che figurano in questi sistemi e' assicurata mediante parole d'ordine.

3. Questi sistemi devono sempre essere in funzione 24 ore su 24.

C. Formato per lo scambio di dati tra le Amministrazioni collegate

alla cassetta elettronica

Questo formato e la sintassi dei messaggi sono basati sulla norma EDIFACT (Interscambi di dati elettronici per le Amministrazioni, il Commercio ed il Trasporto) dell'ISO. Ogni messaggio e' costituito da segmenti che contengono informazioni relative agli avvenimenti da trasmettere. All'interno di un segmento (descrittivo di un avvenimento) si distinguono tre parti diverse:

1. Identificazione del tipo di avvenimento

secondo la lista di seguito an3

2. Dati obbligatori per l'identificazione

dell'avvenimento

a) codice di identificazione dell'invio,

compreso il nome del paese an13

b) paese di destinazione a2

c) data e ora dell'avvenimento (YYMMDDHHMM) n10

3. Dati facoltativi

Per ciascun tipo di avvenimento, possono essere trasmesse informazioni addizionali come quelle specificate nella seguente lista.

Nota: a = alfa; an = alfanumerica; n = numerica

Decisioni diverse da quelle che modificano gli Atti

_____________________________________________________________________ Tipo di Descrizione Descrizione Formato

evento dell'evento rubrica

_________ _________________ _____________________________ _________ EMA Impostaz./raccol- Identita' ufficio di scambio an..9

ta N. conto del cliente an..17

Codice postale mittente an..9

Luogo di origine (mittente) a..6

Codice postale destinatario an..9

Luogo di destinazione a..6

EMB Arrivo all'uffi- Identita' dell'ufficio di an..6

cio di scambio scambio

di partenza

EMC Partenza dall'uf- Identita' dell'ufficio di

ficio di scambio scambio an..6

di partenza N. del dispaccio an..4

Indirizzo del destinatario

del dispaccio (2) an..6

numero del volo (2) an..6

Data di partenza/primo volo n6

EMJ Arrivo all'uffi- Identita' dell'ufficio di

cio di scambio scambio di transito di

di transito origine an..6

Identita' dell'ufficio di

scambio di transito di

origine an..6

N. del dispaccio an..4

EMK Partenza dall'uf- Identita' dell'ufficio di

ficio di scambio scambio di transito an..6

di transito N. del dispaccio attribuito

dall'ufficio di scambio di

transito an..4

Indirizzo del destinatario

del dispaccio (2) an..6

Numero del volo (3) an..6

Data di partenza/primo volo n6

EMD Arrivo all'uffi- Identita' dell'ufficio di

cio di scambio di scambio di arrivo an..6

arrivo Identita' dell'ufficio di

scambio di origine o di tran-

sito an..6

N. del dispaccio an..4

EME Consegna alla Identita' dell'ufficio di

dogana scambio an..6

Codice di ritenzione quando

la dogana trattiene l'invio

(4) n2

EMF Partenza dall'uf- Identita' dell'ufficio di

ficio di scambio scambio an..6

di arrivo soggetto a diritti doganali

(5) a1

non soggetto a diritti doga-

nali (D o N) a1

EMG Arrivo all'Uffi- Identita' dell'Ufficio di re-

cio di scambio di capito an..9

arrivo

EMH Vano tentativo di Identita' dell'Ufficio di re-

recapito capito an..9

Codice di vano tentativo di

recapito (5) an3

EMI Consegna finale Identita' dell'ufficio di re-

capito an..9

Nome del destinatario che ha

firmato a..17

___________________________________________________________________ EMX Informazione sotto forma libera, alfa numerica

___________________________________________________________________ in 10 (1) Il codice di questo formato e' il seguente:

in 10 a = alfa;

in 10 an = alfanumerico;

in 10 n = numerico;

in 10 Nota: i due punti significano "fino a"; ad esempio an..9 significa "fino a 9 caratteri alfanumerici".

in 10 (2) Ufficio di scambio di arrivo o di transito.

in 10 (3) Insieme di dati che puo' includere fino a sei numeri di voli.

in 10 (4) Puo' trattarsi di un insieme di dati (v. annesso 1 a questa raccomandazione).

in 10 (5) V. annesso 2 a questa raccomandazione.

in 0 _____________________________________________________________________

D. Funzioni del sistema di ricerca

in 0 Le funzioni del sistema di ricerca sono le seguenti:

in 0

1. commutazione di messaggi per esigenze di gestione (informazione in radiodiffusione o urgente)

in 0

2. ricerca in base all'individuazione dell'invio (specificante sia un invio, sia una lista di averi classificati secondo i numeri di identificazione);

in 0

3. ricerche basate sulle caratteristiche dell'invio o dell'evento: queste ricerche sono basate sui valori designati con i seguenti parametri:

in 04 - n. del dispaccio:

in 04 - luogo di origine;

in 04 - luogo di consegna;

in 04 - data dell'evento;

in 04 - data e ora del messaggio;

in 04 - natura dell'avvenimento;

in 04

4. trasmissione di dati in massa che consente l'elaborazione locale degli stessi.

in 0 Annesso 1 alla raccomandazione 4

Codice per la ritenzione degli invii EMS in dogana

Codice Descrizione

19 Oggetti vietati

20 Oggetti la cui importazione e' soggetta a

limitazione - Licenza d'importazione richiesta 50 Fattura mancante

51 Fattura inadeguata

52 Certificato di origine mancante

53 Certificato di origine inadeguato

54 C 2/CP 3 mancante

55 C 2/CP inadeguato

56 Merce pregiata - Dichiarazione ufficiale in

dogana richiesta

57 Impossibilita' di contattare il destinatario

per informazioni sull'importazione

58 Si attende presentazione in dogana del

commissionario

59 Numero IVA o d'importazione richiesto

60 Certificato merci rinviate richiesto

61 Modulo di bonifico chiesto alla banca

62 Spedizione incompleta

99 Varie

Annesso 2 alla raccomandazione 4

Codice per il mancato recapito di invii EMS

1. Misure adottate

Codice Misura

A Tentativo di recapito effettuato in data

odierna

B Tentativo di recapito da effettuare il giorno

feriale successivo

C Invio trattenuto, notifica del destinatario in corso

D Mittente contattato, si attende risposta

E Invio rispedito al mittente

F Invio rispedito

G Invio trattenuto per ispezione

H Invio confiscato o distrutto per via della

natura del contenuto

Motivo del mancato recapito

Codice Motivo

0 Indirizzo inesatto

1 Destinatario introvabile

2 Destinatario non rinvenuto all'indirizzo

indicato; ufficio del destinatario chiuso

3 Invio rifiutato dal destinatario

4 Il mittente ha chiesto un'ulteriore consegna

5 Sciopero del destinatario

6 Mancato recapito

7 Invio disguidato

8 Avaria - Invio non recapitato

9 Oggetti vietati - invio non recapitato

0 Importazione soggetta a restrizione - Invio non recapitato

1 Pagamento tasse

9 Varie

Combinazioni possibili (1)

_____________________________________________________________________ Misura Motivo

10 11 12 13 14 15 16 17 18 19 20 21 99 ______ ______________________________________________________________ A X X X X X X X X X X ______ ______________________________________________________________ B X X X X X

______ ______________________________________________________________ C X X X X X X X X

______ ______________________________________________________________ D X X X X X X

______ ______________________________________________________________ E X X X X X

______ ______________________________________________________________ F X X

______ ______________________________________________________________ G X

______ ______________________________________________________________ H X X

____________________________________________________________________ Annesso 3 alla raccomandazione 4

Norme relative alla trasmissione di informazioni alla cassetta postale elettronica

Grado di realizzazione degli obiettivi relativi alla trasmissione d'informazioni

_____________________________________________________________________ Evento Per la trasmissione di informazioni su detti eventi

alla cassetta postale elettronica, le Amministrazioni

sono pregate di rispettare le seguenti norme

____________ ______________________________________________________ Evento EMC Informazioni per il 100% degli invii

Partenza

dall'ufficio

di scambio

di partenza

Evento EMD Informazioni per il 100% degli invii

Arrivo al-

l'ufficio di

scambio di

arrivo

Evento EMH Obiettivo convenuto e realizzabile in considerazione

Vano tenta- della zona di recapito, a seconda se si tratta di zona tivo di re- urbana o non

capito

Evento EMI Obiettivo convenuto e realizzabile in considerazione

Consegna fi- della zona di recapito, a seconda se si tratta di zona nale di re- urbana o non

capito

___________________________________________________________________ Es.: A13 significa un tentativo di recapito effettuato in data odierna, il destinatario avendo rifiutato l'invio

II. Scadenze limite per la trasmissione delle informazioni

____________________________________________________________________ Evento Le Amministrazioni devono trasmettere le informazioni su detti eventi alla cassetta postale elettronica en- tro le seguenti scadenze

__________________________________________________________________ Evento EMD Entro 12 ore dopo l'evento

Arrivo al-

l'ufficio di

scambio di

arrivo

Evento EMH Entro 24 ore dopo l'evento

Vano tenta-

tivo di

recapito

Evento EMI Entro 24 ore dopo l'evento

Consegna

finale

___________________________________________________________________ III. Orari di trasmissione delle informazioni

Le Amministrazioni devono trasmettere le informazioni alla cassetta postale elettronica nelle seguenti fasce orarie:

_____________________________________________________________________ Fascia oraria Evento

___________________________________________________________________ Fra le h. 9 00 e le h. 10 00 EMD (arrivo all'ufficio di scambio

d'arrivo del traffico proveniente da

uno "hub" o da voli commerciali)

EMH (vano tentativo di recapito il

giorno precedente)

EMI (consegna finale effettuata il

giorno precedente

Fra le h. 13 00 e le h. 14 00 EMD (arrivo all'ufficio di scambio

d'arrivo del traffico proveniente da

voli commerciali)

EMH (vano tentativo di recapito)

EMI (consegna finale degli invii per- venuti in mattinata)

Fra le h. 17 00 e le h. 18 00 EMD (arrivo all'ufficio di scambio

d'arrivo del traffico proveniente da

voli commerciali)

EMH (vano tentativo di recapito)

EMI (consegna finale degli invii gia' pervenuti in giornata)

Fra le h. 21 00 e le h. 22 00 EMD (arrivo all'ufficio di scambio

d'arrivo del traffico proveniente da

voli commerciali)

EMH (vano tentativo di recapito)

EMI (consegna finale degli invii di-

stribuiti lo stesso giorno)

___________________________________________________________________

Raccomandazione 5

Notifica dei dispacci

Si raccomanda alle Amministrazioni postali di notificare l'arrivo dei dispacci EMS all'Amministrazione di destinazione, mediante collegamento informatizzato, telefono, telex, telefax o posta elettronica.

Raccomandazione 6

Controllo del trattamento applicato dalle compagnie aeree

Si raccomanda alle Amministrazioni postali di controllare la qualita' del trattamento applicato agli invii EMS dalle compagnie aeree e di prendere, se del caso, le misure correttive necessarie a livello locale.

Raccomandazione 7

Sdoganamento

Le Amministrazioni postali sono incoraggiate ad accelerare lo sdoganamento degli invii EMS con tutti i mezzi a loro disposizione, in particolare:

1. comitati di contatto nazionali;

2. studi approfonditi dell'organizzazione dei servizi negli aeroporti in collegamento con i servizi doganali locali, le compagnie aeree e le autorita' aeroportuali;

3. trasmissione preliminare, in particolare in forma elettronica, delle informazioni necessarie alle autorita' doganali per realizzare lo sdoganamento degli invii EMS su ..... e prima dell'arrivo degli invii.

Raccomandazione 8

Recapito degli invii

Si raccomanda alle Amministrazioni postali:

1. di effettuare il recapito degli invii EMS mediante una rete che consente di raggiungere un livello di rendimento concorrenziale;

2. di assicurare il recapito degli invii EMS in arrivo con fattorino speciale o regolare

Raccomandazione 9

Valutazione dell'esecuzione del servizio

Si raccomanda alle Amministrazioni postali:

1. di instaurare un sistema regolare per valutare l'esecuzione del servizio EMS;

2. di adoperare per questo sistema il metodo piu' conveniente, fermo restando che le Amministrazioni postali devono adottare di preferenza un sistema di monitoraggio e di localizzazione EMS informatizzato.

Raccomandazione 10

Centri operativi

Si raccomanda alle Amministrazioni postali di elaborare un centro operativo cui si possa fare appello, 24 ore su 24 per risolvere i problemi, ivi compresi i reclami, connessi al servizio EMS.

Raccomandazione 11

Responsabilita'

Si raccomanda alle Amministrazioni postali:

1. di assumersi la responsabilita' e di versare un'indennita' corrispondente all'ammontare effettivo della perdita, della defraudazione o dell'avaria di invii EMS;

2. di stabilire se del caso un limite massimo per detta indennita', a condizione che tale ammontare massimo non sia inferiore a 30 DTS per gli invii contenenti unicamente documenti, ed a 130 DTS per quelli che contengono altri oggetti;

3. di rimborsare la totalita' delle tasse postali pagate, sia quando un'indennita' e' dovuta per perdita, defraudazione totale o avaria totale, sia in caso di ritardo nella distribuzione, il pagamento dell'indennita' ed il rimborso delle tasse postali dovendo essere sollecitamente effettuato dall'Amministrazione di origine dopo aver accertato le irregolarita';

4. di ammettere che l'Amministrazione responsabile prenda a suo carico l'indennita' da versare e le tasse postali da rimborsare al mittente;

5. di determinare le irregolarita' per mezzo di una speciale scheda di verifica conforme al modello E2 allegato, e di dare seguito ai reclami secondo le disposizioni dell'Articolo 15 dell'Accordo quadro;

6. di determinare le responsabilita' tra le Amministrazioni se del caso per analogia con le disposizioni della Convenzione o dell'Accordo relativo ai pacchi postali.

Raccomandazione 12

Compensazione degli squilibri degli scambi

Oltre a quanto stabilito nell'articolo 11 dell'Accordo-quadro, si raccomanda alle Amministrazioni postali di prevedere una compensazione quando lo squilibrio annuale degli scambi e' di 100 o piu' invii.

Raccomandazione 13

Norme di servizio per la clientela

Si raccomanda alle Amministrazioni postali:

1. di adottare le seguenti misure che costituiscono gli elementi del servizio per la clientela EMS, la cui adozione a breve termine e' ritenuta auspicabile:

Informazione

a) promulgare una guida al servizio EMS;

b) divulgare materiale di promozione come pubblicita' postale, opuscoli e d!pliant;

c) pubblicare numeri telefonici come punti di contatto per la vendita e l'informazione;

Accessibilita'

d) rendere riconoscibili dall'esterno gli uffici postali che accettano invii EMS;

e) installare speciali sportelli EMS;

f) offrire di ritirare gli invii nei locali dei clienti;

g) mettere a disposizione, gratuitamente, materiale di spedizione, come etichette e documenti doganali su richiesta del cliente;

Funzionalita'

h) sviluppare un sistema rapido e funzionale per il trattamento dei reclami e dei ricorsi;

i) stabilire norme di recapito garantite prevedendo un rimborso per gli invii ritardati;

k) rilasciare su richiesta una prova del recapito (firma del destinatario);

l) pubblicare esplicite modalita' e condizioni per il trasporto e la responsabilita';

m) mettere in funzione un sistema di monitoraggio e di localizzazione manuale;

Comportamento verso i clienti

n) promuovere comportamenti positivi riguardo al servizio EMS tra gli addetti agli sportelli, i fattorini ed i dirigenti;

2. adottare per quanto possibile, le seguenti misure che rappresentano gli elementi di servizio EMS addizionali, in vista della loro adozione a medio termine;

Informazione

o) avvalersi di rappresentanti commerciali come punti di contatti per la vendita e l'informazione;

Accessibilita'

p) in considerazione di elementi di sicurezza, aprire speciali sportelli EMS negli aeroporti per l'impostazione all'ultimo momento di invii EMS;

Funzionalita'

q) attuare un sistema di monitoraggio e di localizzazione informatizzato;

3. prendere nota dei seguenti eventuali provvedimenti addizionali ed esaminare se la loro adozione e' auspicabile e realizzabile nel servizio EMS nazionale:

r) offrire tariffe introduttive speciali;

s) offrire di ritirare gli invii nei locali di tutti i clienti;

t) sistemare cassette postali EMS speciali nelle strade o negli immobili dei quartieri di affari;

u) procedere al confezionamento della posta EMS pronta per la spedizione su richiesta del cliente, sia gratuitamente sia dietro pagamento;

v) addebitare i costi mediante fattura, conto mensile o fattura dettagliata;

w) offrire ai clienti un servizio speciale per i casi difficili, come il recapito a richiesta al di la' dell'area di servizio, l'ammissione di dimensioni e di pesi fuori misura e gli accordi per il ritiro a domicilio;

4. prestare particolare attenzione ai vari elementi di servizio alla clientela offerti dalla concorrenza.

Raccomandazione 14

Informazioni sulla clientela

Si raccomanda alle Amministrazioni postali:

1. di creare e di aggiornare, nell'ambito della loro raccolta di informazioni necessarie per l'analisi della concorrenza e la pianificazione di strategie commerciali, degli schedari sugli effettivi clienti EMS, sia di impostazione che destinatari e sui potenziali gruppi-bersaglio;

2. di classificare le informazioni a seconda del tipo di attivita' e del volume di traffico;

3. di porre, su richiesta, le informazioni pertinenti a disposizione delle Amministrazioni che intendono localizzare la potenziale clientela.

Raccomandazione 15

Sacchi EMS

Si raccomanda alle Amministrazioni postali di adottare, per i loro sacchi EMS, le specifiche del "Modello di sacco EMS" in appresso.

Modello di sacco EMS

Parte di provvedimento in formato grafico

Colore delle strisce: Pantone Matching System 286 (blu) e 151 (arancione)

Sono ammesse le strisce verticali, orizzontali e diagonali.

Larghezza delle strisce: 5,5 cm.

Colore del logo: bianco o nero

Il logo EMS puo' essere riprodotto piu' volte sui due lati del sacco.

Il nome dell'Amministrazione postale deve figurare sul sacco.

Raccomandazione 16

Modello di accordo bilaterale relativo alla qualita' del servizio EMS Si raccomanda alle Amministrazioni postali di avvalersi delle disposizioni stabilite nell'allegato modello di accordo come riferimento per la formulazione degli accordi bilaterali sulla qualita' del servizio EMS che concluderanno con altre Amministrazioni.
