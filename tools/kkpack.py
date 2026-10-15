#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026 Beibit Sakhanov
"""kkpack: status, check, sync, bump, build and fetch for the Joomla kk-KZ language pack.

  python3 tools/kkpack.py fetch 6.1.4                       # Joomla en-GB sources -> .cache/joomla-6.1.4
  python3 tools/kkpack.py status --en .cache/joomla-6.1.4   # coverage against the English original
  python3 tools/kkpack.py check  --en .cache/joomla-6.1.4   # syntax, keys, placeholders, markup
  python3 tools/kkpack.py sync   --en .cache/joomla-6.1.5 --write   # new keys come in English, obsolete keys go
  python3 tools/kkpack.py bump 6.1.5.1                      # versions in the XML manifests
  python3 tools/kkpack.py build                             # dist/*.zip + SHA256SUMS
  python3 tools/kkpack.py feed                              # updates/pkg_kk-KZ.xml for the update server
"""
import argparse, collections, hashlib, io, re, shutil, subprocess, sys, time, urllib.request, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLIENTS = collections.OrderedDict([
    ('administrator', ('administrator/language/kk-KZ', 'administrator/language/en-GB')),
    ('site',          ('language/kk-KZ',               'language/en-GB')),
    ('api',           ('api/language/kk-KZ',           'api/language/en-GB')),
    ('installation',  ('installation/language/kk-KZ',  'installation/language/en-GB')),
])
LINE = re.compile(r'^\s*([A-Za-z][^\s=]*)\s*=\s*"(.*?)"(\s*;.*)?$')
KAZ = 'ӘәҒғҚқҢңӨөҰұҮүҺһІі'
LETTER = '[А-Яа-яЁё' + KAZ + ']'
RUSSIAN = re.compile(r'(?<!%s)(для|или|при|что|если|это|как|его|их|все|всё|нет|будет|может|можно|только|также|после|перед|чтобы|где|когда|который|которые|ваш|ваши|вы|ещё|уже|без|через|между)(?!%s)' % (LETTER, LETTER), re.I)
PLACEHOLDER = re.compile(r'%(?:(\d+)\$)?[-+ 0#]*\d*(?:\.\d+)?[sdfuxXcbeEgGo]')
PHP_LINT = ('$bad=0;$n=0;foreach(new RecursiveIteratorIterator(new RecursiveDirectoryIterator($argv[1],FilesystemIterator::SKIP_DOTS)) as $f){'
            'if(substr((string)$f,-4)!==".ini")continue;set_error_handler(function($a,$s){throw new Exception($s);},E_WARNING);'
            'try{$n+=count(parse_ini_file((string)$f,false,INI_SCANNER_RAW));}catch(Exception $e){$bad++;echo $f.": ".$e->getMessage()."\\n";}restore_error_handler();}'
            'echo "php parse_ini_file: keys=$n errors=$bad\\n";exit($bad?1:0);')


def read_ini(path):
    """Returns (OrderedDict key -> raw value, [(line number, problem)])."""
    values, bad = collections.OrderedDict(), []
    for n, line in enumerate(path.read_text(encoding='utf-8-sig').replace('\r\n', '\n').split('\n'), 1):
        s = line.strip()
        if not s or s.startswith(';'):
            continue
        m = LINE.match(line)
        if not m:
            bad.append((n, 'unparsed line: ' + line[:60]))
        elif m.group(1) in values:
            bad.append((n, 'duplicate key ' + m.group(1)))
        else:
            values[m.group(1)] = m.group(2)
    return values, bad


def plain(s):
    return re.sub(r'<[^>]+>|%(?:\d+\$)?[-+ 0#]*\d*(?:\.\d+)?[sdfuxXcbeEgGo]|\{[^}]*\}|&#?\w+;|\\"|\\n', ' ', s)


def nargs(s):
    seq = top = 0
    for m in PLACEHOLDER.finditer(s):
        if m.group(1):
            top = max(top, int(m.group(1)))
        else:
            seq += 1
    return max(seq, top)


def hrefs(s):
    return {re.sub(r'^https?://(www\.)?', '', h).rstrip('/') for h in re.findall(r'href=\\?["\']([^"\'\\]+)', s)}


def check_value(key, en, kk):
    """Returns [(level, message)]: E breaks Joomla output, W is a markup or style difference."""
    out = []
    if nargs(kk) > nargs(en) and not re.search(r'_[01]$', key):
        out.append(('E', 'more printf arguments than the original (PHP 8 ArgumentCountError)'))
    if set(re.findall(r'\{[A-Za-z_]+\}', kk)) - set(re.findall(r'\{[A-Za-z_]+\}', en)):
        out.append(('E', 'variable not present in the original: %s' % sorted(set(re.findall(r'\{[A-Za-z_]+\}', kk)) - set(re.findall(r'\{[A-Za-z_]+\}', en)))))
    if '"' in kk.replace('\\"', ''):
        out.append(('E', 'unescaped double quote'))
    if kk.strip() == '' and en.strip() != '' and key != 'THOUSANDS_SEPARATOR':
        out.append(('E', 'empty value'))
    if kk.count('\\n') != en.count('\\n'):
        out.append(('W', 'different number of \\n'))
    tags = lambda s: collections.Counter(t.lower() for t in re.findall(r'</?([a-zA-Z0-9]+)', s))
    if tags(en) != tags(kk):
        out.append(('W', 'different inline HTML tags'))
    if hrefs(en) - hrefs(kk):
        out.append(('W', 'link lost: %s' % sorted(hrefs(en) - hrefs(kk))))
    text = plain(kk)
    if RUSSIAN.search(text):
        out.append(('W', 'Russian function word: %s' % RUSSIAN.search(text).group(0)))
    if re.search(r'\b(?=\w*[A-Za-z])(?=\w*%s)\w+' % LETTER, text):
        out.append(('W', 'mixed Latin/Cyrillic word'))
    return out


def load_keep():
    p = ROOT / 'docs' / 'keep-english.txt'
    return set(p.read_text(encoding='utf-8').split('\n')) - {''} if p.exists() else set()


def cmd_status(a):
    keep = load_keep()
    print('%-14s %6s %8s %9s %8s %9s' % ('client', 'files', 'keys', 'English', 'missing', 'obsolete'))
    tot = collections.Counter()
    for client, (kkd, end) in CLIENTS.items():
        row = collections.Counter()
        for p in sorted((ROOT / kkd).glob('*.ini')):
            kk, _ = read_ini(p)
            row['files'] += 1; row['keys'] += len(kk)
            ep = Path(a.en) / end / p.name if a.en else None
            if ep and ep.exists():
                en, _ = read_ini(ep)
                row['missing'] += sum(1 for k in en if k not in kk)
                row['obsolete'] += sum(1 for k in kk if k not in en)
                row['English'] += sum(1 for k, v in kk.items() if k in en and v == en[k] and re.search(r'[A-Za-z]{3,}', plain(v)) and v not in keep)
        if a.en:
            for ep in (Path(a.en) / end).glob('*.ini'):
                if not (ROOT / kkd / ep.name).exists():
                    row['missing'] += len(read_ini(ep)[0])
        print('%-14s %6d %8d %9d %8d %9d' % (client, row['files'], row['keys'], row['English'], row['missing'], row['obsolete']))
        tot.update(row)
    print('%-14s %6d %8d %9d %8d %9d' % ('total', tot['files'], tot['keys'], tot['English'], tot['missing'], tot['obsolete']))
    if a.en:
        done = tot['keys'] - tot['English']
        print('translated: %.1f%% (English left on purpose: %d distinct strings in docs/keep-english.txt)' % (100.0 * done / max(1, tot['keys']), len(keep)))


def cmd_check(a):
    errors = warns = 0
    notes = collections.Counter()
    for client, (kkd, end) in CLIENTS.items():
        for p in sorted((ROOT / kkd).glob('*.ini')):
            rel = p.relative_to(ROOT)
            kk, bad = read_ini(p)
            for n, msg in bad:
                print('E %s:%d: %s' % (rel, n, msg)); errors += 1
            if not a.en:
                continue
            ep = Path(a.en) / end / p.name
            if not ep.exists():
                print('W %s: file is not in the Joomla original' % rel); warns += 1; continue
            en, _ = read_ini(ep)
            for k in en:
                if k not in kk:
                    print('E %s: missing key %s' % (rel, k)); errors += 1
            for k in kk:
                if k not in en:
                    print('W %s: obsolete key %s' % (rel, k)); warns += 1
            for k, v in kk.items():
                if k in en:
                    for lvl, msg in check_value(k, en[k], v):
                        notes[msg.split(':')[0]] += 1
                        if lvl == 'E' or a.verbose:
                            print('%s %s %s: %s' % (lvl, rel, k, msg))
                        errors += lvl == 'E'; warns += lvl == 'W'
    if shutil.which('php') and not a.no_php:
        bad_php = 0
        for kkd, _ in CLIENTS.values():
            r = subprocess.run(['php', '-r', PHP_LINT, '--', str(ROOT / kkd)], capture_output=True, text=True)
            print(kkd + ': ' + r.stdout.strip())
            bad_php += r.returncode != 0
        errors += bad_php
    print('errors: %d, warnings: %d' % (errors, warns))
    if a.en and notes:
        print('warnings by kind: ' + ', '.join('%s: %d' % kv for kv in notes.most_common()))
    return 1 if errors else 0


def cmd_sync(a):
    todo = []
    for client, (kkd, end) in CLIENTS.items():
        ed, kd = Path(a.en) / end, ROOT / kkd
        kd.mkdir(parents=True, exist_ok=True)
        names = sorted(p.name for p in ed.glob('*.ini'))
        for name in names:
            kp = kd / name
            kk = read_ini(kp)[0] if kp.exists() else {}
            lines = []; seen = set()
            for line in (ed / name).read_text(encoding='utf-8-sig').replace('\r\n', '\n').split('\n'):
                m = LINE.match(line)
                if not m:
                    lines.append(line.rstrip()); continue
                key, ev, cm = m.group(1), m.group(2), m.group(3) or ''
                if key in seen:
                    continue  # the original repeats the key (Joomla ignores the repeat); keep one line
                seen.add(key)
                if key in kk:
                    v = kk[key]
                else:
                    v = ev; todo.append((client, name, key, ev))
                lines.append('%s="%s"%s' % (key, v, cm))
            text = '\n'.join(lines).rstrip('\n') + '\n'
            if a.write:
                kp.write_text(text, encoding='utf-8')
        for p in kd.glob('*.ini'):
            if p.name not in names:
                print('obsolete file (not in the original): %s' % p.relative_to(ROOT))
    out = ROOT / 'todo.tsv'
    out.write_text('client\tfile\tkey\ten\n' + ''.join('%s\t%s\t%s\t%s\n' % t for t in todo), encoding='utf-8')
    print('%d new or changed keys (English text inserted) -> %s%s' % (len(todo), out.name, '' if a.write else ' (dry run, use --write)'))


def cmd_bump(a):
    ver = a.version
    files = [ROOT / 'pkg_kk-KZ.xml'] + [ROOT / kkd / n for kkd, _ in CLIENTS.values() for n in ('install.xml', 'langmetadata.xml') if (ROOT / kkd / n).exists()]
    for p in files:
        t = p.read_text(encoding='utf-8')
        t = re.sub(r'<version>[^<]*</version>', '<version>%s</version>' % ver, t, count=1)
        t = re.sub(r'<creationDate>[^<]*</creationDate>', '<creationDate>%s</creationDate>' % time.strftime('%Y-%m'), t, count=1)
        p.write_text(t, encoding='utf-8')
    print('version %s written to %d manifests' % (ver, len(files)))


def pkg_version():
    return re.search(r'<version>([^<]+)</version>', (ROOT / 'pkg_kk-KZ.xml').read_text(encoding='utf-8')).group(1)


FEED = ROOT / 'updates' / 'pkg_kk-KZ.xml'
FEED_HEAD = '<?xml version="1.0" encoding="utf-8"?>\n<!-- Сервер обновлений казахского языкового пакета. Новую версию добавляйте сверху; targetplatform — версия Joomla, под которую собран перевод. -->\n<updates>\n'


def cmd_feed(a):
    """Write updates/pkg_kk-KZ.xml for the version in pkg_kk-KZ.xml; entries for other Joomla minor versions are kept."""
    ver = pkg_version(); joomla, rev = ver.rsplit('.', 1); minor = '.'.join(joomla.split('.')[:2]); tp = minor.replace('.', '\\.')
    block = (
        '    <update>\n'
        '        <name>Kazakh (kk-KZ) Language Pack</name>\n'
        '        <description>Қазақ тілінің пакеті — Joomla %(minor)s</description>\n'
        '        <element>pkg_kk-KZ</element>\n'
        '        <type>package</type>\n'
        '        <client>0</client>\n'
        '        <version>%(ver)s</version>\n'
        '        <infourl title="kk-KZ %(ver)s">https://github.com/bsakhanov/joomla-kk-KZ/releases/tag/%(ver)s</infourl>\n'
        '        <downloads>\n'
        '            <downloadurl type="full" format="zip">https://github.com/bsakhanov/joomla-kk-KZ/releases/download/%(ver)s/kk-KZ_joomla_lang_full_%(joomla)sv%(rev)s.zip</downloadurl>\n'
        '        </downloads>\n'
        '        <tags><tag>stable</tag></tags>\n'
        '        <maintainer>Beibit Sakhanov</maintainer>\n'
        '        <maintainerurl>https://webmarka.kz</maintainerurl>\n'
        '        <targetplatform name="joomla" version="%(tp)s"/>\n'
        '    </update>\n') % dict(minor=minor, ver=ver, joomla=joomla, rev=rev, tp=tp)
    old = FEED.read_text(encoding='utf-8') if FEED.exists() else ''
    keep = [b for b in re.findall(r'    <update>\n.*?    </update>\n', old, flags=re.S) if 'version="%s"/>' % tp not in b]
    FEED.parent.mkdir(exist_ok=True)
    FEED.write_text(FEED_HEAD + block + ''.join(keep) + '</updates>\n', encoding='utf-8')
    print('%s: %s (the archive %s must exist on the release before this file is pushed)' % (FEED.relative_to(ROOT), ver, 'kk-KZ_joomla_lang_full_%sv%s.zip' % (joomla, rev)))


def cmd_build(a):
    ver = pkg_version(); joomla, rev = ver.rsplit('.', 1)
    dist = ROOT / 'dist'; dist.mkdir(exist_ok=True)
    stamp = time.gmtime()[:6]
    sets = [('kk-KZ_joomla_lang_full_%sv%s.zip' % (joomla, rev), ['pkg_kk-KZ.xml', 'script.php', 'administrator', 'api', 'language']),
            ('kk-KZ_joomla_lang_root_%sv%s.zip' % (joomla, rev), ['administrator', 'api', 'language', 'installation'])]
    sums = []
    for name, parts in sets:
        target = dist / name
        with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as z:
            for part in parts:
                base = ROOT / part
                for p in ([base] if base.is_file() else sorted(base.rglob('*'))):
                    if p.is_file():
                        zi = zipfile.ZipInfo(p.relative_to(ROOT).as_posix(), date_time=stamp)
                        zi.compress_type = zipfile.ZIP_DEFLATED; zi.external_attr = 0o644 << 16
                        z.writestr(zi, p.read_bytes())
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        sums.append('%s  %s' % (digest, name)); print('%s  %d bytes' % (name, target.stat().st_size))
    (dist / 'SHA256SUMS').write_text('\n'.join(sums) + '\n', encoding='utf-8')


def cmd_fetch(a):
    v = a.version
    url = a.url or 'https://github.com/joomla/joomla-cms/releases/download/%s/Joomla_%s-Stable-Full_Package.zip' % (v, v)
    print('downloading %s' % url)
    zf = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(url).read()))
    dest = ROOT / '.cache' / ('joomla-' + v)
    wanted = tuple(end + '/' for _, end in CLIENTS.values())
    for n in zf.namelist():
        if n.startswith(wanted) and not n.endswith('/'):
            t = dest / n; t.parent.mkdir(parents=True, exist_ok=True); t.write_bytes(zf.read(n))
    print(dest)


OVERRIDES = ROOT / 'docs' / 'overrides.tsv'
GUARD = ROOT / 'docs' / 'glossary-guard.txt'
CYR_ANY = re.compile('[А-Яа-яЁё' + KAZ + ']')


def load_overrides():
    """docs/overrides.tsv: client/file/KEY <TAB> value <TAB> reason. These values always win over the official translation."""
    out = {}
    if OVERRIDES.exists():
        for line in OVERRIDES.read_text(encoding='utf-8').split('\n'):
            if line.strip() and not line.startswith('#'):
                parts = line.split('\t')
                if len(parts) >= 2:
                    out[parts[0]] = parts[1]
    return out


def load_guard():
    """docs/glossary-guard.txt: one regular expression per line; an official string that matches is not adopted."""
    pats = []
    if GUARD.exists():
        for line in GUARD.read_text(encoding='utf-8').split('\n'):
            line = re.sub(r'\s+#.*$', '', line).strip()
            if line and not line.startswith('#'):
                pats.append(re.compile(line))
    return pats


def defects(en, v):
    n = 0
    tags = lambda s: collections.Counter(t.lower() for t in re.findall(r'</?([a-zA-Z0-9]+)', s))
    if tags(en) != tags(v):
        n += 1
    if hrefs(en) - hrefs(v):
        n += 2
    if en.count('\\n') != v.count('\\n'):
        n += 1
    return n


def official_ok(key, en, off, guard):
    """Returns (value, reason). value is None when the official string must not be adopted."""
    v = off.replace('"_QQ_"', '\\"').replace('_QQ_', '\\"')
    if not v.strip():
        return None, 'empty'
    if v == en:
        return None, 'English'
    if not CYR_ANY.search(v):
        return None, 'no Cyrillic'
    if re.fullmatch(r'«[^«»]*»', v) and not re.search(r'["«&]|\\"', en):
        v = v[1:-1]
    errs = [m for lvl, m in check_value(key, en, v) if lvl == 'E']
    if errs:
        return None, 'defect: ' + errs[0][:34]
    if re.search(r'\\n;|\b[A-Z][A-Z0-9_]{5,}=\\?"', v):
        return None, 'corrupted value'
    text = plain(v)
    if RUSSIAN.search(text):
        return None, 'Russian word'
    if re.search(r'\b(?=\w*[A-Za-z])(?=\w*%s)\w+' % LETTER, text):
        return None, 'mixed script'
    if len(en.split()) <= 5 and len(v) > 3 * len(en) + 15:
        return None, 'wrong context (too long)'
    for g in guard:
        if g.search(v):
            return None, 'glossary'
    return v, 'ok'


def load_adopt():
    """docs/adopt-official.txt: file<TAB>KEY, the strings whose value is taken from the official translation."""
    out = set()
    f = ROOT / 'docs' / 'adopt-official.txt'
    if f.exists():
        for line in f.read_text(encoding='utf-8').split('\n'):
            if line.strip() and not line.startswith('#') and '\t' in line:
                a, b = line.split('\t')[:2]
                out.add((a, b))
    return out


def cmd_official(a):
    """Mode 'list' (default): take the official value only for the strings in docs/adopt-official.txt.
    Mode 'all': take it wherever it passes the checks and the glossary guard. docs/overrides.tsv always wins.
    --diff writes a review table of short labels, --defects writes the official strings that fail the checks."""
    overrides, guard, adopt = load_overrides(), load_guard(), load_adopt()
    choices = {}
    if a.apply:
        for line in Path(a.apply).read_text(encoding='utf-8').split('\n')[1:]:
            parts = line.split('\t')
            if len(parts) >= 6 and parts[5].strip():
                choices[(parts[0], parts[1])] = parts[5].strip()
    stats = collections.Counter(); changed = []; diff = {}; defects_rows = {}
    dirs = {'administrator': a.official, 'site': a.official, 'api': a.official, 'installation': a.official_installer}
    new_overrides = []
    for client, (kkd, end) in CLIENTS.items():
        base = dirs.get(client)
        if not base:
            continue
        offdir = Path(base) / kkd if client != 'installation' else Path(base)
        for p in sorted((ROOT / kkd).glob('*.ini')):
            ep = Path(a.en) / end / p.name
            if not ep.exists():
                continue
            en, _ = read_ini(ep); cur, _ = read_ini(p)
            off = read_ini(offdir / p.name)[0] if (offdir / p.name).exists() else {}
            new = collections.OrderedDict()
            for key, ev in en.items():
                c = cur.get(key, ev); ov = overrides.get('%s/%s/%s' % (client, p.name, key))
                cand = cand_ng = None
                if key in off:
                    cand_ng, reason_ng = official_ok(key, ev, off[key], [])
                    cand, reason = (cand_ng, reason_ng) if (p.name, key) in adopt else official_ok(key, ev, off[key], guard)
                    if cand_ng is None and off[key].strip() and CYR_ANY.search(off[key]) and reason_ng not in ('English', 'no Cyrillic'):
                        defects_rows.setdefault((p.name, key), (reason_ng, off[key]))
                ch = choices.get((p.name, key))
                if ch is not None:
                    if ch == 'ours':
                        n, why = c, 'review: ours'
                    elif ch == 'official' and cand_ng is not None:
                        n, why = cand_ng, 'review: official'
                    elif ch not in ('official', 'ours'):
                        n, why = ch, 'review: custom'; new_overrides.append('%s/%s/%s\t%s\treview' % (client, p.name, key, ch))
                    else:
                        n, why = c, 'review: official rejected by checks'
                elif ov is not None:
                    n, why = ov, 'override'
                elif key not in off:
                    n, why = c, 'not in official'
                elif a.mode == 'list' and (p.name, key) not in adopt:
                    n, why = c, 'not adopted'
                elif cand is None:
                    n, why = c, 'kept'
                elif cand == c:
                    n, why = c, 'same'
                elif a.mode == 'all' and defects(ev, cand) > defects(ev, c) and CYR_ANY.search(c) and c != ev:
                    n, why = c, 'kept: markup'
                else:
                    n, why = cand, 'official'
                stats[why] += 1
                if n != c:
                    changed.append((client, p.name, key, why, ev, c, n))
                if cand_ng is not None and cand_ng != c and len(ev.split()) <= 5 and not re.search(r'[<%{]', ev):
                    diff.setdefault((p.name, key), (ev, c, cand_ng, '' if cand is not None else 'contested term (glossary guard)'))
                new[key] = n
            if a.write:
                lines = p.read_text(encoding='utf-8').split('\n')
                for i, line in enumerate(lines):
                    m = LINE.match(line)
                    if m and m.group(1) in new:
                        lines[i] = '%s="%s"%s' % (m.group(1), new[m.group(1)], m.group(3) or '')
                p.write_text('\n'.join(lines), encoding='utf-8')
    if a.write and new_overrides:
        with OVERRIDES.open('a', encoding='utf-8') as f:
            f.write('\n'.join(sorted(set(new_overrides))) + '\n')
    for k, v in sorted(stats.items(), key=lambda kv: -kv[1]):
        print('%-40s %6d' % (k, v))
    if a.diff:
        Path(a.diff).write_text('file\tkey\ten\tthis pack\tofficial\tchoice (official / ours / your own text)\tnote\n' + ''.join('%s\t%s\t%s\t%s\t%s\t\t%s\n' % (f, k, e, o, c, n) for (f, k), (e, o, c, n) in sorted(diff.items())), encoding='utf-8')
        print('review table: %d strings -> %s' % (len(diff), a.diff))
    if a.defects:
        Path(a.defects).write_text('file\tkey\tdefect\tofficial value\n' + ''.join('%s\t%s\t%s\t%s\n' % (f, k, r, v[:200].replace('\t', ' ')) for (f, k), (r, v) in sorted(defects_rows.items())), encoding='utf-8')
        print('official strings that fail the checks: %d -> %s' % (len(defects_rows), a.defects))
    print('%d strings change%s' % (len(changed), '' if a.write else ' (dry run, use --write)'))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest='cmd', required=True)
    for name, fn in (('status', cmd_status), ('check', cmd_check), ('sync', cmd_sync)):
        p = sp.add_parser(name); p.set_defaults(fn=fn); p.add_argument('--en', help='Joomla tree with the en-GB language folders')
        if name == 'check': p.add_argument('-v', '--verbose', action='store_true'); p.add_argument('--no-php', action='store_true')
        if name == 'sync': p.add_argument('--write', action='store_true'); p.set_defaults(en=None)
    p = sp.add_parser('official', help='adopt strings of the official translation (joomla/core-translations)')
    p.add_argument('--en', required=True); p.add_argument('--official', required=True, help='.../joomla_v6/translations/package/kk-KZ')
    p.add_argument('--official-installer', help='.../joomla_v6/translations/core/installation/language/kk-KZ')
    p.add_argument('--mode', choices=['list', 'all'], default='list'); p.add_argument('--write', action='store_true')
    p.add_argument('--apply', help='review table with the choice column filled in'); p.add_argument('--diff', help='write the review table'); p.add_argument('--defects', help='write the official strings that fail the checks')
    p.set_defaults(fn=cmd_official)
    p = sp.add_parser('bump'); p.add_argument('version'); p.set_defaults(fn=cmd_bump)
    p = sp.add_parser('build'); p.set_defaults(fn=cmd_build)
    p = sp.add_parser('feed', help='write updates/pkg_kk-KZ.xml for the current version'); p.set_defaults(fn=cmd_feed)
    p = sp.add_parser('fetch'); p.add_argument('version'); p.add_argument('--url'); p.set_defaults(fn=cmd_fetch)
    a = ap.parse_args()
    if a.cmd == 'sync' and not a.en:
        ap.error('sync needs --en')
    sys.exit(a.fn(a) or 0)


if __name__ == '__main__':
    main()
