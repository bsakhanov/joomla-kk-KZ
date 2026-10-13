# Quality notes · Заметки о качестве

## English

`kk_lint` v0.4.5 of [kk-redkollegiya](https://github.com/bsakhanov/kk-redkollegiya) (profile `ini`, the English original of Joomla 6.1.4 as `--source`, the author's glossary, the hunspell-kk dictionary) was run over all 537 files. It reported 1,066 findings:

| Rule | Count | What it is |
| --- | --- | --- |
| J01 placeholders (blocker) | 724 | the set of placeholders, HTML tags and escapes differs from the original. Among them: «» used instead of `\"` (by design), entities such as `&#160;`, and the markup differences inherited from the earlier pack (listed in issue 2). Real defects found this way (three strings with an unclosed tag) are fixed. |
| J03 ini_syntax | 167 | keys with a colon, e.g. `COM_ADMIN_HELP_ADMIN_MODULES:_CUSTOM`. The original uses them and PHP parses them: false positives. |
| P01 punct_junk | 141 | file names and code inside descriptions (`.htaccess`, `IndexIgnore`). |
| J02 missing_key | 15 | keys that are empty in the original too (sample data) and the thousands separator, which is a space by design. |
| T02 glossary_avoid | 14 | «сандық» is used for "numeric"; the glossary rule «цифрлық» instead of «сандық» concerns "digital". |
| P04 empty_brackets | 5 | `()` kept from the original. |

2,017 distinct words (10,523 occurrences) are not in the hunspell-kk dictionary: inflected forms, loanwords, product names. The list with frequencies is in [words-outside-dictionary.tsv](words-outside-dictionary.tsv) for the proofreader. In addition, `tools/kkpack.py check` compares every string with the original, and a separate check looks for unclosed HTML tags.

## Русский

`kk_lint` v0.4.5 из [kk-redkollegiya](https://github.com/bsakhanov/kk-redkollegiya) (профиль `ini`, английский оригинал Joomla 6.1.4 в `--source`, глоссарий автора, словарь hunspell-kk) прогнан по всем 537 файлам. Находок 1 066:

| Правило | Число | Что это |
| --- | --- | --- |
| J01 placeholders (blocker) | 724 | набор заполнителей, HTML-тегов и экранирований отличается от оригинала. Среди них: «ёлочки» вместо `\"` (так задумано), сущности вроде `&#160;` и расхождения в разметке, унаследованные от прежнего пакета (список — в issue 2). Настоящие дефекты, найденные так (три строки с незакрытым тегом), исправлены. |
| J03 ini_syntax | 167 | ключи с двоеточием, например `COM_ADMIN_HELP_ADMIN_MODULES:_CUSTOM`. Оригинал их использует, PHP их разбирает: ложные срабатывания. |
| P01 punct_junk | 141 | имена файлов и код внутри описаний (`.htaccess`, `IndexIgnore`). |
| J02 missing_key | 15 | ключи, пустые и в оригинале (демо-данные), и разделитель тысяч, который задуман пробелом. |
| T02 glossary_avoid | 14 | «сандық» стоит для «числовой», правило глоссария «цифрлық» вместо «сандық» относится к «цифровой». |
| P04 empty_brackets | 5 | `()`, сохранённые из оригинала. |

В словаре hunspell-kk нет 2 017 разных слов (10 523 вхождения): словоформы, заимствования, названия продуктов. Список с частотами — в [words-outside-dictionary.tsv](words-outside-dictionary.tsv) для вычитывающего. Кроме того, `tools/kkpack.py check` сверяет каждую строку с оригиналом, а отдельная проверка ищет незакрытые HTML-теги.
