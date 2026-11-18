"""Compute every number of the 20 charts into .build/data.json (run by make.py).

    python -X utf8 visualisations/src/prep.py visualisations/src/.build

Reads only what make.py extracted from git objects into .build/: the compact history (log-*.tsv), the files the
Constitution and the codes changed (log-files.tsv), the tree of normativa/ (tree-normativa.tsv), and the records read
from blobs (blob-*.tsv: act headings, Senate bills, Camera votes, Constitutional Court schede; blob-costituzione.jsonl;
repo/data/atti.csv). Writes .build/data.json and .build/prep.log (the checks printed along the way).
"""
import collections, csv, datetime, html, json, os, re, statistics, sys

B = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '.build')
HEAD = os.environ.get('HEAD_SHA', '')
LOG = open(os.path.join(B, 'prep.log'), 'w', encoding='utf-8', newline='\n')
csv.field_size_limit(1 << 30)


def say(*a):
    print(*a)
    print(*a, file=LOG)


D = datetime.date.fromisoformat
DAYS = lambda a, b: (D(b) - D(a)).days
OUT = {}
PF = {}
MESI = {'gennaio': 1, 'febbraio': 2, 'marzo': 3, 'aprile': 4, 'maggio': 5, 'giugno': 6, 'luglio': 7, 'agosto': 8,
        'settembre': 9, 'ottobre': 10, 'novembre': 11, 'dicembre': 12}


def itdate(s):
    """the first Italian date in a text ("8 novembre 1995", "1° gennaio 2012") as a date, or None"""
    m = re.search(r"(\d{1,2})[°º]?\s+([A-Za-z]+)\s+(\d{4})", s)
    if not m or m.group(2).lower() not in MESI:
        return None
    try:
        return datetime.date(int(m.group(3)), MESI[m.group(2).lower()], int(m.group(1)))
    except ValueError:
        return None


def tsv(name):
    with open(os.path.join(B, name), encoding='utf-8', newline='') as fh:
        for line in fh:
            yield line.rstrip('\n').split('\t')


def dict_tsv(name):
    with open(os.path.join(B, name), encoding='utf-8', newline='') as fh:
        yield from csv.DictReader(fh, delimiter='\t', quoting=csv.QUOTE_NONE)


def text(s):
    """a title as plain text: entities and tags removed, spaces collapsed, typographic apostrophes made plain"""
    s = html.unescape(html.unescape(s))
    s = re.sub(r'<[^>]+>', ' ', s).replace('’', "'").replace('‘', "'")
    return re.sub(r'\s+', ' ', s).strip()


def med(v):
    return statistics.median(v) if v else None


counts = json.load(open(os.path.join(B, 'counts.json'), encoding='utf-8'))
PF['commits'] = counts['commits']
PF['head'] = HEAD
ROM = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX']

# ------------------------------------------------------------------ the act folders of normativa/ and their headings
ACTS = {}                      # folder -> dict(kind, year, files, arts, added)
for r in tsv('tree-normativa.tsv'):
    if r[0] == 'A':
        p = r[1].split('/')
        ACTS[r[1]] = {'kind': p[1], 'year': int(p[2]), 'num': p[3], 'files': int(r[2]), 'arts': int(r[3]), 'added': int(r[4])}
HEADS = {r[0]: r[1] for r in tsv('blob-head.tsv')}
say('act folders', len(ACTS), '| headings', len(HEADS))
PF['acts'] = len(ACTS)

# the "testo vigente" commit of each act (Enacted, Published, In-force of the current version): matched to its folder
KF = [('legge-costituzionale', r'^LEGGE COSTITUZIONALE'), ('regio-decreto-legislativo', r'^REGIO DECRETO LEGISLATIVO'), ('regio-decreto-legge', r'^REGIO DECRETO-LEGGE'),
      ('regio-decreto', r'^(R\.D\.|REGIO DECRETO)'), ('dlgslgt', r'^(D\.LGS\.LGT\.|DECRETO LEGISLATIVO LUOGOTENENZIALE)'), ('decreto-luogotenenziale', r'^DECRETO LUOGOTENENZIALE'),
      ('decreto-legge', r'^(D\.L\.|DECRETO-LEGGE)'), ('decreto-legislativo', r'^(DECRETO LEGISLATIVO|D\.LGS\.)'), ('dpr', r'^(D\.P\.R\.|DECRETO DEL PRESIDENTE DELLA REPUBBLICA)'),
      ('dpcm', r'^(D\.P\.C\.M\.|DECRETO DEL PRESIDENTE DEL CONSIGLIO)'), ('dm', r'^(D\.M\.|DECRETO MINISTERIALE)'), ('legge', r'^LEGGE'), ('decreto', r'^DECRETO'),
      ('ordinanza', r'^ORDINANZA'), ('deliberazione', r'^DELIBERAZIONE')]
VIG = {}
NRM = []                       # code and statute history commits (Affecting)
for r in tsv('log-nrm.tsv'):
    if r[9]:
        NRM.append(r)
        continue
    if not r[5]:
        continue
    s = re.sub(r'^\d{4}-\d\d-\d\d: ', '', r[2]).upper()
    kf = next((k for k, pat in KF if re.match(pat, s)), None)
    m = re.search(r',? N\. ?([0-9A-Z]+)', s)
    if kf and m:
        VIG[f'normativa/{kf}/{r[5][:4]}/{m.group(1).lower()}'] = {'inf': r[4], 'enacted': r[5], 'pub': r[6][:10]}
say('testo vigente commits matched to folders', sum(1 for a in ACTS if a in VIG), 'of', len(ACTS))

GROUP = {'dpr': 'dpr', 'legge': 'legge', 'legge-costituzionale': 'legge', 'decreto-legge': 'dl', 'decreto-legislativo': 'dlgs', 'regio-decreto': 'regi',
         'regio-decreto-legislativo': 'regi', 'regio-decreto-legge': 'regi', 'dlgslgt': 'lgt', 'decreto-luogotenenziale': 'lgt', 'decreto': 'altri', 'dpcm': 'altri',
         'dm': 'altri', 'ordinanza': 'altri', 'deliberazione': 'altri'}
GK = ['dpr', 'legge', 'dl', 'dlgs', 'regi', 'lgt', 'altri']


def head_title(a):
    """the title of an act from its heading: what follows the kind, the date and the number"""
    h = HEADS.get(a, '')
    m = re.match(r'^.*?\d{4} [0-9A-Za-z]+(?:-\w+)? (.*)$', h)
    t = m.group(1) if m else h
    return re.split(r'\s*(?:\(\d{2}[A-Z]\d{5}\)|Entrata in vigore|Decreto-Legge (?:convertito|decaduto)|Il Decreto-Legge non)', t)[0].strip()


# ------------------------------------------------------------------ c01: the acts in force by year and kind
by_year = collections.defaultdict(collections.Counter)
for a, v in ACTS.items():
    by_year[v['year']][GROUP[v['kind']]] += 1
rows = [{'y': y, **{k: by_year[y][k] for k in GK if by_year[y][k]}} for y in range(min(by_year), max(by_year) + 1)]
tot = lambda r: sum(r.get(k, 0) for k in GK)
oldest = sorted((VIG.get(a, {}).get('enacted') or f"{v['year']}-12-31", a) for a, v in ACTS.items())[:6]
old = []
for y, a in oldest:
    old.append([a, VIG.get(a, {}).get('enacted', ''), head_title(a)[:160]])
kind_n = collections.Counter(v['kind'] for v in ACTS.values())
OUT['c01'] = {'rows': rows, 'kinds': kind_n, 'oldest': old,
              'pre1946': sum(tot(r) for r in rows if r['y'] < 1946), 'pre1970': sum(tot(r) for r in rows if r['y'] < 1970),
              'laws_pre1970': sum(1 for v in ACTS.values() if v['kind'] in ('legge', 'regio-decreto-legislativo', 'regio-decreto-legge', 'dlgslgt', 'decreto-legge', 'decreto-legislativo') and v['year'] < 1970)}
say('c01 total', sum(tot(r) for r in rows), 'pre1946', OUT['c01']['pre1946'], 'pre1970', OUT['c01']['pre1970'], 'peak', max(rows, key=tot)['y'], tot(max(rows, key=tot)), 'oldest', old[:2])

# ------------------------------------------------------------------ c02: what the acts in force are about (titles)
TOPICS = [   # matched in this order against the title as Normattiva gives it, lower-cased
    ('eccl', r"^riconoscimento,? agli effetti civili|^dichiarazione formale dei fini|fabbricer|^(soppressione|estinzione|riunione|unione) (della|delle|dei) (parrocchi|chies|confraternit|capitol)|parrocchi|confraternit"),
    ('enti', r"^(erezion[ei] in ente morale|che erige in ente morale|riconoscimento della personalit|estinzione dell|fusione (della|dell|delle|degli|dei)|trasformazione (della|dell)|soppressione dell'(ente|opera|istituto|asilo))|\bente morale\b"),
    ('statuti', r"^(modificazion[ei]|modific[ah]e|modifica) (allo|dello|degli|dell'|agli|al|alla) statut|^(approvazione|nuovo) (del |dello |del nuovo )?statut|^statuto\b"),
    ('trattati', r"^(ratifica|esecuzione (dell|della|del|dello|degli|delle)|approvazione ed esecuzione|piena ed intera esecuzione|adesione|autorizzazione alla ratifica)\b"),
    ('autor', r"^autorizzazione (a|al|alla|all'|ad|agli|alle|allo)\b|^(che )?autorizza\b"),
    ('fond', r"^trasferimento in propriet|riforma fondiaria|^(espropriazione|esproprio) di terreni"),
    ('enel', r"ente nazionale per l'energia elettrica|\benel\b"),
    ('osp', r"^(dichiarazione di ente ospedaliero|costituzione (in|dell') ?ente ospedaliero|costituzione dell'ente ospedaliero)"),
    ('scuole', r"^(istituzione|trasferimento|assegnazione|soppressione) di (un|una|due|tre|posti) (posto|posti|istituto|liceo|scuola|cattedr|ruol)|universit"),
    ('comuni', r"^(riunione dei comuni|aggregazione|ricostituzione del comune|distacco|inclusione dell'abitato|(cambiamento|mutamento|modificazione|modifica) (della|delle) (denominazione|circoscrizion)|costituzione in comun|separazione della frazione)"),
    ('conv', r"^(conversione in legge|convalidazione)"),
    ('ue', r"^(attuazione|recepimento) (della|delle|dell') ?direttiv"),
    ('reg', r"^(regolamento|regolamenti|approvazione del regolamento|norme di attuazione|norme regolamentari)\b"),
]
topic_n = collections.Counter(); topic_dec = collections.defaultdict(collections.Counter); topic_kind = collections.defaultdict(collections.Counter)
examples = collections.defaultdict(list)
no_title = 0
for a, v in ACTS.items():
    t = re.sub(r'^\W+', '', head_title(a).lower().replace('’', "'").replace("all' ", "all'").replace("dell' ", "dell'"))
    if not t:
        no_title += 1
    k = next((k for k, pat in TOPICS if re.search(pat, t)), 'altro')
    topic_n[k] += 1
    topic_dec[k][v['year'] // 10 * 10] += 1
    topic_kind[k][GROUP[v['kind']]] += 1
    if len(examples[k]) < 4 and (v['year'] * 7919 + len(examples[k])) % 13 == 0:
        examples[k].append([v['year'], head_title(a)[:110]])
OUT['c02'] = {'n': topic_n, 'dec': topic_dec, 'kind': topic_kind, 'no_title': no_title}
say('c02 topics', topic_n.most_common(), 'no title', no_title)
for k in topic_n:
    say('   ', k, examples[k][:2])

# ------------------------------------------------------------------ c03: from signature to the Gazzetta Ufficiale
lag = collections.defaultdict(list)
bad = 0
for a, v in VIG.items():
    if a not in ACTS:
        continue
    e, p = v['enacted'], v['pub']
    if not e or not p or p < '1861':
        bad += 1
        continue
    d = DAYS(e, p)
    if d < 0 or d > 3650:
        bad += 1
        continue
    g = GROUP[ACTS[a]['kind']]
    lag[(g, ACTS[a]['year'] // 10 * 10)].append(d)
cells = {f'{g}|{dec}': [len(v), med(v), round(sum(1 for x in v if x <= 1) / len(v), 3)] for (g, dec), v in lag.items()}
OUT['c03'] = {'cells': cells, 'bad': bad}
say('c03 cells', len(cells), 'left out', bad, {k: v for k, v in cells.items() if k.startswith(('legge', 'dpr', 'regi'))})

# ------------------------------------------------------------------ c04: from the Gazzetta to entry into force (acts with the Gazzetta's note)
EIV = re.compile(r'Entrata in vigore del(?:la| | l)?\s*(?:provvedimento|decreto|legge)?\s*:?\s*(\d{1,2})[/-](\d{1,2})[/-](\d{4})')
eiv_rows = collections.defaultdict(collections.Counter); eiv_n = 0
EIVK = [('conv', lambda a, t: ACTS[a]['kind'] == 'legge' and re.search(r'\bconversione in legge\b', t)),
        ('ratif', lambda a, t: ACTS[a]['kind'] == 'legge' and re.search(r'\b(ratifica|adesione)\b', t)),
        ('legge', lambda a, t: ACTS[a]['kind'] == 'legge'),
        ('dl', lambda a, t: ACTS[a]['kind'] == 'decreto-legge'),
        ('dlgs', lambda a, t: ACTS[a]['kind'] == 'decreto-legislativo'),
        ('dpr', lambda a, t: ACTS[a]['kind'] == 'dpr'),
        ('dm', lambda a, t: ACTS[a]['kind'] in ('decreto', 'dm', 'dpcm'))]
by_dec_law = collections.defaultdict(collections.Counter)
for a, h in HEADS.items():
    m = EIV.search(h)
    if not m or a not in VIG or a not in ACTS or ACTS[a]['year'] < 1988:
        continue
    try:
        e = datetime.date(int(m.group(3)), int(m.group(2)), int(m.group(1))).isoformat()
    except ValueError:
        continue
    p = VIG[a]['pub']
    if not p or p < '1861':
        continue
    g = DAYS(p, e)
    b = 'neg' if g < 0 else 'd0' if g == 0 else 'd1' if g == 1 else 'd2' if g <= 14 else 'd15' if g == 15 else 'late'
    t = head_title(a).lower()
    k = next((k for k, f in EIVK if f(a, t)), None)
    if not k:
        continue
    eiv_rows[k][b] += 1
    eiv_n += 1
    if k == 'legge':
        by_dec_law[(ACTS[a]['year'] - 1988) // 10][b] += 1
OUT['c04'] = {'rows': eiv_rows, 'n': eiv_n, 'law_dec': {str(k): v for k, v in by_dec_law.items()}}
say('c04', eiv_n, {k: dict(v) for k, v in eiv_rows.items()}, {k: dict(v) for k, v in by_dec_law.items()})

# ------------------------------------------------------------------ the laws (Camera dei deputati, schede/leggi)
LAWS = []
for r in tsv('log-leggi.tsv'):
    t = text(r[1])
    m = re.match(r'^(Legge(?: costituzionale)?) (\d+[°º]? \w+ \d{4}), n\. (\d+): (.*)$', t)
    if not m:
        continue
    pub = itdate(r[3])
    title = m.group(4)
    acs = re.findall(r'\(([0-9][0-9A-Z\-, e]*)\)\s*$', title)
    LAWS.append({'d': r[2], 'n': int(m.group(3)), 'cost': 'costituzionale' in m.group(1), 'title': title, 'pub': pub.isoformat() if pub else '', 'path': r[4]})
say('laws', len(LAWS), LAWS[0]['d'], LAWS[-1]['d'])
PF['laws'] = len(LAWS)
PF['laws_from'] = min(l['d'] for l in LAWS)
PF['laws_to'] = max(l['d'] for l in LAWS)


def strip_proposers(t):
    """the title without the names of the proposing members ("BURTONE ed altri; VENDOLA ed altri: ...")"""
    if ':' not in t[:400]:
        return t
    pre, rest = t.split(':', 1)
    p = re.sub(r'\b(ed|e) altr[ie]\b', ' ', pre)
    p = re.sub(r'(?i)\b(senat(ori|ore|rici|rice)|deputat[aoie])\b', ' ', p)
    if re.search(r'[A-Z]{3}', pre) and re.fullmatch(r"[A-ZÀ-ÖØ-Þ'’\.\s;,\-]*", p):
        return rest.strip()
    return t


def law_type(t):
    tl = strip_proposers(t).lower()
    if re.search(r"\bconversione in legge\b|\bconvalidazione del decreto", tl):
        return 'conv'
    if re.search(r"\b(ratifica|adesione)\b|\besecuzione (dell'|della |del |dello |dei |degli |delle )(accordo|accordi|convenzion|trattat|protocoll|scambi|atto)", tl):
        return 'ratif'
    if re.search(r"bilancio di previsione|stato di previsione|rendiconto generale|assestamento del bilancio|formazione del bilancio|legge finanziaria|legge di stabilit|esercizio provvisorio|nota di variazioni al bilancio|variazioni al bilancio", tl):
        return 'budget'
    if re.search(r"\bdelega al governo\b|\bdeleghe al governo\b|\bdelega legislativa\b|\bdeleghe legislative\b", tl):
        return 'delega'
    return 'other'


# the legislatures of the Republic: each starts on the first day on which ten or more Camera bills of it were presented
# (members present their bills on the first days); a few bills carry dates from an earlier legislature or a wrong year
bill_days = collections.defaultdict(collections.Counter)
for r in tsv('log-cambill.tsv'):
    m = re.search(r'\((\w+) legislatura della Repubblica\)', r[0])
    if m and r[2] and r[2] >= '1948':
        bill_days[m.group(1)][r[2]] += 1
LEGS, prev = [], '1948-01-01'
for k in ROM[:19]:
    cand = sorted(d for d, n in bill_days[k].items() if n >= 10 and d >= prev)
    LEGS.append((cand[0], ROM.index(k) + 1))
    prev = (D(cand[0]) + datetime.timedelta(days=365)).isoformat()
say('legislature starts', LEGS)
assert [x[0] for x in LEGS] == sorted(x[0] for x in LEGS), 'legislatures out of order'


def leg_of(d):
    n = None
    for s, k in LEGS:
        if d >= s:
            n = k
    return n


OUT['legs'] = [[k, s] for s, k in LEGS]

# ------------------------------------------------------------------ c09: what Parliament approves, by legislature
lt = collections.defaultdict(collections.Counter)
for l in LAWS:
    if l['cost']:
        continue
    k = leg_of(l['d'])
    if k:
        lt[k][law_type(l['title'])] += 1
OUT['c09'] = {'rows': [{'leg': k, **lt[k]} for k in sorted(lt)]}
say('c09', {k: dict(v) for k, v in sorted(lt.items())})
ex = collections.defaultdict(list)
for l in LAWS:
    t = law_type(l['title'])
    if len(ex[t]) < 3 and l['d'] > '2000':
        ex[t].append(l['title'][:100])
say('   examples', dict(ex))

# ------------------------------------------------------------------ c06 + c08: decree-laws converted (dates from the conversion laws' titles)
CONV = []
for l in LAWS:
    m = re.match(r'"?[Cc]onversione in legge(,? con modificazioni,?)? del decreto[- ]legge (\d{1,2}[°º]? \w+ \d{4}), n\. ?(\d+)', strip_proposers(l['title']))
    if not m:
        continue
    dl = itdate(m.group(2))
    if not dl:
        continue
    CONV.append({'law': l['d'], 'lawn': l['n'], 'dl': dl.isoformat(), 'dln': int(m.group(3)), 'mod': bool(m.group(1)), 'title': l['title'], 'days': DAYS(dl.isoformat(), l['d'])})
say('conversion laws with the decree-law date', len(CONV), 'of', sum(1 for l in LAWS if law_type(l['title']) == 'conv'))
hist = collections.Counter(c['days'] for c in CONV if 0 <= c['days'] <= 75)
per = collections.defaultdict(lambda: [0, 0, 0, []])
for c in CONV:
    k = c['law'][:3] + '0'
    per[k][0] += 1
    per[k][1] += c['mod']
    per[k][2] += c['days'] >= 51
    per[k][3].append(c['days'])
OUT['c06'] = {'hist': sorted(hist.items()), 'n': len(CONV), 'over': [[c['law'], c['dl'], c['days'], c['title'][:120]] for c in CONV if c['days'] > 75 or c['days'] < 0],
              'dec': {k: [v[0], v[1], v[2], med(v[3])] for k, v in sorted(per.items())}}
say('c06', len(CONV), 'last ten days', sum(1 for c in CONV if c['days'] >= 51), 'over 62', len(OUT['c06']['over']), {k: v[:3] for k, v in OUT['c06']['dec'].items()})

# the year-end "Milleproroghe": a decree-law of late November or December whose title is only about extending deadlines
MP = re.compile(r"recante (proroga di termini previsti da disposizioni legislative|proroga di termini\s*(\(|$)|proroghe e differimenti di termini|definizione e proroga di termini|proroga e definizione di termini|disposizioni urgenti in materia di (proroga di )?termini (legislativi|normativi))")
mille = []
for c in CONV:
    m = D(c['dl'])
    t = c['title'].replace('’', "'")
    if (m.month == 12 or (m.month == 11 and m.day >= 15)) and MP.search(t):
        mille.append({'dl': c['dl'], 'n': c['dln'], 'law': c['law'], 'lawn': c['lawn'], 'days': c['days'], 'mod': c['mod'],
                      'title': re.sub(r'\s*\([0-9][^)]*\)\s*$', '', re.sub(r'^.*?recante\s+', '', t))[:160]})
OUT['c08'] = {'rows': sorted(mille, key=lambda r: r['dl'])}
say('c08 milleproroghe', [(r['dl'], r['n'], r['law'], r['days'], r['mod']) for r in OUT['c08']['rows']])

# ------------------------------------------------------------------ c12: the calendar of the laws (day of signature)
md = collections.Counter(l['d'][5:] for l in LAWS if l['d'] >= '1948')
mon = collections.Counter(l['d'][5:7] for l in LAWS if l['d'] >= '1948')
wd = collections.Counter(D(l['d']).weekday() for l in LAWS if l['d'] >= '1948')
wdp = collections.Counter(D(l['pub']).weekday() for l in LAWS if l['d'] >= '1948' and l['pub'])
OUT['c12'] = {'md': md, 'mon': mon, 'wd': [wd[i] for i in range(7)], 'wdp': [wdp[i] for i in range(7)], 'n': sum(md.values()), 'y0': 1948, 'y1': int(PF['laws_to'][:4]),
              'top': md.most_common(12)}
say('c12', md.most_common(8), sorted(mon.items()), [wd[i] for i in range(7)], [wdp[i] for i in range(7)])

# ------------------------------------------------------------------ c13: the budget law and the esercizio provvisorio
fy_budget = {}             # financial year -> date of the budget law (the last of the year's estimates before 1965)
ep = collections.defaultdict(list)
for l in LAWS:
    t = l['title'].replace("l' anno", "l'anno")
    m = re.match(r"(?i)^bilancio di previsione dello stato per l'anno finanziario (\d{4})", t)
    if m:
        fy_budget.setdefault(int(m.group(1)), l['d'])
        continue
    m = re.match(r"(?i)^stato di previsione dell[a']\s*(?:entrata|spesa)\b.*?per l'(?:esercizio|anno) finanziario (?:dal 1 luglio )?(\d{4})(?:.*?al 30 giugno (\d{4}))?", t)
    if m and l['d'] < '1965':   # until 1964 the budget was one law per ministry: the year's budget is complete with the last of them
        fy = int(m.group(2)) - 1 if m.group(2) else int(m.group(1))   # the year it ends, less one (the 1956 Treasury title misprints 1950)
        if fy not in fy_budget or l['d'] > fy_budget[fy]:
            fy_budget[fy] = l['d']
        continue
    m = re.match(r"(?i)^bilancio di previsione dello stato per il periodo 1 luglio[ -]+31 dicembre (\d{4})", t)
    if m:   # the half year 1 July - 31 December 1964, which moved the financial year to the calendar year
        fy_budget.setdefault(int(m.group(1)), l['d'])
        continue
    m = re.search(r"(?i)esercizio provvisorio del bilancio (?:dello stato )?(?:per l'(?:anno|esercizio) finanziario|relativo all'anno finanziario|per l'anno finanziario dal 1 luglio)\s*(\d{4})", t)
    if m and l['d'] >= '1948':
        ep[int(m.group(1))].append([l['d'], 'proroga' if re.match(r'(?i)proroga', t) else 'aut'])
fy_rows = []
for y in range(1948, int(PF['laws_to'][:4]) + 1):
    start = f'{y}-07-01' if y < 1965 else f'{y}-01-01'
    b = fy_budget.get(y)
    fy_rows.append({'y': y, 'start': start, 'budget': b, 'days': DAYS(start, b) if b else None, 'ep': ep.get(y, [])})
OUT['c13'] = {'rows': fy_rows}
say('c13 years with ep', [y for y in sorted(ep)], 'budget laws found', len(fy_budget), 'missing', [r['y'] for r in fy_rows if not r['budget']])

# ------------------------------------------------------------------ c05: decree-laws presented to the Camera for conversion, 1915-2026
cb = []
CB = re.compile(r"^(?:[^\"]{0,80}?- )?\"?conversione in legge(?:,? con modificazioni,?| con modificazioni)?\s+(?:del|dello|dei|di|degli)\s+(?:regio\s+|r\.\s*)?"
                r"(?:decreto[- ]legge(?:\s+luogotenenziale)?|decreti[- ]legge|decreto\s+(?:legislativo\s+)?luogotenenziale|decreti\s+(?:legislativi\s+)?luogotenenziali|d\.\s*l\.|regi\s+decreti|decreto|decreti)"
                r"(?:\s+in\s+data)?\s*(\d{1,2}[°º]?\s+\w+\s+\d{4})?(?:-[IVXL]+)?,?\s*(?:n\.\s*(\d+))?,?\s*(.*)$", re.I)
for r in tsv('log-cambill.tsv'):
    t = text(r[1])
    m = CB.match(t)
    if not m or not r[2]:
        continue
    d = itdate(m.group(1)) if m.group(1) else None
    subj = re.sub(r'^(?:recante|concernente|riguardante|contenente|portante|relativo all[ae]?|relativo a|che (?:reca|contiene|modifica|autorizza|approva|proroga|stabilisce))\s+', '', m.group(3).lower())
    subj = re.sub(r'\(.*$', '', subj)
    subj = re.sub(r"[^a-zàèéìòù ]", ' ', subj)
    subj = ' '.join(subj.split()[:12])
    key = (d.isoformat(), m.group(2)) if d and m.group(2) else ('bill', r[3])   # one decree; or a bill naming several decrees
    cb.append((r[2], key, subj if d and m.group(2) else ''))
first = {}
cby = collections.defaultdict(lambda: [0, 0])
seen_dl = set()
for pres, key, subj in sorted(cb):
    if key in seen_dl:
        continue          # the same decree twice (a bill and its text from the Senate)
    seen_dl.add(key)
    y = int(pres[:4])
    rep = len(subj) >= 20 and subj in first and DAYS(first[subj], pres) <= 400
    cby[y][0] += 1
    cby[y][1] += rep
    first[subj] = pres
OUT['c05'] = {'rows': [{'y': y, 'n': v[0], 'rep': v[1]} for y, v in sorted(cby.items()) if y >= 1910]}
say('c05', [(y, v) for y, v in sorted(cby.items()) if y >= 1915 and (v[0] > 150 or y in (1996, 1997))])

# ------------------------------------------------------------------ Senate bills (13th-19th legislature): c07 and c10
SEN = list(dict_tsv('blob-senddl.tsv'))
PF['senate_phases'] = len(SEN)
PF['senate_to'] = max(r['Data di presentazione'] for r in SEN if r['Data di presentazione'])
GOVRE = re.compile(r'\(([A-Z][\w\' ]*-[IVX]+)\)')
gov_first = {}
for r in SEN:
    for g in GOVRE.findall(r['Iniziativa']):
        d = r['Data di presentazione']
        if d and (g not in gov_first or d < gov_first[g]):
            gov_first[g] = d
# the confidence motions of the Camera date each government's start (the motion or its first bill, whichever is earlier)
CV = list(dict_tsv('blob-camvote.tsv'))
PF['camera_votes'] = len(CV)
motions = sorted(r['date'] for r in CV if r['richiestaFiducia'] == '1' and r['type'] == 'Mozione' and r['approvato'] == '1' and re.search(r'(?i)mozion[ei] di fiducia', html.unescape(r['description'])))
motions = [f'{m[:4]}-{m[4:6]}-{m[6:]}' for m in motions]
say('investiture motions', motions)
GOVS = []
for g, d in sorted(gov_first.items(), key=lambda kv: kv[1]):
    if g == 'Berlusconi-III':
        continue          # only its last bills, of April 2006, are in the Senate's data
    mo = [m for m in motions if -60 <= DAYS(m, d) <= 60]
    GOVS.append([g, min([d] + mo)])
for i, g in enumerate(GOVS):
    g.append(GOVS[i + 1][1] if i + 1 < len(GOVS) else None)
say('governments', GOVS)
OUT['govs'] = GOVS


def gov_of(d):
    out = None
    for g, s, e in GOVS:
        if d >= s:
            out = g
    return out


# c07: decree-laws by government, and what became of them
dls = collections.defaultdict(list)
for r in SEN:
    if r['Natura'] != 'di conversione di decreto-legge':
        continue
    m = re.search(r"decreto[- ]legge,? (\d{1,2}[°º]? \w+ \d{4}), n\. ?(\d+)", r['title'])
    d = itdate(m.group(1)) if m else None
    if d:
        dls[(d.isoformat(), int(m.group(2)))].append(r)


def outcome(rs):
    st = ' | '.join(r['Stato'] for r in rs).lower()
    if any(r['Legge n.'] for r in rs) or re.search(r'definit\w*\.? legge|appr\. def', st):
        return 'conv'
    if 'decadut' in st:
        return 'lapsed'
    if 'respint' in st:
        return 'rejected'
    return 'other'


g7 = collections.defaultdict(collections.Counter)
dl_leg = collections.defaultdict(collections.Counter)
for (d, n), rs in dls.items():
    o = outcome(rs)
    dl_leg[rs[0]['path'].split('/')[3]][o] += 1
    g = gov_of(d)
    if g and d >= GOVS[0][1]:
        g7[g][o] += 1
OUT['c07'] = {'govs': [[g, s, e, dict(g7[g])] for g, s, e in GOVS], 'legs': {k: dict(v) for k, v in dl_leg.items()}, 'to': PF['senate_to']}
say('c07', [(g, dict(g7[g])) for g, s, e in GOVS], {k: dict(v) for k, v in dl_leg.items()})

# c10: bills by initiative, and which became law (one bill = one Senate "Id DDL", its phases in both chambers)
bills = collections.defaultdict(list)
for r in SEN:
    bills[(r['path'].split('/')[3], r['Id DDL'])].append(r)


def initiative(rs):
    for r in sorted(rs, key=lambda r: r['Data di presentazione'] or '9'):
        i = r['Iniziativa']
        if not i:
            continue
        if GOVRE.search(i) or re.match(r'(Gov\.|Pres\. Consiglio|Ministro)', i):
            return 'gov'
        if re.match(r'(Sen\.|Dep\.)', i):
            return 'mp'
        return 'other'
    return None


c10 = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0]))
noinit = 0
for (leg, idd), rs in bills.items():
    if int(leg) < 15:
        continue
    i = initiative(rs)
    if not i:
        noinit += 1
        continue
    nat = rs[0]['Natura']
    k = 'conv' if nat == 'di conversione di decreto-legge' else ('gov' if i == 'gov' else i)
    law = any(r['Legge n.'] for r in rs) or any(re.search(r'(?i)definit\w*\.? legge|appr\. def', r['Stato']) for r in rs)
    c10[leg][k][0] += 1
    c10[leg][k][1] += law
OUT['c10'] = {'rows': {leg: {k: v for k, v in c.items()} for leg, c in sorted(c10.items())}, 'noinit': noinit, 'to': PF['senate_to']}
say('c10', {leg: {k: v for k, v in c.items()} for leg, c in sorted(c10.items())}, 'no initiative', noinit)

# ------------------------------------------------------------------ c11: the questione di fiducia in the Camera
fid = []
for r in CV:
    if r['richiestaFiducia'] != '1':
        continue
    d = f"{r['date'][:4]}-{r['date'][4:6]}-{r['date'][6:]}"
    desc = text(r['description']).upper()
    if r['type'] in ('Mozione', 'Risoluzione') or 'MOZION' in desc:
        k = 'mot'
    elif r['type'] == 'Emendamento' or 'EMENDAMENTO' in desc:
        k = 'emend'
    elif 'CONVERSIONE' in desc:
        k = 'conv'
    else:
        k = 'other'
    leg = int(re.search(r'repubblica_(\d+)', r['path']).group(1))
    fid.append([d, k, leg, gov_of(d) if d >= GOVS[0][1] else None, int(r['favorevoli'] or 0), int(r['contrari'] or 0), text(r['description'])[:150]])
fid.sort()
fl = collections.Counter(re.search(r'repubblica_(\d+)', r['path']).group(1) for r in CV if r['richiestaFiducia'] == '1')
OUT['c11'] = {'votes': fid, 'by_leg_all': {re.search(r'repubblica_(\d+)', r['path']).group(1): 0 for r in CV}, 'flag_legs': fl,
              'leg_votes': collections.Counter(re.search(r'repubblica_(\d+)', r['path']).group(1) for r in CV), 'to': max(f"{r['date'][:4]}-{r['date'][4:6]}-{r['date'][6:]}" for r in CV)}
say('c11', len(fid), collections.Counter((r[3] or f'leg{r[2]}', r[1]) for r in fid))

# ------------------------------------------------------------------ c14: the Constitution, article by article
cfiles = {}
for line in open(os.path.join(B, 'blob-costituzione.jsonl'), encoding='utf-8'):
    j = json.loads(line)
    cfiles[j['p']] = j['t']
ch = collections.defaultdict(list)
for r in tsv('log-files.tsv'):
    h, an, inf, st, f = r
    f = re.sub(r'^normativa/', '', f)
    if f.startswith('costituzione/'):
        ch[f].append([inf, an, st])
arts = []
for p, t in sorted(cfiles.items()):
    m = re.match(r'costituzione/(?:allegati/)?(art|disposizione|disp)[-_]?(\w+)\.md$', p)
    if not re.search(r'/(art-\d+|allegati/.*)\.md$', p) or p.endswith('README.md'):
        continue
    hist = sorted(ch.get(p, []))
    mods = [h for h in hist if h[2] == 'M' and not h[1].startswith(('Costituzione', 'Errata', 'Avviso'))]   # corrections of misprints are not amendments
    rep = 2 if re.search(r'(?i)\(\(\s*articolo abrogat', t) else 1 if re.search(r'(?i)\(\(\s*(?:disposizione|comma|parole)?\s*abrogat', t) else 0
    arts.append({'p': p, 'mods': [[h[0], h[1]] for h in mods], 'rep': rep, 'words': len(re.sub(r'(?m)^#.*$', '', t).split())})
groups = []
for line in cfiles.get('costituzione/struttura.md', '').split('\n'):
    m = re.match(r'^- (.*?)\s*\(Art\. (\d+)\.\)', line)
    if m:
        groups.append([re.sub(r'^COSTITUZIONE DELLA REPUBBLICA ITALIANA\s*', '', m.group(1)).replace(' - - - -', '').strip(), int(m.group(2))])
OUT['c14'] = {'arts': arts, 'groups': groups}
say('c14 groups', groups)
say('c14 files', len(arts), 'changed', sum(1 for a in arts if a['mods']), 'repealed', [a['p'] for a in arts if a['rep']])
lcs = []
for r in NRM:
    if r[1].startswith('Legge costituzionale'):
        lcs.append([r[4], r[1], r[9][:300]])
OUT['c14']['laws'] = sorted(lcs)

# ------------------------------------------------------------------ c15 + c16: the four codes
CODES = {'regio-decreto/1942/262': 'cc', 'regio-decreto/1930/1398': 'cp', 'regio-decreto/1940/1443': 'cpc', 'dpr/1988/447': 'cpp'}
ver = collections.defaultdict(collections.Counter)
first_day = {}
CNAME = {'cc': 'Codice civile', 'cp': 'Codice penale', 'cpc': 'Codice di procedura civile', 'cpp': 'Codice di procedura penale'}
for r in NRM:
    for k, name in CNAME.items():
        if r[2].startswith(name + ' (') and (k not in first_day or r[4] < first_day[k]):
            first_day[k] = r[4]
for r in NRM:   # every version after the first, which is the code's original text
    for k, name in CNAME.items():
        if r[2].startswith(name + ' (') and r[4] != first_day[k]:
            ver[k][int(r[4][:4]) // 10 * 10] += 1
say('code first versions', first_day)
CODE_DIR = {'cc': 'allegati/codice-civile/', 'cp': 'allegati/codice-penale/', 'cpc': 'allegati/codice-di-procedura-civile/', 'cpp': ''}   # the code itself: not the approving decree, not the preliminary provisions
files_now = collections.defaultdict(set)
for r in tsv('tree-normativa.tsv'):
    if r[0] == 'F':
        for path, k in CODES.items():
            if r[1].startswith('normativa/' + path + '/'):
                rel = r[1][len('normativa/' + path) + 1:]
                if re.search(r'/art-[^/]+\.md$', '/' + rel) and rel.startswith(CODE_DIR[k]) and (k != 'cpp' or '/' not in rel):
                    files_now[k].add(rel)
hist = collections.defaultdict(lambda: collections.defaultdict(list))
for r in tsv('log-files.tsv'):
    h, an, inf, st, f = r
    f = re.sub(r'^normativa/', '', f)
    for path, k in CODES.items():
        if f.startswith(path + '/'):
            hist[k][f[len(path) + 1:]].append([inf, st, an])
c16 = {}
for k in CODES.values():
    days = sorted({x[0] for v in hist[k].values() for x in v})
    d0 = days[0] if days else None
    rows = []
    for f in sorted(files_now[k], key=lambda f: [int(x) if x.isdigit() else x for x in re.split(r'(\d+)', f)]):
        hs = sorted(hist[k].get(f, []))
        orig = bool(hs) and hs[0][0] == d0 and hs[0][1] == 'A'
        mods = sum(1 for x in hs if x[1] == 'M')
        name = re.sub(r'^.*/art-', '', f)[:-3]
        rows.append([name, 1 if orig else 0, mods])
    c16[k] = {'arts': rows, 'first': d0, 'versions': len(days)}
    say('c16', k, 'files', len(rows), 'original', sum(r[1] for r in rows), 'original never changed', sum(1 for r in rows if r[1] and not r[2]), 'first day', d0, 'versions', len(days))
OUT['c15'] = {'ver': {k: dict(v) for k, v in ver.items()}}
OUT['c16'] = c16
big = collections.defaultdict(collections.Counter)
for k in CODES.values():
    for f, hs in hist[k].items():
        for x in hs:
            if x[0] != c16[k]['first']:
                big[k][x[0]] += 1
OUT['c15']['big'] = {k: v.most_common(5) for k, v in big.items()}
say('c15', OUT['c15'])

# ------------------------------------------------------------------ c17 + c18: the Corte costituzionale
cc = []
for r in tsv('log-cc.tsv'):
    m = re.match(r'Corte costituzionale, (sentenza|ordinanza) (\d+)/(\d{4})', r[0])
    if m:
        cc.append({'t': m.group(1), 'n': int(m.group(2)), 'y': int(m.group(3)), 'dec': r[1], 'dep': r[2]})
yc = collections.defaultdict(collections.Counter)
lagy = collections.defaultdict(list)
for c in cc:
    yc[c['y']][c['t']] += 1
    if c['dec'] and c['dep']:
        lagy[c['y']].append(DAYS(c['dec'], c['dep']))
OUT['c17'] = {'rows': [{'y': y, 's': yc[y]['sentenza'], 'o': yc[y]['ordinanza'], 'lag': med(lagy[y])} for y in sorted(yc)], 'to': max(c['dep'] for c in cc)}
say('c17', len(cc), [(y, dict(yc[y])) for y in (1988, 2025)], {y: med(lagy[y]) for y in (2010, 2014, 2015, 2025)})
PF['cc'] = len(cc)
GJ = [('inc', r'IN VIA INCIDENTALE'), ('pri', r'IN VIA PRINCIPALE'), ('enti', r'CONFLITTO DI ATTRIBUZIONE TRA ENTI'), ('poteri', r'POTERI DELLO STATO'), ('ref', r'REFERENDUM')]
c18 = collections.defaultdict(collections.Counter)
for r in tsv('blob-cc.tsv'):
    y = int(r[0].split('/')[2])
    g = r[2].upper().replace("LEGITTIMITA'", 'LEGITTIMITÀ')
    k = 'other' if '+' in g else next((k for k, pat in GJ if re.search(pat, g)), 'other')
    c18[y][k] += 1
OUT['c18'] = {'years': {y: dict(v) for y, v in sorted(c18.items())}}
say('c18', {p: dict(sum((c18[y] for y in range(a, b + 1)), collections.Counter())) for p, (a, b) in {'1956-89': (1956, 1989), '1990-2001': (1990, 2001), '2002-11': (2002, 2011), '2012-26': (2012, 2026)}.items()})

# ------------------------------------------------------------------ c19: the administrative courts
ga_age = collections.defaultdict(collections.Counter)
ga_n = collections.Counter(); ga_types = collections.Counter(); ga_mon = collections.Counter(); ga_year = collections.Counter()
for r in tsv('log-ga.tsv'):
    m = re.match(r'^(.*?), (.*?) n\. (\d+)/(\d{4})$', r[0])
    if not m:
        continue
    seat, typ = m.group(1), m.group(2)
    ga_n[seat] += 1
    ga_types[typ] += 1
    ga_year[r[1][:4]] += 1
    if typ in ('sentenza', 'sentenza breve'):
        ga_mon[r[1][5:7]] += 1
        py = int(r[1][:4])
        ny = int(r[2][:4]) if len(r[2]) >= 9 and r[2][:4].isdigit() else None
        if ny and 1950 <= ny <= py and py <= 2025:
            a = py - ny
            ga_age[seat]['a0' if a == 0 else 'a1' if a == 1 else 'a2' if a <= 4 else 'a5' if a <= 9 else 'a10'] += 1
OUT['c19'] = {'age': ga_age, 'n': ga_n, 'types': ga_types, 'mon': ga_mon, 'years': ga_year}
PF['ga'] = sum(ga_n.values())
say('c19', len(ga_n), sum(ga_n.values()), sorted(ga_year.items()))

# ------------------------------------------------------------------ c20: EU directives and the national measures notified
NIMK = [('dlgs', r'^decreto legislativo|^d\.\s?lgs|^decreto legislativo'), ('dl', r'^decreto[- ]legge'), ('legge', r'^legge'), ('dpr', r'^decreto del presidente della repubblica|^d\.p\.r'),
        ('dpcm', r'^decreto del presidente del consiglio'), ('dm', r'^decreto (ministeriale|interministeriale|del ministr|dirigenziale)|^d\.m\.|^decreto del ministero')]
ATK = {'Decreto legislativo': 'dlgs', 'Legge': 'legge', 'Legge Comunitaria': 'legge', 'Legge comunitaria': 'legge', 'Decreto-Legge': 'dl', 'Decreto-legge': 'dl',
       'Decreto del Presidente della Repubblica': 'dpr', 'Decreto del presidente della Repubblica': 'dpr', 'Decreto ministeriale': 'dm', 'Decreto del Presidente del Consiglio dei Ministri': 'dpcm',
       'Administrative measures': 'adm', 'Misure amministrative': 'adm', 'administrative measures': 'adm', 'Decreto': 'dm'}   # a plain "Decreto" is a ministerial decree
nim = []
for r in tsv('log-nim.tsv'):
    title = r[0].split(': ', 1)[1] if ': ' in r[0] else r[0]
    tl = title.lower().strip()
    k = 'none' if re.search(r'(?i)not consider|non necessar|non considera', title) else (next((k for k, pat in NIMK if re.search(pat, tl)), None) or ATK.get(r[1], 'other'))
    dy = int(r[3][1:5]) if re.match(r'^3\d{4}L', r[3]) else None
    nim.append({'k': k, 'y': int(r[4][:4]), 'dir': dy, 'at': r[1]})
c20 = collections.defaultdict(collections.Counter)
c20lag = collections.defaultdict(list)
for x in nim:
    c20[x['y']][x['k']] += 1
    if x['dir'] and x['y'] >= x['dir']:
        c20lag[x['y']].append(x['y'] - x['dir'])
OUT['c20'] = {'years': {y: dict(v) for y, v in sorted(c20.items())}, 'lag': {y: [len(v), med(v)] for y, v in sorted(c20lag.items())}, 'n': len(nim)}
say('c20', collections.Counter(x['k'] for x in nim), {p: dict(sum((c20[y] for y in range(a, b + 1)), collections.Counter())) for p, (a, b) in {'-1989': (1958, 1989), '90s': (1990, 1999), '00s': (2000, 2009), '10s': (2010, 2019), '20s': (2020, 2026)}.items()})
PF['nim'] = len(nim)

# ------------------------------------------------------------------ profile
PF['built'] = datetime.date.today().isoformat()
PF['camera_bills'] = sum(1 for _ in tsv('log-cambill.tsv'))
PF['laws_records'] = len(LAWS)
OUT_ALL = {'charts': OUT, 'profile': PF}
json.dump(OUT_ALL, open(os.path.join(B, 'data.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'), default=lambda o: dict(o) if isinstance(o, collections.Counter) else str(o))
say('data.json', os.path.getsize(os.path.join(B, 'data.json')))
