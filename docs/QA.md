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

## Live test · Живая проверка

English. Clean Joomla 6.1.4 full package, PHP 8.3.6, MariaDB 10.11.14, installed with `php installation/joomla.php install`. The pack was installed with `php cli/joomla.php extension:install --path=dist/kk-KZ_joomla_lang_full_6.1.4v2.zip`: three `kk-KZ` language extensions appeared (site, administrator, API). Kazakh was made the default for the site and the administrator (`com_languages` parameters), the admin user logged in, and 81 distinct addresses were requested with `tools/smoke_crawl.py`; 79 opened normally and two gave the expected 404 and 403 error pages, also in Kazakh. They covered: dashboards, article, category, tag, contact, banner, news feed, field, workflow, user, group and menu item forms, lists, global configuration, extensions, languages, scheduler, Smart Search, privacy, mail templates, system information, plus the public login, registration and search pages. None of them returned a PHP error, notice or untranslated language key (the only key-like text is the PHP setting name `PHP_SESSION_UPLOAD_PROGRESS` on the system information page). The web installer, started with `Accept-Language: kk-KZ` over the root archive, rendered in Kazakh. Not covered: JavaScript-driven parts, visual review, the API with a token.

Русский. Чистый полный пакет Joomla 6.1.4, PHP 8.3.6, MariaDB 10.11.14, установка командой `php installation/joomla.php install`. Пакет поставлен командой `php cli/joomla.php extension:install --path=dist/kk-KZ_joomla_lang_full_6.1.4v2.zip`: появились три языковых расширения `kk-KZ` (сайт, админка, API). Казахский сделан языком по умолчанию для сайта и админки (параметры `com_languages`), администратор вошёл, и с помощью `tools/smoke_crawl.py` запрошено 81 разных адресов; 79 открылись штатно, ещё два дали ожидаемые страницы ошибок 404 и 403, тоже на казахском. Охвачены: панели, формы статьи, категории, метки, контакта, баннера, ленты новостей, поля, процесса, пользователя, группы и пункта меню, списки, общая конфигурация, расширения, языки, планировщик, умный поиск, персональные данные, шаблоны писем, сведения о системе, а также публичные страницы входа, регистрации и поиска. Ни один не вернул ошибку PHP, замечание или неперекладённый языковой ключ (единственный текст, похожий на ключ, — имя настройки PHP `PHP_SESSION_UPLOAD_PROGRESS` на странице сведений о системе). Веб-установщик, запущенный с `Accept-Language: kk-KZ` поверх корневого архива, отрисовался на казахском. Не охвачено: части на JavaScript, визуальный осмотр, API с токеном.
