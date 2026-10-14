# Joomla 6 Kazakh language pack (kk-KZ)

**English** · [Русский](README.ru.md) · [Қазақша](README.kk.md)

[![License: GPL-2.0-or-later](https://img.shields.io/badge/license-GPL--2.0--or--later-blue.svg)](LICENSE)
[![Joomla 6.2.0](https://img.shields.io/badge/Joomla-6.2.0-1b5e84.svg)](https://github.com/joomla/joomla-cms/releases/tag/6.2.0)
[![Release](https://img.shields.io/github/v/release/bsakhanov/joomla-kk-KZ?color=blue)](https://github.com/bsakhanov/joomla-kk-KZ/releases)

> The Kazakh text was translated with AI assistance and **has not yet been proofread by a native speaker**. Corrections are welcome: see [CONTRIBUTING.md](CONTRIBUTING.md).

An open-source Kazakh (kk-KZ) language pack for Joomla 6 and later: administrator, site, Web Services API and the installer. The repository is laid out like the Russian pack repository [JPathRu/localisation](https://github.com/JPathRu/localisation): the repository root is the package root, one release per Joomla version, terminology lives in a [glossary](GLOSSARY.md), mistakes are reported as issues.

**Page:** https://bsakhanov.github.io/joomla-kk-KZ/ · **Release:** https://github.com/bsakhanov/joomla-kk-KZ/releases/tag/6.2.0.2

## Status

| | |
| --- | --- |
| Joomla version | 6.2.0 |
| Pack version | 6.2.0.2: the Joomla version plus the translation revision |
| Strings | 13,770 in 539 files; every key of Joomla 6.2.0 has a Kazakh value |
| Left in English on purpose | 152 distinct strings: template position names, protocol and product names ([list](docs/keep-english.txt)) |
| Installer language | included (`installation/language/kk-KZ`), not part of the Joomla package manifest |

For Joomla 6.1.x use the release [6.1.4.4](https://github.com/bsakhanov/joomla-kk-KZ/releases/tag/6.1.4.4).

## Installation

1. Download `kk-KZ_joomla_lang_full_6.2.0v2.zip` from the release assets. If the file is missing, take the release's "Source code (zip)": the repository is laid out as a package and Joomla installs it the same way.
2. In the administrator: System → Install → Extensions → Upload Package File.
3. System → Languages → Installed: make Kazakh the default for the site and/or the administrator.

To install Joomla itself in Kazakh, copy `installation/language/kk-KZ` into `installation/language/` of the Joomla distribution before starting the installer. The archive `kk-KZ_joomla_lang_root_6.2.0v2.zip` unpacks straight into the Joomla root and contains that folder.

### Default language and the Language Filter

When Joomla installs a site language it creates a Content Language for it — unpublished. If the "System - Language Filter" plugin is on and Kazakh becomes the default site language while that content language is unpublished, the filter cannot find its URL prefix and redirects the home page to `//` in a loop (`Undefined array key "kk-KZ"` in `LanguageFilter.php`). Since 6.2.0.2 the package publishes the Kazakh content language itself where it is safe: on a site without the Language Filter, and on a site where Kazakh is already the default. On a multilingual site with another default language it only warns: publish Kazakh in **Content → Languages** before making it the default.

### Updates

The package has an update server: a new version shows up in **System → Update → Extensions**. The update list is `updates/pkg_kk-KZ.xml`; the archive is attached to each release.

## What is inside

| Path | What it is |
| --- | --- |
| `administrator/language/kk-KZ/` | administrator strings |
| `language/kk-KZ/` | site strings |
| `api/language/kk-KZ/` | Web Services API strings |
| `installation/language/kk-KZ/` | installer strings |
| `pkg_kk-KZ.xml` | package manifest |
| `GLOSSARY.md` | frequent terms and the decisions behind them |
| `tools/kkpack.py` | comparison with the English original, checks, build |
| `tools/smoke_crawl.py` | smoke test of the pack on a running Joomla |
| `tools/sidebar_check.js` | checks the administrator sidebar in a real browser (long labels) |
| `docs/` | project page, maintenance guide, list of strings kept in English |

## Maintenance

```bash
python3 tools/kkpack.py fetch 6.1.5                              # English originals of a new Joomla release
python3 tools/kkpack.py status --en .cache/joomla-6.1.5
python3 tools/kkpack.py sync --en .cache/joomla-6.1.5 --write    # new keys arrive in English, obsolete ones go
python3 tools/kkpack.py check --en .cache/joomla-6.1.5
python3 tools/kkpack.py build                                    # dist/*.zip and SHA256SUMS
```

Details: [docs/MAINTAINING.md](docs/MAINTAINING.md).

## Where the text comes from

The source strings are the English files of Joomla 6.2.0 (official release; the official source repository is [joomla/core-translations](https://github.com/joomla/core-translations)). The Kazakh text is the earlier version of this pack plus AI-assisted translation, checked against the **official Kazakh translation** of the Joomla Translations Working Group (translator: Akylkerey Sarvarov, [`joomla_v6/translations/package/kk-KZ`](https://github.com/joomla/core-translations/tree/main/joomla_v6/translations/package/kk-KZ), 12,146 of the 13,471 keys of Joomla 6). Where this pack's wording was demonstrably wrong, the official string is used: 193 strings, listed in [docs/adopt-official.txt](docs/adopt-official.txt).

The official translation is not taken wholesale, for two reasons. It has technical defects: 31 strings with more printf arguments than the original (a fatal error on PHP 8), 7 corrupted values, 7 with Russian text, 26 labels replaced by long sentences, 61 with the legacy `_QQ_` escape that Joomla 6 shows literally. And it has wrong wording in very visible places (Media is «Сурет», Global Check-in is «Жалпы Тіркеу», Overrides is «Өткізуден бас тарту»). Its terminology («мәзір», «санат», «үлгі», «бүркеншік ат») also differs from this pack's decisions («меню», «категория», «шаблон», «алиас»). Details, examples and the list of defects: [docs/OFFICIAL.md](docs/OFFICIAL.md); a table of 5,425 short labels for a native-speaker review: [docs/review/official-diff.tsv](docs/review/official-diff.tsv).

An accredited Kazakh pack also exists for Joomla 3.9 to 5.0 ([downloads.joomla.org](https://downloads.joomla.org)), and Joomla 6 ships a partial Kazakh installer translation. This repository is an independent pack for Joomla 6 and does not claim to be the accredited one. Both use the package id `pkg_kk-KZ`, so this pack installs over an existing one as an upgrade.

## Terminology

The benchmark is expressions established in the language and the international approach. International words stay (alias, plugin, module, template, cache, token, object, subject); the author's decisions are «сайт», «дерекқор», «қолданба», «пошта». Template position names stay in Latin because they are identifiers. See [GLOSSARY.md](GLOSSARY.md).

## What is verified and what is not

Verified by `tools/kkpack.py check`: in all 539 files the keys and their order equal the Joomla 6.2.0 original; no string uses more printf arguments or more variables of the `{NAME}` kind than the original (that would break a PHP 8 page or leave raw variables in an email); there are no unescaped quotes; every file parses with PHP 8.3 `parse_ini_file` without errors.

The strings were also run through `kk_lint` of [kk-redkollegiya](https://github.com/bsakhanov/kk-redkollegiya) v0.4.5; the findings and their interpretation are in [docs/QA.md](docs/QA.md).

Also checked on a clean Joomla 6.2.0 (PHP 8.3, MariaDB 10.11): the package installs with Joomla's own installer and registers for the site, the administrator and the API; with Kazakh set as the default language, 80 administrator and site screens (lists, create forms, global configuration, extensions, languages, scheduler, workflows, privacy, Smart Search) open without PHP errors and without raw language keys, and the web installer starts in Kazakh. The check can be repeated: see [docs/MAINTAINING.md](docs/MAINTAINING.md).

The administrator sidebar was also rendered in headless Chromium (`tools/sidebar_check.js`): in all expanded sections no label wraps and no «+» button drops to the next line.

Not verified: proofreading by a native speaker, a visual review of every screen, the Web Services API with a real token. About 270 strings inherited from the earlier pack differ from the original in inline HTML (mostly dropped emphasis tags); they are tracked in the issues.

## License

GNU General Public License, version 2 or (at your option) any later version ([LICENSE](LICENSE)): the same terms as Joomla! itself. The pack is derived from the English language files of Joomla! (© Open Source Matters, Inc.) and, for part of the strings, from the official Kazakh translation (joomla/core-translations).

## Credits

Joomla! Project (original strings), Akylkerey Sarvarov and the Joomla Translations Working Group (the official Kazakh translation: reference and a source of part of the strings), Webmarka · Beibit Sakhanov (maintenance, Kazakh text), kk-redkollegiya (checking tools), Claude (AI-assisted translation).

## Citation

Sakhanov, B. Joomla 6 Kazakh language pack (kk-KZ), version 6.2.0.2. — 2026. — https://github.com/bsakhanov/joomla-kk-KZ. Machine-readable record: `CITATION.cff`.
