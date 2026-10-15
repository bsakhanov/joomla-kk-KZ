# Quality notes · Заметки о качестве

## English

`kk_lint` v0.4.5 of [kk-redkollegiya](https://github.com/bsakhanov/kk-redkollegiya) (profile `ini`, the English original of Joomla 6.2.0 as `--source`, the author's glossary, the hunspell-kk dictionary) was run over all 539 files. It reported 1,066 findings:

| Rule | Count | What it is |
| --- | --- | --- |
| J01 placeholders (blocker) | 724 | the set of placeholders, HTML tags and escapes differs from the original. Among them: «» used instead of `\"` (by design), entities such as `&#160;`, and the markup differences inherited from the earlier pack (listed in issue 2). Real defects found this way (three strings with an unclosed tag) are fixed. |
| J03 ini_syntax | 167 | keys with a colon, e.g. `COM_ADMIN_HELP_ADMIN_MODULES:_CUSTOM`. The original uses them and PHP parses them: false positives. |
| P01 punct_junk | 141 | file names and code inside descriptions (`.htaccess`, `IndexIgnore`). |
| J02 missing_key | 15 | keys that are empty in the original too (sample data) and the thousands separator, which is a space by design. |
| T02 glossary_avoid | 14 | «сандық» is used for "numeric"; the glossary rule «цифрлық» instead of «сандық» concerns "digital". |
| P04 empty_brackets | 5 | `()` kept from the original. |

2,040 distinct words (10,663 occurrences) are not in the hunspell-kk dictionary: inflected forms, loanwords, product names. The list with frequencies is in [words-outside-dictionary.tsv](words-outside-dictionary.tsv) for the proofreader. In addition, `tools/kkpack.py check` compares every string with the original, and a separate check looks for unclosed HTML tags.

## Русский

`kk_lint` v0.4.5 из [kk-redkollegiya](https://github.com/bsakhanov/kk-redkollegiya) (профиль `ini`, английский оригинал Joomla 6.2.0 в `--source`, глоссарий автора, словарь hunspell-kk) прогнан по всем 539 файлам. Находок 1 066:

| Правило | Число | Что это |
| --- | --- | --- |
| J01 placeholders (blocker) | 724 | набор заполнителей, HTML-тегов и экранирований отличается от оригинала. Среди них: «ёлочки» вместо `\"` (так задумано), сущности вроде `&#160;` и расхождения в разметке, унаследованные от прежнего пакета (список — в issue 2). Настоящие дефекты, найденные так (три строки с незакрытым тегом), исправлены. |
| J03 ini_syntax | 167 | ключи с двоеточием, например `COM_ADMIN_HELP_ADMIN_MODULES:_CUSTOM`. Оригинал их использует, PHP их разбирает: ложные срабатывания. |
| P01 punct_junk | 141 | имена файлов и код внутри описаний (`.htaccess`, `IndexIgnore`). |
| J02 missing_key | 15 | ключи, пустые и в оригинале (демо-данные), и разделитель тысяч, который задуман пробелом. |
| T02 glossary_avoid | 14 | «сандық» стоит для «числовой», правило глоссария «цифрлық» вместо «сандық» относится к «цифровой». |
| P04 empty_brackets | 5 | `()`, сохранённые из оригинала. |

В словаре hunspell-kk нет 2 040 разных слов (10 663 вхождения): словоформы, заимствования, названия продуктов. Список с частотами — в [words-outside-dictionary.tsv](words-outside-dictionary.tsv) для вычитывающего. Кроме того, `tools/kkpack.py check` сверяет каждую строку с оригиналом, а отдельная проверка ищет незакрытые HTML-теги.

## Live test · Живая проверка

English. Clean Joomla 6.2.0 full package, PHP 8.3.6, MariaDB 10.11.14, installed with `php installation/joomla.php install`. The pack was installed with `php cli/joomla.php extension:install --path=dist/kk-KZ_joomla_lang_full_6.2.0v1.zip`: three `kk-KZ` language extensions appeared (site, administrator, API). Kazakh was made the default for the site and the administrator (`com_languages` parameters), the admin user logged in, and 82 distinct addresses were requested with `tools/smoke_crawl.py`; 80 opened normally and two gave the expected 404 and 403 error pages, also in Kazakh. They covered: dashboards, article, category, tag, contact, banner, news feed, field, workflow, user, group and menu item forms, lists, global configuration, extensions, languages, scheduler, Smart Search, privacy, mail templates, system information, plus the public login, registration and search pages. None of them returned a PHP error, notice or untranslated language key (the only key-like text is the PHP setting name `PHP_SESSION_UPLOAD_PROGRESS` on the system information page). The web installer, started with `Accept-Language: kk-KZ` over the root archive, rendered in Kazakh. Not covered: JavaScript-driven parts, visual review, the API with a token.

Русский. Чистый полный пакет Joomla 6.2.0, PHP 8.3.6, MariaDB 10.11.14, установка командой `php installation/joomla.php install`. Пакет поставлен командой `php cli/joomla.php extension:install --path=dist/kk-KZ_joomla_lang_full_6.2.0v1.zip`: появились три языковых расширения `kk-KZ` (сайт, админка, API). Казахский сделан языком по умолчанию для сайта и админки (параметры `com_languages`), администратор вошёл, и с помощью `tools/smoke_crawl.py` запрошено 82 разных адреса; 80 открылись штатно, ещё два дали ожидаемые страницы ошибок 404 и 403, тоже на казахском. Охвачены: панели, формы статьи, категории, метки, контакта, баннера, ленты новостей, поля, процесса, пользователя, группы и пункта меню, списки, общая конфигурация, расширения, языки, планировщик, умный поиск, персональные данные, шаблоны писем, сведения о системе, а также публичные страницы входа, регистрации и поиска. Ни один не вернул ошибку PHP, замечание или неперекладённый языковой ключ (единственный текст, похожий на ключ, — имя настройки PHP `PHP_SESSION_UPLOAD_PROGRESS` на странице сведений о системе). Веб-установщик, запущенный с `Accept-Language: kk-KZ` поверх корневого архива, отрисовался на казахском. Не охвачено: части на JavaScript, визуальный осмотр, API с токеном.

## Interface check · Проверка интерфейса

English. The specialist's report was reproduced first: in headless Chromium (sidebar width 288 px) the label «Басқару панелінің модульдері» (28 characters) pushed its «+» button to the next line. After the fix `tools/sidebar_check.js` measures the sidebar of the running administrator: 4 expanded sections, 54 visible rows, none wraps and none loses its «+» button in the line. The script fails when it finds no sections, so a changed page structure cannot pass unnoticed. A label fits when it is up to about 24 characters.

Русский. Замечание специалиста сначала воспроизведено: в безголовом Chromium (ширина меню 288 пикселей) подпись «Басқару панелінің модульдері» (28 знаков) уводила кнопку «+» на следующую строку. После правки `tools/sidebar_check.js` измеряет боковое меню работающей админки: 4 раскрытых раздела, 54 видимые строки, ни одна не переносится и ни одна не теряет кнопку «+» в строке. Скрипт завершается ошибкой, если не нашёл разделов, поэтому изменившаяся структура страницы не пройдёт незамеченной. Подпись помещается, если в ней до 24 знаков.

English. Page titles were also checked on a phone-sized screen (394 px wide, headless Chromium): «Мақалалар: Мақаланы өңдеу» was clipped by the gear button, «Мақалалар: Өңдеу» fits. The same steps as in the report (a new article with the title «Қәңіғүһұө», alias «qaniguhuo») give the label «Тақырыбы *» on a clean Joomla 6.2.0.

Русский. Заголовки страниц проверены и на экране размером с телефон (394 пикселя, безголовый Chromium): «Мақалалар: Мақаланы өңдеу» обрезалось кнопкой с шестерёнкой, «Мақалалар: Өңдеу» помещается. Те же шаги, что в замечании (новая статья с заголовком «Қәңіғүһұө», алиас «qaniguhuo»), дают подпись «Тақырыбы *» на чистой Joomla 6.2.0.

## Language Filter scenario · Сценарий с фильтром языков

English. On a clean Joomla 6.2.0 with the System - Language Filter plugin on and Kazakh as the default site language, the package 6.2.0.1 reproduces the reported problem: the home page redirects to itself until the client gives up after 6 redirects. Installing 6.2.0.2 as an update publishes the Kazakh content language, and the home page answers 200 at `/index.php/kk`. On a multilingual site with another default language the content language stays unpublished (the installer only warns); on a site without the filter it is published. The update server: after the installed version was set back to 6.2.0.1, `php cli/joomla.php update:extensions:check` found 6.2.0.2 from `raw.githubusercontent.com`.

Русский. На чистой Joomla 6.2.0 с включённым плагином «Система — Фильтр языков» и казахским языком сайта по умолчанию пакет 6.2.0.1 воспроизводит описанную в замечании ошибку: главная страница переадресует сама на себя, пока клиент не сдаётся после 6 переадресаций. Установка 6.2.0.2 как обновления публикует казахский язык контента, и главная отвечает 200 по адресу `/index.php/kk`. На многоязычном сайте с другим языком по умолчанию язык контента остаётся неопубликованным (установщик только предупреждает); на сайте без фильтра он публикуется. Сервер обновлений: после возврата установленной версии к 6.2.0.1 команда `php cli/joomla.php update:extensions:check` нашла 6.2.0.2 на `raw.githubusercontent.com`.

## Update server · Сервер обновлений

English. The update feed needs `<client>0</client>`. Without it Joomla links the update to the administrator client (client_id 1), cannot find the installed package (client_id 0), stores the update with extension_id 0, and System → Update → Extensions never shows it. Checked on a clean Joomla 6.2.0 with the installed version set back to 6.2.0.1: without the line the page shows no row; with it the row appears and the update installs from the page (6.2.0.1 → 6.2.0.2, the archive is downloaded from the GitHub release, the installer script runs). When the translation list (simulated by a local file) and this feed both offer an update, the page shows one row. Joomla keeps an update server registered for an installed package even if a later version of the package drops it.

Русский. В файле обновлений нужен `<client>0</client>`. Без него Joomla привязывает обновление к клиенту «административный» (client_id 1), не находит установленный пакет (client_id 0), сохраняет обновление с extension_id 0, и «Система → Обновление → Расширения» его не показывает. Проверено на чистой Joomla 6.2.0 при установленной версии, возвращённой к 6.2.0.1: без этой строки страница не показывает ни одной строки, с ней строка появляется и обновление ставится прямо со страницы (6.2.0.1 → 6.2.0.2, архив скачивается с релиза на GitHub, сценарий установки выполняется). Когда общий список переводов (имитирован локальным файлом) и этот файл оба предлагают обновление, страница показывает одну строку. Joomla не снимает с установленного пакета сервер обновлений, даже если следующая версия пакета от него отказалась.
