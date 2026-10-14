# Maintaining the pack · Сопровождение пакета

## English

The pack follows Joomla releases: the first three numbers of the version (6.1.4) are the Joomla version, the fourth is the translation revision (6.1.4.2 is the second revision for Joomla 6.1.4).

1. Get the English originals of the new Joomla release: `python3 tools/kkpack.py fetch 6.1.5` (it downloads the full package and keeps only the language folders in `.cache/joomla-6.1.5`). For release candidates pass `--url` with the asset address.
2. See what changed: `python3 tools/kkpack.py status --en .cache/joomla-6.1.5`.
3. Bring the files into line: `python3 tools/kkpack.py sync --en .cache/joomla-6.1.5 --write`. New and changed keys come in English and are listed in `todo.tsv`; obsolete keys and files disappear; the order follows the original.
4. Translate the keys from `todo.tsv` directly in the `.ini` files, following [GLOSSARY.md](../GLOSSARY.md). Strings that must stay in English go into `docs/keep-english.txt`.
5. `python3 tools/kkpack.py check --en .cache/joomla-6.1.5` must report no errors.
6. `python3 tools/kkpack.py bump 6.1.5.1` writes the version into the manifests; update `CHANGELOG.md` and `CITATION.cff`.
7. `python3 tools/kkpack.py build` creates two archives in `dist/` and `SHA256SUMS`: the installable package (`..._full_...`) and the archive for unpacking into the Joomla root with the installer language (`..._root_...`). Tag the release with the pack version (`6.1.5.1`) and publish it: the `Release assets` workflow builds the archives and attaches them to the release (for an existing tag run it by hand from the Actions tab).
8. Smoke test on a clean Joomla (optional but recommended):
   ```bash
   php installation/joomla.php install --site-name=Test --admin-user="Admin User" --admin-username=admin --admin-password='a-long-password-12345' --admin-email=admin@example.kz --db-type=mysqli --db-host=127.0.0.1 --db-user=USER --db-pass=PASS --db-name=DB --db-prefix=jt_ --db-encryption=0
   php cli/joomla.php extension:install --path=/path/to/dist/kk-KZ_joomla_lang_full_6.1.5v1.zip
   mysql DB -e "UPDATE jt_extensions SET params = JSON_SET(params,'\$.administrator','kk-KZ','\$.site','kk-KZ') WHERE element='com_languages' AND type='component'"
   # put  public $live_site = 'http://127.0.0.1:8099';  into configuration.php, then:
   php -S 127.0.0.1:8099 -t /path/to/joomla &
   python3 tools/smoke_crawl.py --base http://127.0.0.1:8099 --user admin --password 'a-long-password-12345'
   ```
   The script logs in to the administrator, opens about 80 screens and reports PHP errors, raw language keys and non-200 answers.

9. Compare with the official translation and look at the interface (see [OFFICIAL.md](OFFICIAL.md)): `python3 tools/kkpack.py official ...` re-applies the adoption list and rebuilds the review tables; `node tools/sidebar_check.js --base http://127.0.0.1:8099 --user admin --password '...'` (after `npm i @sparticuz/chromium puppeteer-core`) renders the administrator sidebar in headless Chromium and reports labels that wrap or push the «+» button to the next line.

**Update server.** Sites check `updates/pkg_kk-KZ.xml` (served from `main`) for new versions. After the release workflow has attached the archives, run `python3 tools/kkpack.py feed`, then commit and push the file; push it only when the archive exists, otherwise sites will try to download a missing file. Entries for other Joomla minor versions are kept.

## Русский

Пакет идёт за выпусками Joomla: первые три числа версии (6.1.4) — версия Joomla, четвёртое — номер редакции перевода (6.1.4.2 — вторая редакция для Joomla 6.1.4).

1. Получите английские оригиналы нового выпуска: `python3 tools/kkpack.py fetch 6.1.5` (команда скачивает полный пакет и оставляет в `.cache/joomla-6.1.5` только языковые каталоги). Для release candidate укажите адрес файла в `--url`.
2. Посмотрите, что изменилось: `python3 tools/kkpack.py status --en .cache/joomla-6.1.5`.
3. Приведите файлы в соответствие: `python3 tools/kkpack.py sync --en .cache/joomla-6.1.5 --write`. Новые и изменённые ключи приходят по-английски и попадают в `todo.tsv`; устаревшие ключи и файлы исчезают; порядок следует оригиналу.
4. Переведите ключи из `todo.tsv` прямо в `.ini`, следуя [GLOSSARY.md](../GLOSSARY.md). Строки, которые должны остаться по-английски, добавьте в `docs/keep-english.txt`.
5. `python3 tools/kkpack.py check --en .cache/joomla-6.1.5` не должен показывать ошибок.
6. `python3 tools/kkpack.py bump 6.1.5.1` запишет версию в манифесты; обновите `CHANGELOG.md` и `CITATION.cff`.
7. `python3 tools/kkpack.py build` создаст в `dist/` два архива и `SHA256SUMS`: устанавливаемый пакет (`..._full_...`) и архив для распаковки в корень Joomla с языком установщика (`..._root_...`). Отметьте выпуск тегом с версией пакета (`6.1.5.1`) и опубликуйте его: workflow `Release assets` соберёт архивы и приложит их к релизу (для уже существующего тега запустите его вручную на вкладке Actions).
8. Дымовая проверка на чистой Joomla (необязательно, но рекомендуется): команды те же, что выше в английской части (установка Joomla из CLI, `extension:install`, казахский язык по умолчанию в параметрах `com_languages`, `live_site` в `configuration.php`, встроенный сервер PHP), затем `python3 tools/smoke_crawl.py --base http://127.0.0.1:8099 --user admin --password '...'`. Скрипт входит в админку, открывает около 80 экранов и сообщает об ошибках PHP, «сырых» языковых ключах и ответах не 200.
9. Сверка с официальным переводом и осмотр интерфейса (см. [OFFICIAL.md](OFFICIAL.md)): `python3 tools/kkpack.py official ...` заново применяет список заимствований и пересобирает таблицы для вычитки; `node tools/sidebar_check.js --base http://127.0.0.1:8099 --user admin --password '...'` (после `npm i @sparticuz/chromium puppeteer-core`) отрисовывает боковое меню админки в безголовом Chromium и сообщает о подписях, которые переносятся или сдвигают кнопку «+» на следующую строку.

**Сервер обновлений.** Сайты проверяют `updates/pkg_kk-KZ.xml` (отдаётся из `main`) на новые версии. Когда workflow выпуска приложил архивы, выполните `python3 tools/kkpack.py feed`, затем зафиксируйте и отправьте файл; отправляйте его только после появления архива, иначе сайты попробуют скачать несуществующий файл. Записи для других минорных версий Joomla сохраняются.
