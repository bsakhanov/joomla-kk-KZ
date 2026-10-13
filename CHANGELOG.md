# Changelog · История изменений

## 6.1.4.3 — 13 October 2026 · 13 октября 2026 года

**English.** Feedback from a Kazakh Joomla specialist: some labels were too long and broke the look of the administrator, and the pack should not rest on the Russian JPath pack.

- sidebar labels that did not fit next to the «+» button are shortened (the reported «Басқару панелінің модульдері» is now «Әкімші модульдері»; also the action log, user notes, consents, requests, capabilities); the layout is checked in a real browser with `tools/sidebar_check.js`;
- the pack no longer says that it is based on the JPath Russian pack (manifests, README, citation, file headers): the source strings are the English files of Joomla 6.1.4, and the Kazakh text is checked against the official Kazakh translation of the Joomla Translations Working Group (Akylkerey Sarvarov), whose author is credited in the manifests;
- 193 strings are taken from the official translation where the earlier text was demonstrably wrong (for example «Толығырақ» stood for New Banner, General, Edit Contact); 101 strings have the pack's own corrected wording; 534 values changed in total;
- one term for «extension»: «кеңейтім» everywhere (it was mixed with «кеңейту» in 224 strings);
- `tools/kkpack.py official`, [docs/OFFICIAL.md](docs/OFFICIAL.md), a table of 5,419 labels for a native-speaker review and a list of 80 defects of the official translation (31 strings that break PHP 8, 7 corrupted, 7 Russian, 26 mis-contextual labels; 61 more use the legacy `_QQ_` escape);
- `docs/glossary-guard.txt`: official terms that conflict with the author's glossary («мәзір», «санат», «үлгі», «бүркеншік ат») are not taken.

**Русский.** Замечания казахстанского специалиста по Joomla: часть подписей была слишком длинной и портила вид админки, а пакет не должен опираться на русский пакет JPath.

- подписи бокового меню, не умещавшиеся рядом с кнопкой «+», сокращены («Басқару панелінің модульдері» из замечания теперь «Әкімші модульдері»; также журнал действий, заметки о пользователях, согласия, запросы, возможности); вёрстка проверяется в настоящем браузере скриптом `tools/sidebar_check.js`;
- пакет больше не называет себя основанным на русском пакете JPath (манифесты, README, цитирование, заголовки файлов): исходные строки — английские файлы Joomla 6.1.4, а казахский текст сверен с официальным казахским переводом рабочей группы по переводам Joomla (Акылкерей Сарваров), автор указан в манифестах;
- 193 строки взяты из официального перевода там, где прежний текст был заведомо неверным (например, «Толығырақ» стояло против New Banner, General, Edit Contact); у 101 строки собственная исправленная формулировка; всего изменено 534 значения;
- один термин для «расширения»: везде «кеңейтім» (в 224 строках он мешался с «кеңейту»);
- `tools/kkpack.py official`, [docs/OFFICIAL.md](docs/OFFICIAL.md), таблица из 5 419 подписей для вычитки носителем языка и список из 80 дефектов официального перевода (31 строка, роняющая PHP 8, 7 повреждённых, 7 русских, 26 подписей не из того контекста; ещё 61 со старым экранированием `_QQ_`);
- `docs/glossary-guard.txt`: официальные термины, противоречащие глоссарию автора («мәзір», «санат», «үлгі», «бүркеншік ат»), не берутся.

## 6.1.4.2 — 13 October 2026 · 13 октября 2026 года

**English.** The translation is complete: all keys of Joomla 6.1.4 now have Kazakh values (previously about 3 970 administrator strings, 64 site strings and 30 API strings were still the Russian text of the JPath pack, and the installer language was missing).

- translated about 3 400 strings; added the installer language (`installation/language/kk-KZ`);
- files rebuilt in the order of the Joomla 6.1.4 originals; about 550 obsolete keys (mostly Russian plural forms) removed;
- fixed strings that could break output: one string with more `%s` than the original, mail templates using variables the original does not have, empty workflow descriptions of the blog sample data, a lost link in the CAPTCHA description;
- added `tools/kkpack.py` (status, check, sync, bump, build, fetch), `GLOSSARY.md`, trilingual README and CONTRIBUTING;
- licence stated as GPL-2.0-or-later.

Checked on a clean Joomla 6.1.4 (PHP 8.3, MariaDB 10.11): the package installs with `extension:install`, 79 administrator and site screens open without PHP errors or raw keys, the web installer starts in Kazakh. Joomla's own distribution already carries a partial kk-KZ installer translation (249 of 262 keys in `joomla.ini`, 5 of 37 in `joomla.cli.ini`); the installer files of this pack are complete for 6.1.4.

Known limits: not proofread by a native speaker; about 270 inherited strings differ from the original in inline HTML markup.

**Русский.** Перевод доведён до конца: у всех ключей Joomla 6.1.4 есть казахские значения (раньше около 3 970 строк админки, 64 строки сайта и 30 строк API оставались русским текстом пакета JPath, а языка установщика не было).

- переведено около 3 400 строк; добавлен язык установщика (`installation/language/kk-KZ`);
- файлы пересобраны в порядке оригиналов Joomla 6.1.4; убрано около 550 устаревших ключей (в основном русские формы множественного числа);
- исправлены строки, способные испортить вывод: одна строка с лишним `%s`, шаблоны писем с переменными, которых нет в оригинале, пустые описания процесса в демо-данных блога, потерянная ссылка в описании CAPTCHA;
- добавлены `tools/kkpack.py` (status, check, sync, bump, build, fetch), `GLOSSARY.md`, трёхъязычные README и CONTRIBUTING;
- лицензия указана как GPL-2.0-or-later.

Проверено на чистой Joomla 6.1.4 (PHP 8.3, MariaDB 10.11): пакет ставится через `extension:install`, 79 экранов админки и сайта открывается без ошибок PHP и «сырых» ключей, веб-установщик запускается на казахском. В дистрибутив Joomla уже входит частичный казахский перевод установщика (249 из 262 ключей в `joomla.ini`, 5 из 37 в `joomla.cli.ini`); файлы установщика этого пакета полны для 6.1.4.

Известные ограничения: перевод не вычитан носителем языка; около 270 унаследованных строк отличаются от оригинала встроенной HTML-разметкой.

## 6.1.4.1 — October 2026 · октябрь 2026 года

First version of the pack, built on the JPath Russian pack 6.1.4.1; untranslated strings stayed in Russian. · Первая версия пакета на основе русского пакета JPath 6.1.4.1; непереведённые строки оставались на русском.
