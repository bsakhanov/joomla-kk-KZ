#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026 Beibit Sakhanov
"""Smoke test of the language pack on a running Joomla.

Logs in to the administrator, opens 82 screens (80 must answer 200, two are expected error pages) and reports PHP errors,
raw language keys and unexpected HTTP statuses. Install the pack and make it the default language first, see docs/MAINTAINING.md.

  python3 tools/smoke_crawl.py --base http://127.0.0.1:8099 --user admin --password 'a-long-password-12345'
"""
import argparse, html, http.cookiejar, re, sys, urllib.error, urllib.parse, urllib.request

A = '/administrator/index.php?option='
PAGES = [
    ('dashboard', '/administrator/index.php'),
    ('dashboard content', A + 'com_cpanel&view=cpanel&dashboard=content'), ('dashboard users', A + 'com_cpanel&view=cpanel&dashboard=users'),
    ('dashboard system', A + 'com_cpanel&view=cpanel&dashboard=system'), ('dashboard menus', A + 'com_cpanel&view=cpanel&dashboard=menus'),
    ('dashboard components', A + 'com_cpanel&view=cpanel&dashboard=components'), ('dashboard help', A + 'com_cpanel&view=cpanel&dashboard=help'),
    ('articles', A + 'com_content&view=articles'), ('article add', A + 'com_content&task=article.add'), ('featured', A + 'com_content&view=featured'),
    ('categories', A + 'com_categories&view=categories&extension=com_content'),
    ('users', A + 'com_users&view=users'), ('groups', A + 'com_users&view=groups'), ('levels', A + 'com_users&view=levels'), ('user notes', A + 'com_users&view=notes'),
    ('user add', A + 'com_users&task=user.add'), ('debug group', A + 'com_users&view=debuggroup&group_id=8'),
    ('global configuration', A + 'com_config'), ('menus', A + 'com_menus&view=menus'), ('menu items', A + 'com_menus&view=items&menutype='),
    ('menu item add', A + 'com_menus&task=item.add&menutype=mainmenu'), ('modules', A + 'com_modules&view=modules&client_id=0'), ('module select', A + 'com_modules&view=select&client_id=0'),
    ('plugins', A + 'com_plugins&view=plugins'), ('site template styles', A + 'com_templates&view=styles&client_id=0'), ('admin template styles', A + 'com_templates&view=styles&client_id=1'),
    ('extensions', A + 'com_installer&view=manage'), ('install', A + 'com_installer&view=install'), ('database', A + 'com_installer&view=database'),
    ('warnings', A + 'com_installer&view=warnings'), ('update sites', A + 'com_installer&view=updatesites'),
    ('languages installed', A + 'com_languages&view=installed'), ('content languages', A + 'com_languages&view=languages'),
    ('language overrides', A + 'com_languages&view=overrides'), ('joomla update', A + 'com_joomlaupdate'),
    ('scheduler', A + 'com_scheduler&view=tasks'), ('workflows', A + 'com_workflow&view=workflows&extension=com_content.article'), ('smart search index', A + 'com_finder&view=index'),
    ('banners', A + 'com_banners&view=banners'), ('contacts', A + 'com_contact&view=contacts'), ('newsfeeds', A + 'com_newsfeeds&view=newsfeeds'),
    ('tags', A + 'com_tags&view=tags'), ('fields', A + 'com_fields&view=fields&context=com_content.article'),
    ('media', A + 'com_media'), ('privacy requests', A + 'com_privacy&view=requests'), ('privacy consents', A + 'com_privacy&view=consents'),
    ('privacy capabilities', A + 'com_privacy&view=capabilities'), ('action logs', A + 'com_actionlogs&view=actionlogs'), ('guided tours', A + 'com_guidedtours&view=tours'),
    ('mail templates', A + 'com_mails&view=templates'), ('redirects', A + 'com_redirect&view=links'), ('check-in', A + 'com_checkin'), ('cache', A + 'com_cache'),
    ('associations', A + 'com_associations'), ('system information', A + 'com_admin&view=sysinfo'), ('messages', A + 'com_messages&view=messages'),
    ('post-installation', A + 'com_postinstall&view=messages&eid=700'), ('help', A + 'com_admin&view=help'),
    ('category add', A + 'com_categories&task=category.add&extension=com_content'), ('tag add', A + 'com_tags&task=tag.add'), ('contact add', A + 'com_contact&task=contact.add'),
    ('banner add', A + 'com_banners&task=banner.add'), ('newsfeed add', A + 'com_newsfeeds&task=newsfeed.add'), ('field add', A + 'com_fields&task=field.add&context=com_content.article'),
    ('workflow add', A + 'com_workflow&task=workflow.add&extension=com_content.article'), ('group add', A + 'com_users&task=group.add'), ('tour add', A + 'com_guidedtours&task=tour.add'),
    ('scheduler select', A + 'com_scheduler&view=select&layout=default'), ('finder filter add', A + 'com_finder&task=filter.add'), ('message add', A + 'com_messages&task=message.add'),
    ('redirect add', A + 'com_redirect&task=link.add'), ('privacy request add', A + 'com_privacy&task=request.add'),
    ('site home', '/'), ('site login', '/index.php?option=com_users&view=login'), ('site registration', '/index.php?option=com_users&view=registration'),
    ('site reset', '/index.php?option=com_users&view=reset'), ('site remind', '/index.php?option=com_users&view=remind'), ('site search', '/index.php?option=com_finder&view=search&q=test'),
    ('site featured', '/index.php?option=com_content&view=featured'), ('site tags', '/index.php?option=com_tags&view=tags'),
    ('site missing article (404 expected)', '/index.php?option=com_content&view=article&id=99999'),
    ('site article form as guest (403 expected)', '/index.php?option=com_content&view=form&layout=edit'),
]
EXPECTED = {'site missing article (404 expected)': 404, 'site article form as guest (403 expected)': 403}
HARMLESS_KEYS = {'PHP_SESSION_UPLOAD_PROGRESS'}  # a PHP setting name on the system information page
ERR = re.compile(r'Fatal error|Warning:|Notice:|Deprecated:|Uncaught|ArgumentCountError|Stack trace|Parse error')
KEY = re.compile(r'\b[A-Z][A-Z0-9]+(?:_[A-Z0-9]+){2,}\b')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--base', default='http://127.0.0.1:8099'); ap.add_argument('--user', default='admin'); ap.add_argument('--password', required=True)
    a = ap.parse_args()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))

    def get(path, data=None):
        try:
            with opener.open(urllib.request.Request(a.base + path, data=data), timeout=90) as r:
                return r.status, r.read().decode('utf-8', 'replace')
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode('utf-8', 'replace')
        except Exception as e:
            return 0, str(e)

    status, page = get('/administrator/index.php')
    token = re.search(r'name="([0-9a-f]{32})" value="1"', page)
    if not token:
        sys.exit('login form not found (status %s)' % status)
    get('/administrator/index.php', urllib.parse.urlencode({'username': a.user, 'passwd': a.password, 'option': 'com_login', 'task': 'login', 'return': 'aW5kZXgucGhw', token.group(1): '1'}).encode())
    problems, kk = [], 0
    for name, path in PAGES:
        status, page = get(path)
        text = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', page, flags=re.S | re.I)
        text = html.unescape(re.sub(r'<[^>]+>', ' ', text))
        keys = sorted(set(KEY.findall(text)) - HARMLESS_KEYS)
        lang = re.search(r'<html[^>]*\blang="([^"]+)"', page)
        kk += bool(lang and lang.group(1).lower() == 'kk-kz')
        if status != EXPECTED.get(name, 200) or ERR.search(page) or keys:
            problems.append((name, status, ERR.findall(page)[:2], keys[:4]))
    print('screens requested: %d, html lang kk-kz: %d, problems: %d' % (len(PAGES), kk, len(problems)))
    for p in problems:
        print('  !', p)
    sys.exit(1 if problems else 0)


if __name__ == '__main__':
    main()
