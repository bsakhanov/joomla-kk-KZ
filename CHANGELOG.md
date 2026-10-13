# Changelog · История изменений

## 6.1.4.2 — 13 October 2026 · 13 октября 2026 года

**English.** The translation is complete: all keys of Joomla 6.1.4 now have Kazakh values (previously about 3 970 administrator strings, 64 site strings and 30 API strings were still the Russian text of the JPath pack, and the installer language was missing).

- translated about 3 400 strings; added the installer language (`installation/language/kk-KZ`);
- files rebuilt in the order of the Joomla 6.1.4 originals; about 550 obsolete keys (mostly Russian plural forms) removed;
- fixed strings that could break output: one string with more `%s` than the original, mail templates using variables the original does not have, empty workflow descriptions of the blog sample data, a lost link in the CAPTCHA description;
- added `tools/kkpack.py` (status, check, sync, bump, build, fetch), `GLOSSARY.md`, trilingual README and CONTRIBUTING;
- licence stated as GPL-2.0-or-later.

Known limits: not proofread by a native speaker; no live installation test yet; about 270 inherited strings differ from the original in inline HTML markup.

**Русский.** Перевод доведён до конца: у всех ключей Joomla 6.1.4 есть казахские значения (раньше около 3 970 строк админки, 64 строки сайта и 30 строк API оставались русским текстом пакета JPath, а языка установщика не было).

- переведено около 3 400 строк; добавлен язык установщика (`installation/language/kk-KZ`);
- файлы пересобраны в порядке оригиналов Joomla 6.1.4; убрано около 550 устаревших ключей (в основном русские формы множественного числа);
- исправлены строки, способные испортить вывод: одна строка с лишним `%s`, шаблоны писем с переменными, которых нет в оригинале, пустые описания процесса в демо-данных блога, потерянная ссылка в описании CAPTCHA;
- добавлены `tools/kkpack.py` (status, check, sync, bump, build, fetch), `GLOSSARY.md`, трёхъязычные README и CONTRIBUTING;
- лицензия указана как GPL-2.0-or-later.

Известные ограничения: перевод не вычитан носителем языка; живой установки для проверки пока не было; около 270 унаследованных строк отличаются от оригинала встроенной HTML-разметкой.

## 6.1.4.1 — October 2026 · октябрь 2026 года

First version of the pack, built on the JPath Russian pack 6.1.4.1; untranslated strings stayed in Russian. · Первая версия пакета на основе русского пакета JPath 6.1.4.1; непереведённые строки оставались на русском.
