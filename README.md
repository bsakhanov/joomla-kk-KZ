# Joomla 6 Kazakh language pack (kk-KZ)

**English** · [Русский](README.ru.md) · [Қазақша](README.kk.md)

[![License: GPL-2.0-or-later](https://img.shields.io/badge/license-GPL--2.0--or--later-blue.svg)](LICENSE)
[![Joomla 6.1.4](https://img.shields.io/badge/Joomla-6.1.4-1b5e84.svg)](https://github.com/joomla/joomla-cms/releases/tag/6.1.4)
[![Release](https://img.shields.io/github/v/release/bsakhanov/joomla-kk-KZ?color=blue)](https://github.com/bsakhanov/joomla-kk-KZ/releases)

> The Kazakh text was translated with AI assistance and **has not yet been proofread by a native speaker**. Corrections are welcome: see [CONTRIBUTING.md](CONTRIBUTING.md).

An open-source Kazakh (kk-KZ) language pack for Joomla 6 and later: administrator, site, Web Services API and the installer. It is maintained the way the Russian pack is maintained at [JPathRu/localisation](https://github.com/JPathRu/localisation): the repository root is the package root, one release per Joomla version, terminology lives in a [glossary](GLOSSARY.md), mistakes are reported as issues.

**Page:** https://bsakhanov.github.io/joomla-kk-KZ/ · **Release:** https://github.com/bsakhanov/joomla-kk-KZ/releases/tag/6.1.4.2

## Status

| | |
| --- | --- |
| Joomla version | 6.1.4 (6.2 follows after its stable release) |
| Pack version | 6.1.4.2: the Joomla version plus the translation revision |
| Strings | 13,691 in 537 files; every key of Joomla 6.1.4 has a Kazakh value |
| Left in English on purpose | 153 distinct strings: template position names, protocol and product names ([list](docs/keep-english.txt)) |
| Installer language | included (`installation/language/kk-KZ`), not part of the Joomla package manifest |

## Installation

1. Download `kk-KZ_joomla_lang_full_6.1.4v2.zip` from the release assets. If the file is missing, take the release's "Source code (zip)": the repository is laid out as a package and Joomla installs it the same way.
2. In the administrator: System → Install → Extensions → Upload Package File.
3. System → Languages → Installed: make Kazakh the default for the site and/or the administrator.

To install Joomla itself in Kazakh, copy `installation/language/kk-KZ` into `installation/language/` of the Joomla distribution before starting the installer. The archive `kk-KZ_joomla_lang_root_6.1.4v2.zip` unpacks straight into the Joomla root and contains that folder.

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

## Terminology

The benchmark is expressions established in the language and the international approach. International words stay (alias, plugin, module, template, cache, token, object, subject); the author's decisions are «сайт», «дерекқор», «қолданба», «пошта». Template position names stay in Latin because they are identifiers. See [GLOSSARY.md](GLOSSARY.md).

## What is verified and what is not

Verified by `tools/kkpack.py check`: in all 537 files the keys and their order equal the Joomla 6.1.4 original; no string uses more printf arguments or more `{VARIABLES}` than the original (that would break a PHP 8 page or leave raw variables in an email); there are no unescaped quotes; every file parses with PHP 8.3 `parse_ini_file` without errors.

Not verified: a live installation and a click-through of the administrator in Joomla 6, and proofreading by a native speaker. About 270 strings inherited from the earlier pack differ from the original in inline HTML (mostly dropped emphasis tags); they are tracked in the issues.

## License

GNU General Public License, version 2 or (at your option) any later version ([LICENSE](LICENSE)): the same terms as Joomla! itself. The pack is derived from the English language files of Joomla! (© Open Source Matters, Inc.) and from the Russian pack of the Joomla community (JPathRu).

## Credits

Joomla! Project (original strings), the JPathRu translation team (the base of the pack), Webmarka · Beibit Sakhanov (maintenance, Kazakh text), kk-redkollegiya (checking tools), Claude (AI-assisted translation).

## Citation

Sakhanov, B. Joomla 6 Kazakh language pack (kk-KZ), version 6.1.4.2. — 2026. — https://github.com/bsakhanov/joomla-kk-KZ. Machine-readable record: `CITATION.cff`.
