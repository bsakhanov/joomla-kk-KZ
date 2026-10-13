# Maintaining the pack · Сопровождение пакета

## English

The pack follows Joomla releases: the first three numbers of the version (6.1.4) are the Joomla version, the fourth is the translation revision (6.1.4.2 is the second revision for Joomla 6.1.4).

1. Get the English originals of the new Joomla release: `python3 tools/kkpack.py fetch 6.1.5` (it downloads the full package and keeps only the language folders in `.cache/joomla-6.1.5`). For release candidates pass `--url` with the asset address.
2. See what changed: `python3 tools/kkpack.py status --en .cache/joomla-6.1.5`.
3. Bring the files into line: `python3 tools/kkpack.py sync --en .cache/joomla-6.1.5 --write`. New and changed keys come in English and are listed in `todo.tsv`; obsolete keys and files disappear; the order follows the original.
4. Translate the keys from `todo.tsv` directly in the `.ini` files, following [GLOSSARY.md](../GLOSSARY.md). Strings that must stay in English go into `docs/keep-english.txt`.
5. `python3 tools/kkpack.py check --en .cache/joomla-6.1.5` must report no errors.
6. `python3 tools/kkpack.py bump 6.1.5.1` writes the version into the manifests; update `CHANGELOG.md` and `CITATION.cff`.
7. `python3 tools/kkpack.py build` creates two archives in `dist/` and `SHA256SUMS`: the installable package (`..._full_...`) and the archive for unpacking into the Joomla root with the installer language (`..._root_...`). Tag the release with the pack version (`6.1.5.1`) and attach both files.

## Русский

Пакет идёт за выпусками Joomla: первые три числа версии (6.1.4) — версия Joomla, четвёртое — номер редакции перевода (6.1.4.2 — вторая редакция для Joomla 6.1.4).

1. Получите английские оригиналы нового выпуска: `python3 tools/kkpack.py fetch 6.1.5` (команда скачивает полный пакет и оставляет в `.cache/joomla-6.1.5` только языковые каталоги). Для release candidate укажите адрес файла в `--url`.
2. Посмотрите, что изменилось: `python3 tools/kkpack.py status --en .cache/joomla-6.1.5`.
3. Приведите файлы в соответствие: `python3 tools/kkpack.py sync --en .cache/joomla-6.1.5 --write`. Новые и изменённые ключи приходят по-английски и попадают в `todo.tsv`; устаревшие ключи и файлы исчезают; порядок следует оригиналу.
4. Переведите ключи из `todo.tsv` прямо в `.ini`, следуя [GLOSSARY.md](../GLOSSARY.md). Строки, которые должны остаться по-английски, добавьте в `docs/keep-english.txt`.
5. `python3 tools/kkpack.py check --en .cache/joomla-6.1.5` не должен показывать ошибок.
6. `python3 tools/kkpack.py bump 6.1.5.1` запишет версию в манифесты; обновите `CHANGELOG.md` и `CITATION.cff`.
7. `python3 tools/kkpack.py build` создаст в `dist/` два архива и `SHA256SUMS`: устанавливаемый пакет (`..._full_...`) и архив для распаковки в корень Joomla с языком установщика (`..._root_...`). Отметьте выпуск тегом с версией пакета (`6.1.5.1`) и приложите оба файла.
