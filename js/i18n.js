document.addEventListener('DOMContentLoaded', () => {
    const langSelect = document.getElementById('lang-select');
    const mobileLangSelect = document.getElementById('mobile-lang-select');
    
    // Check if translations object exists (from translations.js)
    if (typeof translations === 'undefined') {
        console.error("translations.js is missing or failed to load");
        return;
    }

    // Default language
    const defaultLang = 'es';
    let currentLang = localStorage.getItem('site_lang') || defaultLang;

    // Initialize dropdowns
    if (langSelect) langSelect.value = currentLang;
    if (mobileLangSelect) mobileLangSelect.value = currentLang;

    // Apply translations on load
    applyTranslations(currentLang);

    // Event listeners
    if (langSelect) {
        langSelect.addEventListener('change', (e) => {
            const newLang = e.target.value;
            applyTranslations(newLang);
            if (mobileLangSelect) mobileLangSelect.value = newLang;
        });
    }

    if (mobileLangSelect) {
        mobileLangSelect.addEventListener('change', (e) => {
            const newLang = e.target.value;
            applyTranslations(newLang);
            if (langSelect) langSelect.value = newLang;
        });
    }

    function applyTranslations(lang) {
        localStorage.setItem('site_lang', lang);
        document.documentElement.lang = lang; // update html lang attribute

        const elements = document.querySelectorAll('[data-i18n]');
        
        elements.forEach(el => {
            const key = el.getAttribute('data-i18n');
            
            if (translations[lang] && translations[lang][key]) {
                // We use textContent because our translation tool used get_text(strip=True)
                // Using innerHTML might inject unsafe content or overwrite child elements, 
                // but since we only tagged leaf elements or simple wrappers, textContent is safer.
                el.textContent = translations[lang][key];
            } else if (translations[defaultLang] && translations[defaultLang][key]) {
                // Fallback to Spanish if translation is missing
                el.textContent = translations[defaultLang][key];
            }
        });
    }
});
