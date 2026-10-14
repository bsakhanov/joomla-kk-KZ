<?php

/**
 * @package     pkg_kk-KZ
 * @copyright   (C) 2026 Webmarka
 * @license     GNU General Public License version 2 or later
 *
 * Сценарий пакета казахского языка.
 *
 * Joomla, устанавливая язык сайта, сама создаёт для него «Язык контента» — но
 * неопубликованным. Если на сайте включён плагин «Система — Фильтр языков», а казахский
 * сделали языком сайта по умолчанию, фильтр не находит его префикс и бесконечно
 * перенаправляет главную на «//» (Undefined array key "kk-KZ" в LanguageFilter.php).
 * Сценарий публикует казахский язык контента там, где это безопасно, и предупреждает,
 * где решение остаётся за администратором.
 */

\defined('_JEXEC') or die;

use Joomla\CMS\Component\ComponentHelper;
use Joomla\CMS\Factory;
use Joomla\CMS\Installer\InstallerAdapter;
use Joomla\CMS\Installer\InstallerScriptInterface;
use Joomla\CMS\Plugin\PluginHelper;
use Joomla\Database\DatabaseInterface;

return new class () implements InstallerScriptInterface {
    public function install(InstallerAdapter $adapter): bool
    {
        return true;
    }

    public function update(InstallerAdapter $adapter): bool
    {
        return true;
    }

    public function uninstall(InstallerAdapter $adapter): bool
    {
        return true;
    }

    public function preflight(string $type, InstallerAdapter $adapter): bool
    {
        return true;
    }

    public function postflight(string $type, InstallerAdapter $adapter): bool
    {
        if (!\in_array($type, ['install', 'update', 'discover_install'], true)) {
            return true;
        }

        try {
            $app = Factory::getApplication();
            $db  = Factory::getContainer()->get(DatabaseInterface::class);

            $row = $db->setQuery(
                $db->createQuery()
                    ->select($db->quoteName(['lang_id', 'published']))
                    ->from($db->quoteName('#__languages'))
                    ->where($db->quoteName('lang_code') . ' = ' . $db->quote('kk-KZ'))
            )->loadObject();

            if (!$row || (int) $row->published === 1) {
                return true;
            }

            $filter  = PluginHelper::isEnabled('system', 'languagefilter');
            $default = (string) ComponentHelper::getParams('com_languages')->get('site', 'en-GB');

            // Одноязычный сайт (фильтр выключен) — опубликованный язык контента ничего не меняет
            // на сайте, но не даст сломать его потом. Казахский по умолчанию — публикуем обязательно
            if (!$filter || $default === 'kk-KZ') {
                $db->setQuery(
                    $db->createQuery()
                        ->update($db->quoteName('#__languages'))
                        ->set($db->quoteName('published') . ' = 1')
                        ->where($db->quoteName('lang_id') . ' = ' . (int) $row->lang_id)
                )->execute();

                // Список языков Joomla кэширует: без очистки фильтр ещё какое-то время видел бы старое состояние
                $caches = Factory::getContainer()->get(\Joomla\CMS\Cache\CacheControllerFactoryInterface::class);

                foreach (['com_languages', '_system'] as $group) {
                    $caches->createCacheController('callback', ['defaultgroup' => $group])->clean();
                }

                return true;
            }

            // Многоязычный сайт: публикация языка без главной страницы на нём — решение администратора
            $app->enqueueMessage(
                'Қазақ тілі «Мазмұн → Тілдер» тізімінде жарияланбаған. Қазақ тілін сайттың әдепкі тілі етуден бұрын оны жариялаңыз, әйтпесе «Жүйе — Тілдер сүзгісі» плагині басты бетті «//» мекенжайына шексіз қайта бағыттайды. / '
                . 'Kazakh is not published in Content → Languages. Publish it before making Kazakh the default site language, otherwise the System - Language Filter plugin redirects the home page to "//" in a loop.',
                'warning'
            );
        } catch (\Throwable $e) {
            // Сценарий не должен мешать установке перевода
        }

        return true;
    }
};
