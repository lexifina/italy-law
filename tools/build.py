"""Builds a git repository of Italian law from Normattiva Open Data (dati.normattiva.it), in which every amending act is
one commit, dated the day it took effect.

    python -X utf8 scripts/italy-law/build.py [--repo ../italy-law] [--today 2026-10-28] [--offline] [--verify-rebuild]

Normattiva Open Data (Istituto Poligrafico e Zecca dello Stato, for the Presidenza del Consiglio dei Ministri and AgID)
exports acts "in multivigenza": one Akoma Ntoso file per version of the act, each named by the day it applies from
("..._VIGENZA_2022-03-09_V25.xml"), plus the same versions as JSON. The JSON of each version records, for every article,
the provisions of other acts that produced its current wording ("articoliAggiornanti") and the day that wording applies
from; its "storia" lists every act in the act's update history. We compare consecutive versions provision by provision
and credit each change to the act that Normattiva's per-article record names. A change no record explains is never
credited to an act: it gets its own commit by the publisher, labelled.

Sources are fetched through the documented Open Data API (no scraping): the async export ("ricerca-asincrona") for single
acts and the prepared collection download for the constitutional laws. Everything is cached in .cache/ (self-gitignored).
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import time
import zipfile
from multiprocessing import Pool
from pathlib import Path

from lxml import etree

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CACHE = HERE / '.cache'
ZIPS = CACHE / 'zips'
API = 'https://api.normattiva.it/t/normattiva.api/bff-opendata/v1/api/v1'
UA = 'Lexifina-gitlaw/1.0 (+https://lexifina.com; legal research)'
COMMITTER = ('Lexifina', 'italy-law@lexifina.com')
PUBLISHER = ('Normattiva (IPZS)', 'redazione@normattiva.invalid')
NS = '{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}'

# The data: one async export per act (AKN and JSON), and the prepared collection of constitutional laws.
def _q(den, num=None, year=None):
    p = {'denominazioneAtto': den, 'titoloContainsType': 'ALL_WORDS', 'testoContainsType': 'ALL_WORDS',
         'limitaAnniVigenza': False}
    if num:
        p['numeroProvvedimento'] = str(num)
        p['annoProvvedimento'] = year
    return p


SOURCES = [
    {'id': 'costituzione', 'kind': 'async', 'params': _q('COSTITUZIONE')},
    {'id': 'legge-300-1970', 'kind': 'async', 'params': _q('LEGGE', 300, 1970)},
    {'id': 'legge-241-1990', 'kind': 'async', 'params': _q('LEGGE', 241, 1990)},
    {'id': 'dlgs-196-2003', 'kind': 'async', 'params': _q('DECRETO LEGISLATIVO', 196, 2003)},
    {'id': 'dlgs-82-2005', 'kind': 'async', 'params': _q('DECRETO LEGISLATIVO', 82, 2005)},
    {'id': 'leggi-costituzionali', 'kind': 'collection', 'nome': 'Leggi costituzionali'},
]

REQUESTS: list[dict] = []


# ---------------------------------------------------------------- fetching (the documented Open Data API)

def curl(args: list[str]) -> tuple[int, dict, bytes]:
    """One HTTP request with curl (gzip, a timeout, our User-Agent). Returns status, headers and body."""
    out = subprocess.run(['curl', '-sS', '--compressed', '--max-time', '600', '-A', UA, '-D', '-', *args],
                         capture_output=True)
    if out.returncode:
        raise RuntimeError(f'curl {args}: {out.stderr.decode(errors="replace")}')
    raw = out.stdout
    status, headers = 0, {}
    while raw.startswith(b'HTTP/'):
        head, _, raw = raw.partition(b'\r\n\r\n')
        lines = head.decode('latin-1').split('\r\n')
        status = int(lines[0].split()[1])
        headers = {l.split(':', 1)[0].lower(): l.split(':', 1)[1].strip() for l in lines[1:] if ':' in l}
    return status, headers, raw


def fetch_zip(src: dict, fmt: str, offline: bool) -> Path:
    """The export of one source in one format (AKN or JSON), from the cache or the API."""
    name = src['id'] + ('' if fmt == 'AKN' else '-json')
    path = ZIPS / f'{name}.zip'
    REQUESTS.append({'source': src['id'], 'format': fmt, 'file': path})
    if path.exists():
        return path
    if offline:
        raise SystemExit(f'not cached: {path.name}')
    ZIPS.mkdir(parents=True, exist_ok=True)
    (CACHE / '.gitignore').write_text('*\n')
    meta = {'request': {}}
    if src['kind'] == 'collection':
        q = f'nome={src["nome"].replace(" ", "%20")}&formato={fmt}&formatoRichiesta=M'
        url = f'{API}/collections/download/collection-preconfezionata?{q}'
        status, _, body = curl(['-L', url])
        meta['request'] = {'GET': url}
    else:
        body_json = {'formato': fmt, 'tipoRicerca': 'A', 'richiestaExport': 'M', 'parametriRicerca': src['params']}
        status, _, token = curl(['-H', 'Content-Type: application/json', '-X', 'POST', '--data',
                                 json.dumps(body_json), f'{API}/ricerca-asincrona/nuova-ricerca'])
        token = token.decode().strip()
        if status not in (200, 202) or not re.fullmatch(r'[0-9a-f-]{36}', token):
            raise SystemExit(f'nuova-ricerca {src["id"]}: {status} {token[:200]}')
        meta['request'] = {'POST': f'{API}/ricerca-asincrona/nuova-ricerca', 'body': body_json}
        meta['token'] = token
        deadline = time.monotonic() + 3600
        while True:
            status, headers, st = curl([f'{API}/ricerca-asincrona/check-status/{token}'])
            state = json.loads(st or b'{}').get('stato')
            if state == 0:
                curl(['-H', 'Content-Type: application/json', '-X', 'PUT', '--data', json.dumps({'token': token}),
                      f'{API}/ricerca-asincrona/conferma-ricerca'])
            elif state == 3 or status == 303:
                break
            elif state in (4, 5):
                raise SystemExit(f'export {src["id"]} {fmt}: {st[:300]}')
            if time.monotonic() > deadline:
                raise SystemExit(f'export {src["id"]} {fmt}: still waiting after an hour')
            time.sleep(10)
        status, _, body = curl(['-L', f'{API}/collections/download/collection-asincrona/{token}'])
    if status != 200 or not body.startswith(b'PK'):
        raise SystemExit(f'download {src["id"]} {fmt}: HTTP {status}')
    path.write_bytes(body)
    meta.update({'retrieved': dt.date.today().isoformat(), 'sha256': hashlib.sha256(body).hexdigest(), 'bytes': len(body)})
    path.with_suffix('.json').write_text(json.dumps(meta, indent=1) + '\n')
    return path


# ---------------------------------------------------------------- reading one version (Akoma Ntoso)

BLOCK = {'paragraph', 'subparagraph', 'list', 'point', 'intro', 'wrapUp', 'content', 'p', 'heading', 'subheading',
         'alinea', 'citation', 'citations', 'formula', 'blockList', 'item', 'listIntroduction', 'listWrapUp', 'tblock',
         'table', 'tr', 'td', 'th', 'docType', 'docDate', 'docNumber', 'docTitle', 'authorialNote', 'longTitle',
         'blockContainer', 'signature', 'container', 'mainBody', 'preface', 'preamble', 'conclusions', 'num', 'br',
         'eol', 'section', 'chapter', 'part', 'title', 'book', 'article', 'division', 'clause', 'hcontainer'}
QUOTED = {'quotedStructure', 'quotedText', 'mod', 'embeddedStructure'}
GLUED_NUM_PARENTS = {'paragraph', 'subparagraph', 'point', 'item', 'alinea', 'list', 'clause'}
SPACE = re.compile(r'[ \t\r\f\v  -   　]+')
INVISIBLE = re.compile('[­​‌‍⁠﻿]')
BREAK = '\x00'


def _local(tag) -> str:
    return tag.split('}', 1)[1] if isinstance(tag, str) and '}' in tag else (tag if isinstance(tag, str) else '')


def render_lines(el) -> list[str]:
    """The text of an element, one line per block (paragraph, point, line of a paragraph). Structure inside quoted text
    (an amending provision quoting another act) is not split into blocks."""
    out: list[str] = []
    glue = [False]

    def brk():
        if glue[0]:
            glue[0] = False
            out.append(' ')
        else:
            out.append(BREAK)

    def walk(e, quoted: bool):
        name = _local(e.tag)
        if not name:          # comments, processing instructions
            if e.tail:
                out.append(e.tail)
            return
        q = quoted or name in QUOTED
        block = name in BLOCK and not quoted
        if block:
            brk()
        if e.text:
            out.append(e.text)
        for c in e:
            walk(c, q)
        if block:
            if name == 'num' and _local(e.getparent().tag) in GLUED_NUM_PARENTS:
                glue[0] = True      # "1." or "a)" stays on the line of its text
            else:
                brk()
        if e.tail:
            out.append(e.tail)

    walk(el, False)
    text = INVISIBLE.sub('', ''.join(out)).replace('\n', BREAK)
    lines = [SPACE.sub(' ', l).strip() for l in text.split(BREAK)]
    return [l for l in lines if l]


def unit_text(lines: list[str]) -> str:
    return '\n\n'.join(lines) + '\n' if lines else ''


def slug(s: str, n: int = 90) -> str:
    s = s.lower()
    for a, b in (('à', 'a'), ('è', 'e'), ('é', 'e'), ('ì', 'i'), ('ò', 'o'), ('ù', 'u')):
        s = s.replace(a, b)
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s[:n].rstrip('-')


def art_path(eid: str) -> str:
    """art_2-quater -> art-002-quater.md; art_1 -> art-001.md (other eIds are kept as they are)."""
    m = re.fullmatch(r'art_(\d+)(.*)', eid)
    if m:
        return f'art-{int(m.group(1)):03d}{slug(m.group(2)) and "-" + slug(m.group(2))}.md'
    return f'{slug(eid)}.md'


def doc_path(name: str) -> str:
    """An annex: 'Allegato A.3 Codice ...-art. 4 bis' -> allegati/allegato-a-3-codice-.../art-004-bis.md."""
    m = re.fullmatch(r'(.*?)\s*-\s*art\.?\s*(\d+)\s*(.*)', name, re.I)
    if m:
        rest = slug(m.group(3))
        return f'allegati/{slug(m.group(1), 80)}/art-{int(m.group(2)):03d}{"-" + rest if rest else ""}.md'
    return f'allegati/{slug(name, 120)}.md'


def norm_key(s: str) -> str:
    return re.sub(r'[^a-z0-9]', '', s.lower())


def read_version(args) -> dict:
    """Parse one version: its units (preface, preamble, each article, conclusions, each annex), the structure headings,
    the act's lifecycle events, and (from the JSON of the same version) each article's amending acts."""
    zpath, member, jzpath, jmember = args
    with zipfile.ZipFile(zpath) as z:
        raw = z.read(member)
    root = etree.fromstring(raw)
    act = root.find(f'{NS}act')
    meta = act.find(f'{NS}meta')
    expr = meta.find(f'.//{NS}FRBRExpression/{NS}FRBRdate')
    eli = meta.find(f'.//{NS}FRBRWork/{NS}FRBRalias[@name="eli"]')
    refs = {p.get('eId'): p.get('href') or '' for p in meta.iter(f'{NS}passiveRef')}
    refs.update({p.get('eId'): p.get('href') or '' for p in meta.iter(f'{NS}original')})
    events = sorted({(e.get('date'), refs.get(e.get('source'), '')) for e in meta.iter(f'{NS}eventRef')})
    units: dict[str, dict] = {}
    order: list[str] = []
    paths: set[str] = set()

    def add(key, path, label, lines):
        if not lines:
            return
        if key in units:            # a duplicate identifier in the source: keep both
            i = 2
            while f'{key}~{i}' in units:
                i += 1
            key = f'{key}~{i}'
        base, i = path[:-3], 2
        while path in paths:
            path, i = f'{base}-{i}.md', i + 1
        paths.add(path)
        units[key] = {'key': key, 'path': path, 'label': label, 'text': unit_text(lines)}
        order.append(key)

    pre = act.find(f'{NS}preface')
    if pre is not None:
        add('intestazione', 'intestazione.md', 'Intestazione', render_lines(pre))
    pa = act.find(f'{NS}preamble')
    if pa is not None:
        add('preambolo', 'preambolo.md', 'Preambolo', render_lines(pa))
    body = act.find(f'{NS}body')
    structure = []
    if body is not None:
        def walk(e, depth):
            for c in e:
                name = _local(c.tag)
                if name == 'article':
                    num = c.find(f'{NS}num')
                    lab = SPACE.sub(' ', ''.join(num.itertext())).strip().rstrip('.') if num is not None else c.get('eId')
                    add('art:' + (c.get('eId') or lab), art_path(c.get('eId') or slug(lab)), lab, render_lines(c))
                elif name in ('chapter', 'part', 'title', 'book', 'section', 'division', 'subsection', 'hcontainer'):
                    num, head = c.find(f'{NS}num'), c.find(f'{NS}heading')
                    t = ' '.join(x for x in (SPACE.sub(' ', ''.join(n.itertext())).strip() if n is not None else ''
                                             for n in (num, head)) if x and x != '-')
                    first = c.find(f'.//{NS}article/{NS}num')
                    fl = SPACE.sub(' ', ''.join(first.itertext())).strip() if first is not None else ''
                    structure.append('  ' * depth + f'- {t}' + (f' ({fl})' if fl else ''))
                    walk(c, depth + 1)
                elif name in ('num', 'heading'):
                    continue
                else:
                    lines = render_lines(c)
                    if lines:
                        add(f'blk:{name}:{c.get("eId") or len(order)}', f'{slug(name)}-{len(order):03d}.md', name, lines)
        walk(body, 0)
    if structure:
        units['struttura'] = {'key': 'struttura', 'path': 'struttura.md', 'label': 'Struttura',
                              'text': unit_text([INVISIBLE.sub('', SPACE.sub(' ', s)) for s in structure])}
        order.append('struttura')
    co = act.find(f'{NS}conclusions')
    if co is not None:
        add('conclusioni', 'conclusioni.md', 'Conclusioni', render_lines(co))
    for doc in act.iter(f'{NS}doc'):
        name = doc.get('name') or 'allegato'
        mb = doc.find(f'{NS}mainBody')
        if mb is not None:
            add('doc:' + name, doc_path(name), name, render_lines(mb))
    amenders: dict[str, dict] = {}
    storia = []
    codes: dict[str, tuple] = {}
    if jzpath:
        with zipfile.ZipFile(jzpath) as z:
            j = json.loads(z.read(jmember))
        storia = [{k: e.get(k) for k in ('versione', 'dataPubblicazione', 'tipodoc', 'numdoc', 'datadoc')}
                  for e in ((j.get('metadati') or {}).get('storia') or {}).get('elementi') or []]

        def jw(e):
            for x in (e or {}).get('elementi') or []:
                yield x
                yield from jw(x)
        for x in list(jw(j.get('articolato'))) + list(jw(j.get('annessi'))):
            if not x.get('nomeNir'):
                continue
            k = ('art:art_' if x['nomeNir'] == 'articolo' else 'doc:') + (x.get('numNir') or '')
            starts = sorted({v.get('inizioVigore') for v in x.get('dataVigoreVersione') or [] if v.get('inizioVigore')})
            amenders[norm_key(k)] = {
                'from': starts[-1] if starts else None,
                'by': sorted({(a.get('dataPubblicazioneGazzetta') or '', a.get('codiceRedazionale') or '')
                              for a in x.get('articoliAggiornanti') or []}),
                'notes': [a.get('testo') or '' for a in x.get('articoliAggiornanti') or []]}
        # codice redazionale of each amending act -> its URN (type, date, number), from the act's update list
        for a in (j.get('metadati') or {}).get('aggiornamentiAtto') or []:
            for u in a.get('urnModifiche') or []:
                cr = (u.get('articoloAggiornante') or {}).get('codiceRedazionale')
                m = re.match(r'urn:nir:[^:]+:([^:]+):([^;#]+)(?:;([^#]*))?', u.get('urnModificante') or '')
                if cr and m:
                    codes[cr] = (m.group(1), m.group(2), (m.group(3) or '').strip())
    return {'member': member, 'sha256': hashlib.sha256(raw).hexdigest(), 'expr': expr.get('date') if expr is not None else None,
            'eli': eli.get('value') if eli is not None else None, 'events': events, 'units': units, 'order': order,
            'amenders': amenders, 'storia': storia, 'codes': codes}


# ---------------------------------------------------------------- acts and their labels

TYPE = {  # source name -> (label, slug for paths and emails, URN type)
    'COSTITUZIONE': ('Costituzione', 'costituzione', 'costituzione'),
    'LEGGE': ('Legge', 'legge', 'legge'),
    'LEGGE COSTITUZIONALE': ('Legge costituzionale', 'legge-costituzionale', 'legge.costituzionale'),
    'DECRETO-LEGGE': ('D.L.', 'decreto-legge', 'decreto.legge'),
    'DECRETO LEGISLATIVO': ('D.Lgs.', 'decreto-legislativo', 'decreto.legislativo'),
    'DECRETO DEL PRESIDENTE DELLA REPUBBLICA': ('D.P.R.', 'dpr', 'decreto.del.presidente.della.repubblica'),
    'DECRETO DEL PRESIDENTE DEL CONSIGLIO DEI MINISTRI': ('D.P.C.M.', 'dpcm', 'decreto.del.presidente.del.consiglio.dei.ministri'),
    'DECRETO': ('Decreto', 'decreto', 'decreto'),
    'DECRETO MINISTERIALE': ('D.M.', 'dm', 'decreto.ministeriale'),
    'CIRCOLARE': ('Circolare', 'circolare', 'circolare'),
    'REGIO DECRETO': ('R.D.', 'regio-decreto', 'regio.decreto'),
    'REGIO DECRETO-LEGGE': ('R.D.L.', 'regio-decreto-legge', 'regio.decreto.legge'),
    'DECRETO LEGISLATIVO LUOGOTENENZIALE': ('D.Lgs.Lgt.', 'dlgslgt', 'decreto.legislativo.luogotenenziale'),
}
NOT_ACTS = {'ERRATA-CORRIGE': 'Errata corrige', 'AVVISO DI RETTIFICA': 'Avviso di rettifica', 'COMUNICATO': 'Comunicato'}
MESI = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre',
        'novembre', 'dicembre']


def long_it(day: str) -> str:
    y, m, d = (int(x) for x in day.split('-'))
    return f'{d} {MESI[m - 1]} {y}'


def gu_iso(s: str) -> str:
    """'22/02/2022' -> '2022-02-22'."""
    d, m, y = s.split('/')
    return f'{y}-{m}-{d}'


def law_of(e: dict) -> dict:
    """An entry of Normattiva's update history ('storia') as an author: label, email, citation, link."""
    t, num, dd, gu = (e.get('tipodoc') or '').strip(), (e.get('numdoc') or '').strip(), e.get('datadoc') or '', e['dataPubblicazione']
    good_date = bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}', dd)) and not dd.startswith('0000')
    if t in NOT_ACTS:
        lab = f'{NOT_ACTS[t]} (G.U. {long_it(gu)})'
        return {'key': f'{t}|{gu}', 'label': lab, 'email': f'{slug(t)}-{gu}@gazzettaufficiale.invalid', 'kind': 'correction',
                'type': t, 'num': '', 'date': '', 'gu': gu, 'cite': lab, 'url': None}
    if t == 'SENTENZA':
        year = dd[:4] if good_date else gu[:4]
        return {'key': f'{t}|{dd}|{num}|{gu}', 'label': f'Corte costituzionale, sentenza {num}/{year}', 'kind': 'judgment',
                'email': f'sentenza-{year}-{num}@cortecostituzionale.invalid', 'type': t, 'num': num,
                'date': dd if good_date else '', 'gu': gu,
                'cite': f'Corte costituzionale, sentenza {long_it(dd) + ", " if good_date else ""}n. {num} (G.U. {long_it(gu)})',
                'url': f'https://www.cortecostituzionale.it/actionSchedaPronuncia.do?param_ecli=ECLI:IT:COST:{year}:{num}'}
    if t == 'COSTITUZIONE':
        return {'key': 'COSTITUZIONE', 'label': 'Costituzione della Repubblica Italiana', 'kind': 'act', 'type': t,
                'email': 'costituzione-1947@normattiva.invalid', 'num': '', 'date': '1947-12-22', 'gu': gu,
                'cite': 'Costituzione della Repubblica Italiana (G.U. 27 dicembre 1947, n. 298)',
                'url': 'https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:costituzione'}
    lab_t, slug_t, urn_t = TYPE.get(t, (t.capitalize(), slug(t), t.lower().replace(' ', '.').replace('-', '.')))
    year = dd[:4] if good_date else gu[:4]
    if num:
        label = f'{lab_t} {num}/{year}'
        email = f'{slug_t}-{year}-{num}@normattiva.invalid'
    else:
        label = f'{lab_t} {long_it(dd)} (G.U. {long_it(gu)})' if good_date else f'{lab_t} (G.U. {long_it(gu)})'
        email = f'{slug_t}-{dd if good_date else gu}@normattiva.invalid'
    cite = f'{t.capitalize() if t not in TYPE else t[0] + t[1:].lower()} {long_it(dd) if good_date else ""}'.strip()
    cite += f', n. {num}' if num else ''
    cite += f' (G.U. {long_it(gu)})'
    url = (f'https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:{urn_t}:{dd}' + (f';{num}' if num else '')) if good_date else None
    return {'key': f'{t}|{dd}|{num}|{gu}', 'label': label, 'email': email, 'kind': 'act', 'type': t, 'num': num,
            'date': dd if good_date else '', 'gu': gu, 'cite': cite, 'url': url}


# ---------------------------------------------------------------- one act: versions, changes, causes

def plain(text: str) -> str:
    """Text with Normattiva's update marks (( )) and spacing removed, for telling editorial changes from real ones."""
    return ' '.join(text.replace('((', ' ').replace('))', ' ').split()).casefold()


def act_from_folder(folder: str, v0: dict) -> dict:
    m = re.fullmatch(r'(.+)_(\d{8}|0+)_(\w+)', folder)
    t, d, n = m.group(1), m.group(2), m.group(3)
    lab_t, slug_t, _ = TYPE.get(t, (t.capitalize(), slug(t), ''))
    if t == 'COSTITUZIONE':
        return {'type': t, 'path': 'costituzione', 'short': 'Costituzione', 'date': '1947-12-22', 'num': ''}
    day = f'{d[:4]}-{d[4:6]}-{d[6:]}'
    return {'type': t, 'path': f'{slug_t}/{d[:4]}/{n}', 'short': f'{lab_t} {n}/{d[:4]}', 'date': day, 'num': n}


def build_act(folder: str, versions: list[dict], today: str) -> dict:
    """Consecutive versions of one act -> the changes, grouped by the act that caused them."""
    act = act_from_folder(folder, versions[0])
    v0 = versions[0]
    v0['from'] = v0['expr'] or v0['events'][0][0]
    for v in versions[1:]:
        v['from'] = re.search(r'_VIGENZA_(\d{4}-\d{2}-\d{2})_V\d+', v['member']).group(1)
    # Several versions on one day: the later one wins (the source's own order).
    kept: list[dict] = []
    for v in versions:
        if kept and kept[-1]['from'] == v['from']:
            kept[-1] = v
        else:
            kept.append(v)
    versions = kept
    for a, b in zip(versions, versions[1:]):
        if b['from'] < a['from']:
            raise SystemExit(f'{folder}: versions out of order {a["member"]} {b["member"]}')
    storia = versions[-1]['storia']
    codes: dict[str, tuple] = {}
    for v in versions:
        codes.update(v['codes'])
    laws_by_gu: dict[str, list[dict]] = {}
    for e in storia:
        laws_by_gu.setdefault(e['dataPubblicazione'], []).append(law_of(e))
    self_law = law_of(storia[0]) if storia else None
    title = ''
    m = re.search(r'\n\n(.+?)\n$', v0['units'].get('intestazione', {}).get('text', ''), re.S)
    changes, problems = [], []
    for prev, cur in zip(versions, versions[1:]):
        new_gu = sorted({d for d, _ in cur['events']} - {d for d, _ in prev['events']})
        new_laws = [l for d in new_gu for l in laws_by_gu.get(d, [])]
        keys = [k for k in cur['order'] if k in cur['units']] + [k for k in prev['order'] if k not in cur['units']]
        changed = [k for k in keys if (prev['units'].get(k) or {}).get('text') != (cur['units'].get(k) or {}).get('text')]
        groups: dict[str, list[str]] = {}
        why: dict[str, str] = {}
        cands: dict[str, list[dict]] = {}
        maybe: dict[str, list[dict]] = {}
        laws: dict[str, dict] = {}
        for k in changed:
            a, c = (prev['units'].get(k) or {}).get('text', ''), (cur['units'].get(k) or {}).get('text', '')
            if a and c and plain(a) == plain(c):
                groups.setdefault('editorial', []).append(k)
                why[k] = 'editorial: only the update marks (( )), spacing or letter case changed'
                continue
            rec = cur['amenders'].get(norm_key(k)) if c else None
            named: list[dict] = []
            if rec and rec['from'] == cur['from']:
                in_cur = {d for d, _ in cur['events']}
                for gu, cr in rec['by']:
                    if not gu or gu_iso(gu) not in in_cur:
                        continue      # an act the version's own history does not list yet
                    same_day = laws_by_gu.get(gu_iso(gu), [])
                    if len(same_day) > 1 and cr in codes:
                        _t, d, n = codes[cr]
                        same_day = [l for l in same_day if l['date'] == d and l['num'] == n] or same_day
                    for l in same_day:
                        if l['key'] not in [x['key'] for x in named]:
                            named.append(l)
            pick, w = None, ''
            if len(named) == 1:
                pick, w = named[0], 'record'
            elif len(named) > 1:
                inter = [l for l in named if l['key'] in {x['key'] for x in new_laws}]
                if len(inter) == 1:
                    pick, w = inter[0], 'record+history'
                else:
                    cands[k] = inter or named
            elif len(new_laws) == 1 and not k.startswith('doc:'):
                # (annexes are never credited by date: codes of conduct and similar annexes take effect on dates the
                # update history does not record)
                pick, w = new_laws[0], 'history'
            elif len(new_laws) > 1:
                cands[k] = new_laws
            else:
                maybe[k] = new_laws
            if pick:
                laws[pick['key']] = pick
                groups.setdefault(pick['key'], []).append(k)
                why[k] = w
            elif k in cands:
                groups.setdefault('candidates', []).append(k)
                why[k] = 'two or more acts possible'
                problems.append(f'{cur["from"]} {k}: candidates {", ".join(l["label"] for l in cands[k])}')
            else:
                groups.setdefault('unexplained', []).append(k)
                why[k] = 'no act in the record or the update history'
                problems.append(f'{cur["from"]} {k}: unexplained')
        # Units without a per-article record (title, preamble, structure headings) in a version whose recorded changes
        # all come from one act: that act.
        recorded = {g for g in groups if g not in ('editorial', 'candidates', 'unexplained')
                    and any(why[k].startswith('record') for k in groups[g])}
        if len(recorded) == 1 and groups.get('unexplained'):
            g = recorded.pop()
            for k in [k for k in groups['unexplained'] if not k.startswith(('art:', 'doc:'))]:
                groups['unexplained'].remove(k)
                groups[g].append(k)
                why[k] = 'only act of this version'
                problems.remove(f'{cur["from"]} {k}: unexplained')
            if not groups['unexplained']:
                del groups['unexplained']
            groups[g].sort(key=lambda k: keys.index(k))
        changes.append({'from': cur['from'], 'prev': prev, 'cur': cur, 'groups': groups, 'why': why, 'cands': cands,
                        'maybe': maybe,
                        'laws': laws, 'new_laws': new_laws})
    return {'folder': folder, 'act': act, 'versions': versions, 'changes': changes, 'problems': problems,
            'self': self_law, 'storia': storia, 'laws_by_gu': laws_by_gu}


def load_all(offline: bool, today: str) -> list[dict]:
    tasks, where = [], []
    for src in SOURCES:
        zp, jp = fetch_zip(src, 'AKN', offline), fetch_zip(src, 'JSON', offline)
        with zipfile.ZipFile(zp) as z:
            members = [n for n in z.namelist() if n.endswith('.xml')]
        with zipfile.ZipFile(jp) as z:
            jmembers = {n[:-5]: n for n in z.namelist() if n.endswith('.json')}
        by_folder: dict[str, list[str]] = {}
        for n in members:
            by_folder.setdefault(n.split('/')[0], []).append(n)
        for folder in sorted(by_folder):
            ms = sorted(by_folder[folder], key=lambda n: int(re.search(r'_V(\d+)\.xml$', n).group(1)))
            for n in ms:
                tasks.append((str(zp), n, str(jp) if n[:-4] in jmembers else None, jmembers.get(n[:-4])))
                where.append((src['id'], folder))
    with Pool(min(8, os.cpu_count() or 2)) as pool:
        parsed = list(pool.imap(read_version, tasks, chunksize=4))
    groups: dict[tuple, list[dict]] = {}
    for w, p in zip(where, parsed):
        groups.setdefault(w, []).append(p)
    built = [build_act(folder, vs, today) for (sid, folder), vs in groups.items()]
    built.sort(key=lambda b: (b['act']['type'] != 'COSTITUZIONE', b['act']['path']))
    return built


# ---------------------------------------------------------------- the git repository

def last_sunday(year: int, month: int) -> dt.date:
    d = (dt.date(year, month + 1, 1) if month < 12 else dt.date(year + 1, 1, 1)) - dt.timedelta(days=1)
    return d - dt.timedelta(days=(d.weekday() + 1) % 7)


# Italian summer time 1970-1979 (Rome), first and last day of summer time (from the tz database's Italy rules);
# from 1980 the EU rules: from the first Sunday of April in 1980, the last Sunday of March from 1981, to the last Sunday
# of September until 1995 and of October since 1996.
SUMMER_1970S = {1970: ('1970-05-31', '1970-09-27'), 1971: ('1971-05-23', '1971-09-26'), 1972: ('1972-05-28', '1972-10-01'),
                1973: ('1973-06-03', '1973-09-30'), 1974: ('1974-05-26', '1974-09-29'), 1975: ('1975-06-01', '1975-09-28'),
                1976: ('1976-05-30', '1976-09-26'), 1977: ('1977-05-22', '1977-09-25'), 1978: ('1978-05-28', '1978-10-01'),
                1979: ('1979-05-27', '1979-09-30')}


def rome_offset(day: dt.date) -> int:
    """Hours ahead of UTC at noon in Rome. Summer time starts and ends in the night, so the test is start <= day < end."""
    if day.year in SUMMER_1970S:
        a, b = (dt.date.fromisoformat(x) for x in SUMMER_1970S[day.year])
    elif day.year == 1980:
        a, b = dt.date(1980, 4, 6), last_sunday(1980, 9)
    else:
        a, b = last_sunday(day.year, 3), last_sunday(day.year, 9 if day.year < 1996 else 10)
    return 2 if a <= day < b else 1


def commit_date(day: str, seq: list[int]) -> str:
    """Noon in Rome on the day. Git cannot record a time before 1970, so changes in force before then are dated
    1 January 1970 (UTC), one second apart in the order they took effect; the real day is in the In-force trailer."""
    d = dt.date.fromisoformat(day)
    if d.year < 1970:
        seq[0] += 1
        return f'@{seq[0]} +0000'
    off = rome_offset(d)
    stamp = int(dt.datetime(d.year, d.month, d.day, 12, tzinfo=dt.timezone(dt.timedelta(hours=off))).timestamp())
    return f'@{stamp} +0{off}00'


def git(repo: Path, *args: str, env: dict | None = None, input: str | bytes | None = None) -> str:
    out = subprocess.run(['git', *args], cwd=repo, capture_output=True, env=env,
                         input=input.encode() if isinstance(input, str) else input)
    if out.returncode:
        raise SystemExit(f'git {" ".join(args)} failed: {out.stderr.decode(errors="replace")}')
    return out.stdout.decode('utf-8')


PRE_1970 = ['Git non puo\' registrare date anteriori al 1970: il commit e\' datato 1 gennaio 1970 e il giorno di entrata',
            'in vigore e\' nel trailer In-force. (Git cannot record dates before 1970: the real day is In-force.)', '']


def unit_labels(b: dict, keys: list[str], ch: dict | None) -> list[str]:
    out = []
    for k in keys:
        u = (ch['cur']['units'].get(k) or ch['prev']['units'].get(k)) if ch else b['versions'][0]['units'][k]
        out.append(u['label'])
    return out


def plan(built: list[dict], today: str) -> list[dict]:
    """Every commit, in the order the changes took effect. One commit per amending act per day (across all the acts
    in the record), then on the same day the commits no act explains."""
    days: dict[str, dict] = {}
    for ai, b in enumerate(built):
        v0 = b['versions'][0]
        d = days.setdefault(v0['from'], {'start': [], 'law': {}, 'other': []})
        d['start'].append(b)
        for ch in b['changes']:
            d = days.setdefault(ch['from'], {'start': [], 'law': {}, 'other': []})
            for g, keys in ch['groups'].items():
                if g in ('editorial', 'candidates', 'unexplained'):
                    d['other'].append((g, b, ch, keys))
                else:
                    d['law'].setdefault(g, {'law': ch['laws'][g], 'parts': []})['parts'].append((b, ch, keys))
    out = []
    for day in sorted(days):
        d = days[day]
        starts = []
        for b in d['start']:
            # An act of the record that also amends another act of the record on the day it takes effect: one commit.
            if b['self'] and b['self']['key'] in d['law']:
                d['law'][b['self']['key']].setdefault('starts', []).append(b)
            else:
                starts.append(b)
        for b in starts:
            out.append({'day': day, 'kind': 'start', 'b': b})
        for key in sorted(d['law'], key=lambda k: (d['law'][k]['law']['gu'], d['law'][k]['law']['label'])):
            out.append({'day': day, 'kind': 'law', 'law': d['law'][key]['law'], 'parts': d['law'][key]['parts'],
                        'starts': d['law'][key].get('starts', [])})
        order = {'candidates': 0, 'unexplained': 1, 'editorial': 2}
        for g, b, ch, keys in sorted(d['other'], key=lambda x: (order[x[0]], built.index(x[1]))):
            out.append({'day': day, 'kind': g, 'b': b, 'ch': ch, 'keys': keys})
    return out


def describe_parts(parts) -> tuple[list[str], list[str], list[str]]:
    """Body lines, Affecting values and Evidence values for the units one act changed in one or more acts."""
    body, affecting, evidence = [], [], []
    for b, ch, keys in parts:
        short = b['act']['short']
        kinds: dict[str, list[str]] = {}
        for k in keys:
            p, c = ch['prev']['units'].get(k), ch['cur']['units'].get(k)
            kind = 'Inserito' if p is None else 'Rimosso' if c is None else 'Modificato'
            kinds.setdefault(kind, []).append((c or p)['label'])
        for kind in ('Inserito', 'Modificato', 'Rimosso'):
            if kind in kinds:
                body.append(f'{short}: {kind.lower()} {", ".join(kinds[kind])}')
        affecting.append(f'{short} ' + ', '.join(unit_labels(b, keys, ch)))
        whys = sorted({ch['why'][k] for k in keys})
        if 'history' in whys:
            evidence.append(f'{short}: by date only (the only new act in Normattiva\'s update history for this version)')
        if any(w.startswith('record') for w in whys):
            evidence.append(f'{short}: Normattiva per-article update record (articoliAggiornanti)')
    return body, affecting, evidence


def message(c: dict, built: list[dict]) -> tuple[tuple[str, str], list[str], list[str], list[tuple[dict, dict | None, list[str]]]]:
    """Author, message lines, trailers, and the files to write: (act, change or None for the first version, keys)."""
    day = c['day']
    trailers: list[str] = []
    if c['kind'] == 'start':
        b = c['b']
        v0 = b['versions'][0]
        law = b['self'] or {'label': b['act']['short'], 'email': f'{slug(b["act"]["short"])}@normattiva.invalid',
                            'cite': b['act']['short'], 'gu': '', 'url': None}
        author = (law['label'], law['email'])
        msg = [f'{law["label"]}: testo originario', '', law['cite'], '',
               f'Il testo dell\'atto come pubblicato, in vigore dal {long_it(day)} secondo Normattiva.',
               'The act as published, in force from this day according to Normattiva.', '']
        trailers += [f'Enacted: {b["act"]["date"]}'] if b['act']['date'] and b['act']['type'] != 'COSTITUZIONE' else []
        trailers += [f'Published: {law["gu"]} (Gazzetta Ufficiale)'] if law.get('gu') else []
        trailers += [f'In-force: {day}', f'Consolidated: https://www.normattiva.it/{v0["eli"]}' if v0['eli'] else '']
        trailers += [f'Source: {law["url"]}'] if law.get('url') else []
        files = [(b, None, list(v0['units']))]
    elif c['kind'] == 'law':
        law = c['law']
        author = (law['label'], law['email'])
        body, affecting, evidence = describe_parts(c['parts'])
        targets = ', '.join(b['act']['short'] for b, _, _ in c['parts'])
        subject = f'{law["label"]}: {targets}'
        n = sum(len(k) for _, _, k in c['parts'])
        if len(c['parts']) == 1 and n <= 3:
            subject = f'{law["label"]}: {targets} ' + ', '.join(unit_labels(c['parts'][0][0], c['parts'][0][2], c['parts'][0][1]))
        elif n > 1:
            subject = f'{law["label"]}: {targets}, {n} disposizioni'
        if len(subject) > 72:
            subject = f'{law["label"]}: {len(c["parts"])} atti, {n} disposizioni'
        if c['starts']:
            body += [f"Testo originario dell'atto: {b['act']['path']}/" for b in c['starts']]
        if law['kind'] == 'judgment':
            msg = [subject, '', law['cite'], '',
                   "Una sentenza della Corte costituzionale; Normattiva ne riporta l'effetto nel testo consolidato.",
                   'A judgment of the Constitutional Court; Normattiva records its effect in the consolidated text.', '']
        elif law['kind'] == 'correction':
            msg = [subject, '', law['cite'], '',
                   'Una correzione pubblicata in Gazzetta Ufficiale, non un atto che modifica la legge.',
                   'A correction published in the Gazzetta Ufficiale, not an amending act.', '']
        else:
            msg = [subject, '', law['cite'], '']
        msg += body + ['']
        if law.get('gu') and day < law['gu']:
            msg += [f'Nota: Normattiva fa decorrere questa versione dal {long_it(day)}, prima della pubblicazione',
                    f'dell\'atto ({long_it(law["gu"])}). Il giorno e\' riportato come lo da\' la fonte.',
                    'Note: the source dates this version before the act was published; the day is kept as given.', '']
            trailers += ['Date-note: in force before publication (retroactive, as recorded by Normattiva)']
        trailers += [f'Enacted: {law["date"]}'] if law.get('date') else []
        trailers += [f'Published: {law["gu"]} (Gazzetta Ufficiale)', f'In-force: {day}']
        trailers += [f'Affecting: {a}' for a in affecting] + [f'Evidence: {e}' for e in evidence]
        trailers += [f'Source: {law["url"]}'] if law.get('url') else []
        trailers += [f'Consolidated: https://www.normattiva.it/{ch["cur"]["eli"]}' for _, ch, _ in c['parts'] if ch['cur']['eli']]
        files = [(b, None, list(b['versions'][0]['units'])) for b in c['starts']]
        files += [(b, ch, keys) for b, ch, keys in c['parts']]
    else:
        b, ch, keys = c['b'], c['ch'], c['keys']
        author = PUBLISHER
        labels = unit_labels(b, keys, ch)
        short = b['act']['short']
        what = ', '.join(labels) if len(labels) <= 3 else f'{len(labels)} disposizioni'
        if c['kind'] == 'editorial':
            msg = [f'{short}: {what} (redazionale)', '',
                   'Normattiva ha cambiato solo la presentazione del testo (i segni (( )) che evidenziano le modifiche,',
                   'gli spazi o le maiuscole), senza cambiare le parole. Nessun atto e\' accreditato.',
                   'Normattiva changed only the presentation (the (( )) update marks, spacing or case); no act is credited.', '']
            trailers += ['Editorial: yes']
        elif c['kind'] == 'candidates':
            names = sorted({l['label'] for k in keys for l in ch['cands'][k]})
            msg = [f'{short}: {what} (atto non determinato)', '',
                   'Il testo e\' cambiato in questa versione e piu\' di un atto puo\' averlo causato; il commit non e\'',
                   'accreditato a nessuno di essi. Atti possibili: ' + '; '.join(names) + '.',
                   'More than one act could have made this change, so it is credited to none; the candidates are named.', '']
            trailers += [f'Candidate: {n}' for n in names]
        else:
            msg = [f'{short}: {what} (modifica senza atto)', '',
                   "Il testo consolidato di Normattiva e' cambiato in questo giorno, ma il registro degli aggiornamenti",
                   "dell'articolo non nomina un atto per questa modifica. Nessun atto e' accreditato.",
                   "Normattiva's text changed on this day but its per-article record names no act for it; no act is",
                   'credited.', '']
            names = sorted({l['label'] for k in keys for l in ch['maybe'].get(k, [])})
            if names:
                msg += ['Atto nuovo nella storia di questa versione, non confermato: ' + '; '.join(names) + '.',
                        "An act new in this version's update history, not confirmed as the cause, is named below.", '']
                trailers += [f'Candidate: {n}' for n in names]
        trailers += [f'In-force: {day}', f'Affecting: {short} ' + ', '.join(labels)]
        trailers += [f'Consolidated: https://www.normattiva.it/{ch["cur"]["eli"]}'] if ch['cur']['eli'] else []
        files = [(b, ch, keys)]
    if day < '1970-01-01':
        msg += PRE_1970
    return author, msg, [t for t in trailers if t], files


def write_repo(repo: Path, built: list[dict], docs: Path, today: str) -> tuple[list[dict], dict]:
    remote = None
    if (repo / '.git').exists():
        out = subprocess.run(['git', 'remote', 'get-url', 'origin'], cwd=repo, capture_output=True, text=True)
        remote = out.stdout.strip() or None
    elif repo.exists() and any(repo.iterdir()):
        raise SystemExit(f'{repo} is not empty and not a git repository; refusing to build into it')

    def force(fn, path, _exc):
        os.chmod(path, 0o700)
        fn(path)
    if repo.exists():
        for p in repo.iterdir():
            shutil.rmtree(p, onexc=force) if p.is_dir() else p.unlink()
    repo.mkdir(parents=True, exist_ok=True)
    git(repo, 'init', '-q', '-b', 'main')
    git(repo, 'config', 'core.autocrlf', 'false')
    git(repo, 'config', 'core.quotepath', 'false')
    if remote:
        git(repo, 'remote', 'add', 'origin', remote)

    # One fast-import stream: every commit writes its files as full blobs, so no working tree is touched.
    seq = [0]
    stream = io.BytesIO()
    marks = 0
    log, tags = [], {}
    future = False

    def data(b: bytes):
        stream.write(f'data {len(b)}\n'.encode() + b + b'\n')

    head_mark = None
    for c in plan(built, today):
        day = c['day']
        if day > today:
            future = True
            continue
        author, msg, trailers, files = message(c, built)
        when = commit_date(day, seq)
        marks += 1
        text = '\n'.join(msg).rstrip('\n') + '\n\n' + '\n'.join(trailers) + '\n'
        stream.write(b'commit refs/heads/main\n' + f'mark :{marks}\n'.encode())
        stream.write(f'author {author[0]} <{author[1]}> {when.lstrip("@")}\n'.encode())
        stream.write(f'committer {COMMITTER[0]} <{COMMITTER[1]}> {when.lstrip("@")}\n'.encode())
        data(text.encode('utf-8'))
        if head_mark:
            stream.write(f'from :{head_mark}\n'.encode())
        n = 0
        for b, ch, keys in files:
            units = b['versions'][0]['units'] if ch is None else ch['cur']['units']
            prev_units = {} if ch is None else ch['prev']['units']
            for k in keys:
                u = units.get(k)
                old = prev_units.get(k)
                if u is None:
                    stream.write(f'D {b["act"]["path"]}/{old["path"]}\n'.encode())
                else:
                    if old is not None and old['path'] != u['path']:
                        stream.write(f'D {b["act"]["path"]}/{old["path"]}\n'.encode())
                    stream.write(f'M 100644 inline {b["act"]["path"]}/{u["path"]}\n'.encode())
                    data(u['text'].encode('utf-8'))
                n += 1
        stream.write(b'\n')
        head_mark = marks
        for b, ch, keys in files:
            tags[f'{b["act"]["path"]}/{day}'] = marks
        if c['kind'] == 'law':
            tags.setdefault('atto/' + c['law']['email'].split('@')[0], marks)
        elif c['kind'] == 'start' and c['b']['self']:
            tags.setdefault('atto/' + c['b']['self']['email'].split('@')[0], marks)
        log.append({'day': day, 'kind': c['kind'], 'author': author[0], 'units': n, 'clamped': day < '1970-01-01',
                    'mark': marks})
    for name, mark in tags.items():
        stream.write(f'reset refs/tags/{name}\nfrom :{mark}\n\n'.encode())
    out = subprocess.run(['git', 'fast-import', '--quiet', '--date-format=raw', f'--export-marks={repo / ".git" / "marks"}'],
                         cwd=repo, input=stream.getvalue(), capture_output=True)
    if out.returncode:
        raise SystemExit(f'fast-import: {out.stderr.decode(errors="replace")}')
    mk = dict(l.split(' ') for l in (repo / '.git' / 'marks').read_text().split('\n') if l)
    (repo / '.git' / 'marks').unlink()
    for e in log:
        e['commit'] = mk[f':{e["mark"]}']
    tag_hashes = {n: mk[f':{m}'] for n, m in tags.items()}
    git(repo, 'checkout', '-q', '-f', 'main')

    # Documentation, tables, tools and the record of how it was made come last, by Lexifina, dated by the data's
    # retrieval day, so the same data gives the same hashes on any later day.
    for p in sorted(docs.rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts:
            dest = repo / p.relative_to(docs)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(p.read_bytes())
    (repo / 'tools').mkdir(exist_ok=True)
    for name in ('build.py', 'reproduce.py', 'check_repo.py', 'test_repo.py'):
        (repo / 'tools' / name).write_bytes((HERE / name).read_bytes())
    write_tables(repo, built, today)
    sys.path.insert(0, str(HERE))
    from reproduce import write_manifest, write_reproduce
    write_manifest(repo, built, today)
    write_reproduce(repo, built, log, tag_hashes, REQUESTS, today, future)
    git(repo, 'add', '-A')
    when = commit_date(today, seq)
    env = {**os.environ, 'GIT_AUTHOR_NAME': COMMITTER[0], 'GIT_AUTHOR_EMAIL': COMMITTER[1], 'GIT_AUTHOR_DATE': when,
           'GIT_COMMITTER_NAME': COMMITTER[0], 'GIT_COMMITTER_EMAIL': COMMITTER[1], 'GIT_COMMITTER_DATE': when}
    git(repo, 'commit', '-q', '-m', 'Documentazione, tabelle, strumenti e REPRODUCE.md (documentation, tables, tools)', env=env)
    return log, tag_hashes


def write_tables(repo: Path, built: list[dict], today: str):
    """atti.csv: every act the record credits, with the provisions it changed; and a README per act."""
    rows = []
    for b in built:
        if b['self']:
            rows.append({'atto': b['self']['label'], 'citazione': b['self']['cite'], 'pubblicato': b['self']['gu'],
                         'in_vigore': b['versions'][0]['from'], 'modifica': b['act']['short'], 'disposizioni': len(b['versions'][0]['units']),
                         'tipo': 'testo originario', 'fonte': b['self'].get('url') or ''})
        for ch in b['changes']:
            for g, keys in ch['groups'].items():
                if g in ('editorial', 'candidates', 'unexplained'):
                    rows.append({'atto': PUBLISHER[0], 'citazione': '', 'pubblicato': '', 'in_vigore': ch['from'],
                                 'modifica': b['act']['short'], 'disposizioni': len(keys),
                                 'tipo': {'editorial': 'redazionale', 'candidates': 'atto non determinato',
                                          'unexplained': 'senza atto'}[g], 'fonte': ''})
                else:
                    l = ch['laws'][g]
                    rows.append({'atto': l['label'], 'citazione': l['cite'], 'pubblicato': l['gu'], 'in_vigore': ch['from'],
                                 'modifica': b['act']['short'], 'disposizioni': len(keys),
                                 'tipo': 'correzione' if l['kind'] == 'correction' else 'modifica', 'fonte': l.get('url') or ''})
    rows = [r for r in rows if r['in_vigore'] <= today]
    rows.sort(key=lambda r: (r['in_vigore'], r['modifica'], r['atto']))
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(rows[0]), lineterminator='\n')
    w.writeheader()
    w.writerows(rows)
    (repo / 'atti.csv').write_text(buf.getvalue(), encoding='utf-8', newline='\n')
    for b in built:
        vs = [v for v in b['versions'] if v['from'] <= today]
        last = vs[-1]
        counts: dict[str, int] = {}
        lastday: dict[str, str] = {}
        for ch in b['changes']:
            if ch['from'] > today:
                continue
            for keys in ch['groups'].values():
                for k in keys:
                    counts[k] = counts.get(k, 0) + 1
                    lastday[k] = ch['from']
        head = b['self']['cite'] if b['self'] else b['act']['short']
        out = [f'# {b["act"]["short"]}', '', head, '',
               f'{len(vs)} versioni in Normattiva, dal {vs[0]["from"]} al {last["from"]} (ultima versione).', '',
               '| Disposizione | File | Modifiche | Ultima modifica |', '| --- | --- | ---: | --- |']
        for k in last['order']:
            u = last['units'][k]
            out.append(f'| {u["label"]} | [{u["path"]}]({u["path"]}) | {counts.get(k, 0)} | {lastday.get(k, "")} |')
        (repo / b['act']['path'] / 'README.md').write_text('\n'.join(out) + '\n', encoding='utf-8', newline='\n')


# ---------------------------------------------------------------- main

def data_day() -> str:
    """The day the cached data was retrieved (the newest download), so a rebuild on any later day gives the same hashes."""
    days = [json.loads(p.read_text())['retrieved'] for p in ZIPS.glob('*.json')] if ZIPS.exists() else []
    return max(days) if days else dt.date.today().isoformat()


def hashes(r: str) -> tuple[list[str], dict]:
    log = git(Path(r), 'log', '--format=%H', 'main').split()
    tags = dict(l.split(' ', 1)[::-1] for l in git(Path(r), 'show-ref', '--tags').split('\n') if l)
    return log, tags


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', default=str(ROOT.parent / 'italy-law'))
    ap.add_argument('--offline', action='store_true', help='read only the cache; fail on anything not cached')
    ap.add_argument('--today', default=None, help='the build day (default: the day the cached data was retrieved)')
    ap.add_argument('--verify-rebuild', action='store_true',
                    help='build again from the cache into a temporary folder and compare every hash with --repo')
    args = ap.parse_args()
    if args.verify_rebuild:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out = subprocess.run([sys.executable, '-X', 'utf8', str(HERE / 'build.py'), '--offline', '--repo', tmp]
                                 + (['--today', args.today] if args.today else []), capture_output=True, text=True)
            if out.returncode:
                raise SystemExit(out.stderr)
            a, b = hashes(args.repo), hashes(tmp)
            rec = {'identical': a[0][1:] == b[0][1:] and a[1] == b[1], 'history_tip': a[0][1], 'commits': len(a[0]) - 1,
                   'tags': len(a[1]), 'main_identical': a[0][0] == b[0][0], 'main': a[0][0], 'rebuilt_main': b[0][0]}
            print(json.dumps(rec, indent=1))
            p = HERE / 'verification.json'
            ver = json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
            ver['rebuild'] = {k: rec[k] for k in ('identical', 'history_tip', 'commits', 'tags')}
            p.write_text(json.dumps(ver, indent=1, sort_keys=True) + '\n', encoding='utf-8', newline='\n')
            for f in Path(tmp).rglob('*'):
                os.chmod(f, 0o700)
            raise SystemExit(0 if rec['identical'] else 1)
    today = args.today or data_day()
    t0 = time.monotonic()
    built = load_all(args.offline, today)
    for b in built:
        n = sum(len(ks) for ch in b['changes'] for ks in ch['groups'].values())
        kinds: dict[str, int] = {}
        for ch in b['changes']:
            for k, w in ch['why'].items():
                kinds[w.split(':')[0]] = kinds.get(w.split(':')[0], 0) + 1
        print(f'{b["act"]["path"]}: {len(b["versions"])} versions {b["versions"][0]["from"]}..{b["versions"][-1]["from"]}, '
              f'{n} unit changes {dict(sorted(kinds.items()))}')
        for p in b['problems']:
            print('   ', p)
    log, tags = write_repo(Path(args.repo), built, HERE / 'repo', today)
    print(f'repo: {len(log)} commits + 1 documentation commit, {len(tags)} tags -> {args.repo} '
          f'({time.monotonic() - t0:.0f}s)')


if __name__ == '__main__':
    main()
