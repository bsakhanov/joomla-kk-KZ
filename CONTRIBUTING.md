# Contributing · Участие · Қатысу

**English** · [Русский](#русский) · [Қазақша](#қазақша)

## English

Found a wrong, unclear or missing Kazakh string? Open an [issue](https://github.com/bsakhanov/joomla-kk-KZ/issues/new/choose) with the language key (for example `COM_CONTENT_ARTICLE_CONTENT`), the file, the current text and your proposal. Pull requests are welcome too:

1. Edit the `.ini` file in the right folder: `administrator/language/kk-KZ/`, `language/kk-KZ/`, `api/language/kk-KZ/` or `installation/language/kk-KZ/`. Keys and their order must stay as in Joomla.
2. Keep placeholders (`%s`, `%d`, `%1$s`, `{NAME}`) and HTML tags and links exactly as in the original; escape double quotes inside values as `\"`, or use «» in Kazakh text.
3. Follow [GLOSSARY.md](GLOSSARY.md). Use «» for quotation marks and a long dash (—); do not write words in capital letters for emphasis.
4. Run `python3 tools/kkpack.py check --en .cache/joomla-6.1.4` (fetch the original first with `python3 tools/kkpack.py fetch 6.1.4`) and make sure there are no errors.

By contributing you agree that your changes are licensed under GPL-2.0-or-later, like the rest of the pack.

## Русский

Нашли неверную, неясную или отсутствующую казахскую строку? Создайте [issue](https://github.com/bsakhanov/joomla-kk-KZ/issues/new/choose): укажите ключ (например, `COM_CONTENT_ARTICLE_CONTENT`), файл, текущий текст и своё предложение. Pull request тоже подойдёт:

1. Правьте `.ini` в нужном каталоге: `administrator/language/kk-KZ/`, `language/kk-KZ/`, `api/language/kk-KZ/` или `installation/language/kk-KZ/`. Ключи и их порядок остаются как в Joomla.
2. Заполнители (`%s`, `%d`, `%1$s`, `{NAME}`), HTML-теги и ссылки сохраняйте как в оригинале; двойные кавычки внутри значения экранируйте как `\"` или используйте «ёлочки» в казахском тексте.
3. Следуйте [GLOSSARY.md](GLOSSARY.md). Кавычки — «ёлочки», тире — длинное (—); капслоком слова не выделяйте.
4. Запустите `python3 tools/kkpack.py check --en .cache/joomla-6.1.4` (оригинал скачивается командой `python3 tools/kkpack.py fetch 6.1.4`) и убедитесь, что ошибок нет.

Внося правки, вы соглашаетесь, что они распространяются на условиях GPL-2.0-or-later, как и весь пакет.

## Қазақша

Қате, түсініксіз немесе жоқ қазақша жолды таптыңыз ба? [Issue](https://github.com/bsakhanov/joomla-kk-KZ/issues/new/choose) ашып, кілтті (мысалы, `COM_CONTENT_ARTICLE_CONTENT`), файлды, қазіргі мәтінді және өз ұсынысыңызды көрсетіңіз. Pull request те қабылданады:

1. `.ini` файлын тиісті қалтада өңдеңіз: `administrator/language/kk-KZ/`, `language/kk-KZ/`, `api/language/kk-KZ/` немесе `installation/language/kk-KZ/`. Кілттер мен олардың реті Joomla-дағыдай қалуы керек.
2. Толтырғыштарды (`%s`, `%d`, `%1$s`, `{NAME}`), HTML тегтері мен сілтемелерді түпнұсқадағыдай сақтаңыз; мән ішіндегі қос тырнақшаны `\"` деп экрандаңыз немесе қазақ мәтінінде «» қолданыңыз.
3. [GLOSSARY.md](GLOSSARY.md) ережелерін ұстаныңыз. Тырнақша — «», сызықша — ұзын (—); сөздерді бас әріптермен бөлектемеңіз.
4. `python3 tools/kkpack.py check --en .cache/joomla-6.1.4` пәрменін орындап (түпнұсқа `python3 tools/kkpack.py fetch 6.1.4` арқылы жүктеледі), қате жоқ екеніне көз жеткізіңіз.

Өзгерістер енгізу арқылы олардың бүкіл пакет сияқты GPL-2.0-or-later шарттарымен таратылуына келісесіз.
