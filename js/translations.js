/* CHUS BZN — cargador i18n.
   Carga ÚNICAMENTE el diccionario del idioma activo más el español (base de
   respaldo), en lugar del bundle completo de 10 idiomas (~710 KB). Los
   diccionarios viven en js/translations/<lang>.js.

   Los ficheros se insertan de forma síncrona (parser-blocking) con
   document.write, de modo que `translations` queda disponible exactamente
   igual que antes: para cuando se ejecuta js/i18n.js y el resto de scripts
   inline de la página. Al cambiar de idioma en la UI, js/i18n.js carga el
   fichero que falte bajo demanda. */
(function () {
    var SUPPORTED = ['es', 'ca', 'en', 'it', 'de', 'ru', 'ja', 'uk', 'zh-CN', 'ar'];
    var DEFAULT = 'es';

    var lang = DEFAULT;
    try { lang = localStorage.getItem('site_lang') || DEFAULT; } catch (e) {}
    if (SUPPORTED.indexOf(lang) === -1) lang = DEFAULT;

    // El español siempre va primero (respaldo de claves ausentes).
    var langs = (lang === DEFAULT) ? [DEFAULT] : [DEFAULT, lang];
    var base = 'js/translations/';
    for (var i = 0; i < langs.length; i++) {
        document.write('<script src="' + base + langs[i] + '.js"><\/script>');
    }
})();
