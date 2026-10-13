# The official Kazakh translation and this pack · Официальный казахский перевод и этот пакет

## English

**Source.** [joomla/core-translations](https://github.com/joomla/core-translations) (connected to Crowdin), folder `joomla_v6/translations/package/kk-KZ`, commit 528d55e of 12 October 2026. Translator: Akylkerey Sarvarov (Joomla Translations Working Group). 536 `.ini` files.

**Coverage** against the source of Joomla 6 (13,471 keys): 12,146 keys have a Kazakh value, 113 equal the English text, 976 are missing (new in Joomla 6.x: com_workflow 94, com_admin 81, com_joomlaupdate 67, lib_joomla 40, com_scheduler 31, ...). Compared with this pack, 1,597 strings are identical and about 10,300 differ.

**Technical defects**, found by checking the official files against Joomla 6.1.4 with `tools/kkpack.py` (the list is in [review/official-defects.tsv](review/official-defects.tsv)):

| Defect | Strings |
| --- | --- |
| more printf arguments than the original (an error on PHP 8 when the string is used) | 31 |
| value corrupted (several keys merged into one) | 7 |
| Russian words (JGLOBAL_NAME_ASC and JGLOBAL_NAME_DESC are Russian entirely) | 7 |
| Latin and Cyrillic letters mixed in one word | 9 |
| a short label replaced by a long sentence from another context | 26 |
| legacy `_QQ_` escape, which Joomla 6 does not interpret and shows literally | 61 |

**Wording problems in very visible places** (English → official): Media → «Сурет»; Global Check-in → «Жалпы Тіркеу»; Overrides → «Өткізуден бас тарту»; No → «Ешқашан»; Trashed → «Тазаланған»; Stage → «Сахна»; Unfeatured → «Бейресми»; Check-in → «Тексеріңіз». The earlier text of this pack had errors of its own kind (the word «Толығырақ» stood for 27 different strings, for example New Banner and General; «Басқару панелі» stood for Administrator): in 193 such places the official string was taken.

**Terminology** (occurrences in this pack / in the official translation, counted before the review): меню 437 / 17 and мәзір 0 / 366; категория 534 / 84 and санат 0 / 421; шаблон 232 / 16 and үлгі 37 / 242; алиас 79 / 4 and бүркеншік ат 0 / 66; кеңейтім 167 / 322 (this pack mixed it with «кеңейту» 252 / 30 and now uses «кеңейтім» only).

**How the pack uses it**

1. The official translation is a reference. A string is taken from it only if it is listed in [adopt-official.txt](adopt-official.txt) (193 strings), it passes the checks, and nothing in [overrides.tsv](overrides.tsv) says otherwise.
2. [overrides.tsv](overrides.tsv) holds the pack's own wording (101 strings): it wins over the official one.
3. [glossary-guard.txt](glossary-guard.txt) lists the official terms that conflict with the author's decisions; in mode `all` such strings are not taken.
4. [review/official-diff.tsv](review/official-diff.tsv) is a table of 5,419 short labels where the two translations differ (462 of them because of the guard). A native speaker fills the column `choice` with `official`, `ours` or his own text, and the choices are applied with `--apply`.

```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/joomla/core-translations.git
git -C core-translations sparse-checkout set joomla_v6/translations/package/kk-KZ joomla_v6/translations/core/installation
OFF=core-translations/joomla_v6/translations
python3 tools/kkpack.py official --en .cache/joomla-6.1.4 --official $OFF/package/kk-KZ --official-installer $OFF/core/installation/language/kk-KZ            # dry run for the adoption list
python3 tools/kkpack.py official ... --diff docs/review/official-diff.tsv --defects docs/review/official-defects.tsv                                             # rebuild the review tables
python3 tools/kkpack.py official ... --apply docs/review/official-diff.tsv --write                                                                               # apply the review choices
```

The defect list can be reported to the official Kazakh team on [Crowdin](https://joomla.crowdin.com/cms).

## Русский

**Источник.** [joomla/core-translations](https://github.com/joomla/core-translations) (связан с Crowdin), каталог `joomla_v6/translations/package/kk-KZ`, коммит 528d55e от 12 октября 2026 года. Переводчик — Акылкерей Сарваров (рабочая группа по переводам Joomla). 536 файлов `.ini`.

**Охват** относительно исходника Joomla 6 (13 471 ключ): у 12 146 ключей есть казахское значение, у 113 оно совпадает с английским текстом, 976 отсутствуют (новые в Joomla 6.x: com_workflow 94, com_admin 81, com_joomlaupdate 67, lib_joomla 40, com_scheduler 31 и так далее). С нашим пакетом совпадают 1 597 строк, около 10 300 отличаются.

**Технические дефекты**, найденные проверкой официальных файлов по Joomla 6.1.4 командой `tools/kkpack.py` (список — в [review/official-defects.tsv](review/official-defects.tsv)):

| Дефект | Строк |
| --- | --- |
| больше аргументов printf, чем в оригинале (на PHP 8 при использовании строки возникает ошибка) | 31 |
| повреждённое значение (несколько ключей склеены в один) | 7 |
| русские слова (JGLOBAL_NAME_ASC и JGLOBAL_NAME_DESC целиком по-русски) | 7 |
| латинские и кириллические буквы в одном слове | 9 |
| короткая подпись заменена длинным предложением из другого контекста | 26 |
| старое экранирование `_QQ_`, которое Joomla 6 не обрабатывает и показывает как есть | 61 |

**Неверные формулировки в самых видимых местах** (английский → официальный): Media → «Сурет»; Global Check-in → «Жалпы Тіркеу»; Overrides → «Өткізуден бас тарту»; No → «Ешқашан»; Trashed → «Тазаланған»; Stage → «Сахна»; Unfeatured → «Бейресми»; Check-in → «Тексеріңіз». В прежнем тексте этого пакета были ошибки того же рода (слово «Толығырақ» стояло против 27 разных строк, например New Banner и General; «Басқару панелі» — против Administrator): в 193 таких местах взята официальная строка.

**Терминология** (вхождений в этом пакете / в официальном переводе, подсчёт до вычитки): меню 437 / 17 и мәзір 0 / 366; категория 534 / 84 и санат 0 / 421; шаблон 232 / 16 и үлгі 37 / 242; алиас 79 / 4 и бүркеншік ат 0 / 66; кеңейтім 167 / 322 (в этом пакете оно мешалось с «кеңейту» 252 / 30, теперь везде «кеңейтім»).

**Как пакет это использует**

1. Официальный перевод — эталон. Строка берётся оттуда, только если она есть в [adopt-official.txt](adopt-official.txt) (193 строки), проходит проверки и [overrides.tsv](overrides.tsv) не говорит обратного.
2. В [overrides.tsv](overrides.tsv) лежат собственные формулировки пакета (101 строка): они сильнее официальных.
3. [glossary-guard.txt](glossary-guard.txt) перечисляет официальные термины, противоречащие решениям автора; в режиме `all` такие строки не берутся.
4. [review/official-diff.tsv](review/official-diff.tsv) — таблица из 5 419 коротких подписей, где переводы расходятся (462 из них — из-за охранного списка). Носитель языка заполняет столбец `choice` словом `official`, `ours` или своим текстом, и выбор применяется ключом `--apply`.

Команды — в английской части выше. Список дефектов можно передать официальной казахской команде на [Crowdin](https://joomla.crowdin.com/cms).
