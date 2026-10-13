<?php
/**
 * @package    Joomla.Language
 * @copyright  (C) 2026 Webmarka; основа — русский пакет JPath, Open Source Matters, Inc.
 * @license    GNU General Public License version 2 or later
 */

defined('_JEXEC') or die;

use Joomla\String\StringHelper;

/**
 * kk-KZ localise class.
 */
abstract class Kk_KZLocalise
{
	/**
	 * Казахский: после числительного существительное в единственном числе («5 мақала»),
	 * поэтому достаточно форм 0, 1 и «много».
	 */
	public static function getPluralSuffixes($count)
	{
		if ($count == 0) {
			return ['0'];
		}

		return [$count == 1 ? '1' : 'MORE'];
	}

	/**
	 * Транслитерация для алиасов: казахские буквы → латиница по правилам, близким к официальному алфавиту 2021 года
	 * (ә → a, ғ → g, қ → q, ң → n, ө → o, ұ → u, ү → u, һ → h, і → i), остальная кириллица — как в русском пакете.
	 */
	public static function transliterate($string)
	{
		$str = StringHelper::strtolower($string);
		$glyph_array = [
			'a'    => 'á,Á,α,ά,ą,Ą,ä,Ä,ā,а,ә',
			'b'    => 'β,б',
			'v'    => 'в',
			'g'    => 'γ,ğ,Ğ,ģ,ґ,г,ғ',
			'd'    => 'ď,Ď,đ,Đ,δ,ð,д',
			'e'    => 'ě,Ě,ε,έ,é,É,ë,Ë,ę,Ę,ē,е,є,э',
			'yo'   => 'ё',
			'zh'   => 'ж',
			'z'    => 'ž,Ž,ź,Ź,ζ,з',
			'i'    => 'í,Í,η,ή,ι,ί,į,и,і',
			'y'    => 'й,ý,Ý,ы',
			'k'    => 'к',
			'q'    => 'қ',
			'l'    => 'λ,Λ,ł,Ł,ľ,Ľ,ĺ,Ĺ,ļ,л',
			'm'    => 'μ,м',
			'n'    => 'ń,Ń,ň,Ň,ñ,Ñ,ņ,н,ң',
			'o'    => 'ó,Ó,ω,Ώ,ώ,ö,Ö,ő,Ő,ô,Ô,о,ө',
			'p'    => 'π,п',
			'r'    => 'ř,Ř,ŕ,Ŕ,ρ,р',
			's'    => 'š,Š,σ,ς,ś,Ś,ş,с',
			't'    => 'ť,Ť,τ,т',
			'u'    => 'ú,Ú,ů,Ů,υ,ύ,ϋ,Ü,ü,ű,Ű,ų,ū,ΰ,у,ұ,ү',
			'f'    => 'φ,ф',
			'h'    => 'х,һ',
			'ts'   => 'ц',
			'ch'   => 'ч',
			'sh'   => 'ш',
			'shch' => 'щ',
			''     => 'ъ,ь',
			'yu'   => 'ю',
			'ya'   => 'я',
			'ae'   => 'æ,Æ',
			'c'    => 'č,Č,ć,Ć,ç',
			'ks'   => 'ξ,Ξ',
			'ps'   => 'ψ,Ψ',
			'ss'   => 'ß',
			'x'    => 'χ',
			'eur'  => '€',
			'rub'  => '₽',
			'kzt'  => '₸',
			'usd'  => '$',
		];

		foreach ($glyph_array as $letter => $glyphs) {
			$glyphs = explode(',', $glyphs);
			$str = StringHelper::str_ireplace($glyphs, $letter, $str);
		}

		return preg_replace('#\&\#?[a-z0-9]+\;#ismu', '', $str);
	}

	/** Слова, которые поиск пропускает. */
	public static function getIgnoredSearchWords()
	{
		return ['және', 'мен', 'бен', 'пен', 'үшін', 'бұл', 'осы', 'сол', 'бар', 'жоқ', 'деп', 'да', 'де', 'та', 'те', 'ал', 'не', 'ма', 'ме', 'ба', 'бе'];
	}

	public static function getLowerLimitSearchWord()
	{
		return 3;
	}

	public static function getUpperLimitSearchWord()
	{
		return 200;
	}

	public static function getSearchDisplayedCharactersNumber()
	{
		return 200;
	}
}
