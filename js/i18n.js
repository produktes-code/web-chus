document.addEventListener('DOMContentLoaded', () => {
    const langSelect = document.getElementById('lang-select');
    const mobileLangSelect = document.getElementById('mobile-lang-select');
    
    // SVG Flag Icons dictionary (100% official vector standards)
    const FLAG_SVGS = {
        'es': `<svg viewBox="0 0 750 500" class="w-5 h-3.5 rounded-sm inline-block shadow-sm align-middle"><rect width="750" height="500" fill="#c60b1e"/><rect y="125" width="750" height="250" fill="#ffc400"/></svg>`,
        'ca': `<svg viewBox="0 0 900 600" class="w-5 h-3.5 rounded-sm inline-block shadow-sm align-middle"><rect width="900" height="600" fill="#FFC400"/><rect y="66.67" width="900" height="66.67" fill="#C8102E"/><rect y="200" width="900" height="66.67" fill="#C8102E"/><rect y="333.33" width="900" height="66.67" fill="#C8102E"/><rect y="466.67" width="900" height="66.67" fill="#C8102E"/></svg>`,
        'en': `<svg viewBox="0 0 60 30" class="w-5 h-3.5 rounded-sm inline-block shadow-sm align-middle"><clipPath id="s"><path d="M0,0 v30 h60 v-30 z"/></clipPath><clipPath id="t"><path d="M30,15 h30 v15 z M30,15 h-30 v-15 z M30,15 h-30 v15 z M30,15 h30 v-15 z"/></clipPath><g clip-path="url(#s)"><path d="M0,0 v30 h60 v-30 z" fill="#012169"/><path d="M0,0 L60,30 M60,0 L0,30" stroke="#fff" stroke-width="6"/><path d="M0,0 L60,30 M60,0 L0,30" clip-path="url(#t)" stroke="#C8102E" stroke-width="4"/><path d="M30,0 v30 M0,15 h60" stroke="#fff" stroke-width="10"/><path d="M30,0 v30 M0,15 h60" stroke="#C8102E" stroke-width="6"/></g></svg>`,
        'it': `<svg viewBox="0 0 1500 1000" class="w-5 h-3.5 rounded-sm inline-block shadow-sm align-middle"><rect width="500" height="1000" fill="#009246"/><rect x="500" width="500" height="1000" fill="#ffffff"/><rect x="1000" width="500" height="1000" fill="#ce2b37"/></svg>`,
        'de': `<svg viewBox="0 0 5 3" class="w-5 h-3.5 rounded-sm inline-block shadow-sm align-middle"><rect width="5" height="3" fill="#000"/><rect y="1" width="5" height="2" fill="#D00"/><rect y="2" width="5" height="1" fill="#FFCE00"/></svg>`,
        'ru': `<svg viewBox="0 0 9 6" class="w-5 h-3.5 rounded-sm inline-block shadow-sm align-middle"><rect width="9" height="6" fill="#fff"/><rect y="2" width="9" height="4" fill="#0039a6"/><rect y="4" width="9" height="2" fill="#d52b1e"/></svg>`,
        'ja': `<svg viewBox="0 0 900 600" class="w-5 h-3.5 rounded-sm inline-block shadow-sm align-middle"><rect width="900" height="600" fill="#fff"/><circle cx="450" cy="300" r="180" fill="#bc002d"/></svg>`,
        'uk': `<svg viewBox="0 0 3 2" class="w-5 h-3.5 rounded-sm inline-block shadow-sm align-middle"><rect width="3" height="2" fill="#0057b7"/><rect y="1" width="3" height="1" fill="#ffd700"/></svg>`,
        'zh-CN': `<svg viewBox="0 0 900 600" class="w-5 h-3.5 rounded-sm inline-block shadow-sm align-middle"><rect width="900" height="600" fill="#ee1c25"/><circle cx="150" cy="150" r="45" fill="#ffde00"/></svg>`,
        'ar': `<svg viewBox="0 0 3 2" class="w-5 h-3.5 rounded-sm inline-block shadow-sm align-middle"><rect width="3" height="2" fill="#006c35"/></svg>`
    };

    const LANG_LABELS = {
        'es': { short: 'ES', full: 'ESPAÑOL' },
        'ca': { short: 'CA', full: 'CATALÀ' },
        'en': { short: 'EN', full: 'ENGLISH' },
        'it': { short: 'IT', full: 'ITALIANO' },
        'de': { short: 'DE', full: 'DEUTSCH' },
        'ru': { short: 'RU', full: 'РУССКИЙ' },
        'ja': { short: 'JA', full: '日本語' },
        'uk': { short: 'UK', full: 'УКРАЇНСЬКА' },
        'zh-CN': { short: 'ZH', full: '中文' },
        'ar': { short: 'AR', full: 'العربية' }
    };

    // Check if translations object exists
    if (typeof translations === 'undefined') {
        console.error("translations.js is missing or failed to load");
        return;
    }

    // Default language MUST BE SPANISH ('es')
    const defaultLang = 'es';
    let currentLang = localStorage.getItem('site_lang') || defaultLang;

    // Ensure default on load is Spanish if none explicitly chosen
    if (!localStorage.getItem('site_lang')) {
        currentLang = defaultLang;
        localStorage.setItem('site_lang', defaultLang);
    }

    // Initialize underlying select tags if present
    if (langSelect) langSelect.value = currentLang;
    if (mobileLangSelect) mobileLangSelect.value = currentLang;

    // Build custom styled dropdowns to render SVG flags INSIDE the dropdown list
    setupCustomDropdown(langSelect, false);
    setupCustomDropdown(mobileLangSelect, true);

    // Apply translations on load
    applyTranslations(currentLang);

    function setupCustomDropdown(selectEl, isMobile) {
        if (!selectEl) return;

        // Create container for custom dropdown
        const wrapper = document.createElement('div');
        wrapper.className = 'relative inline-block text-left lang-custom-dropdown';
        selectEl.parentNode.insertBefore(wrapper, selectEl);

        // Hide original select element visually while keeping it in DOM for sync
        selectEl.style.display = 'none';
        wrapper.appendChild(selectEl);

        // Trigger Button
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'bg-black/90 border border-white/20 text-white text-xs font-mono px-3 py-1.5 uppercase cursor-pointer outline-none hover:border-signal-red inline-flex items-center gap-2 transition-all rounded-sm shadow-md';
        button.innerHTML = `
            <span class="btn-flag inline-flex items-center"></span>
            <span class="btn-text font-bold"></span>
            <svg class="w-3 h-3 text-white/60 ml-0.5 transition-transform duration-200 chevron-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
        `;
        wrapper.appendChild(button);

        // Dropdown Options Menu
        const menu = document.createElement('div');
        menu.className = 'hidden absolute right-0 mt-1.5 w-60 sm:w-64 min-w-[240px] bg-black/95 border border-white/20 shadow-2xl backdrop-blur-md rounded-sm py-1.5 z-50 transition-all';
        wrapper.appendChild(menu);

        // Populate Menu items with real SVG flags
        Object.keys(LANG_LABELS).forEach(code => {
            const item = document.createElement('button');
            item.type = 'button';
            item.className = 'w-full text-left px-3.5 py-2.5 text-xs font-mono uppercase text-white/80 hover:text-white hover:bg-white/15 flex items-center justify-between whitespace-nowrap transition-colors border-b border-white/5 last:border-0 cursor-pointer';
            item.setAttribute('data-value', code);
            
            const info = LANG_LABELS[code];

            item.innerHTML = `
                <span class="flex items-center gap-2.5 whitespace-nowrap shrink-0">
                    <span class="inline-flex items-center shrink-0">${FLAG_SVGS[code]}</span>
                    <span class="font-bold text-white tracking-widest shrink-0 w-5 text-left">${info.short}</span>
                    <span class="text-white/30 font-light shrink-0">|</span>
                    <span class="font-medium text-white/90 shrink-0">${info.full}</span>
                </span>
                <span class="check-icon text-signal-red opacity-0 font-bold ml-3 shrink-0">✓</span>
            `;

            item.addEventListener('click', (e) => {
                e.stopPropagation();
                const selectedLang = code;
                selectEl.value = selectedLang;
                applyTranslations(selectedLang);
                if (langSelect && langSelect !== selectEl) langSelect.value = selectedLang;
                if (mobileLangSelect && mobileLangSelect !== selectEl) mobileLangSelect.value = selectedLang;
                closeAllMenus();
            });

            menu.appendChild(item);
        });

        // Toggle menu on click
        button.addEventListener('click', (e) => {
            e.stopPropagation();
            const isOpen = !menu.classList.contains('hidden');
            closeAllMenus();
            if (!isOpen) {
                menu.classList.remove('hidden');
                button.querySelector('.chevron-icon').style.transform = 'rotate(180deg)';
            }
        });

        // Store sync function on wrapper element
        wrapper.syncState = (lang) => {
            const info = LANG_LABELS[lang] || LANG_LABELS['es'];
            button.querySelector('.btn-flag').innerHTML = FLAG_SVGS[lang] || FLAG_SVGS['es'];
            button.querySelector('.btn-text').textContent = info.short;

            menu.querySelectorAll('button[data-value]').forEach(btn => {
                const isSelected = btn.getAttribute('data-value') === lang;
                const check = btn.querySelector('.check-icon');
                if (isSelected) {
                    btn.classList.add('bg-white/15', 'text-white', 'border-l-2', 'border-l-signal-red');
                    if (check) check.classList.remove('opacity-0');
                } else {
                    btn.classList.remove('bg-white/15', 'text-white', 'border-l-2', 'border-l-signal-red');
                    if (check) check.classList.add('opacity-0');
                }
            });
        };
    }

    function closeAllMenus() {
        document.querySelectorAll('.lang-custom-dropdown').forEach(wrapper => {
            const menu = wrapper.querySelector('div:not(.btn)');
            const chevron = wrapper.querySelector('.chevron-icon');
            if (menu) menu.classList.add('hidden');
            if (chevron) chevron.style.transform = 'rotate(0deg)';
        });
    }

    document.addEventListener('click', closeAllMenus);

    function applyTranslations(lang) {
        localStorage.setItem('site_lang', lang);
        document.documentElement.lang = lang; // update html lang attribute

        // Update all custom dropdown buttons & items
        document.querySelectorAll('.lang-custom-dropdown').forEach(wrapper => {
            if (wrapper.syncState) wrapper.syncState(lang);
        });

        const elements = document.querySelectorAll('[data-i18n]');
        
        elements.forEach(el => {
            const key = el.getAttribute('data-i18n');
            
            if (translations[lang] && translations[lang][key]) {
                const val = translations[lang][key];
                if (val.includes('<') || val.includes('&')) {
                    el.innerHTML = val;
                } else {
                    el.textContent = val;
                }
            } else if (translations[defaultLang] && translations[defaultLang][key]) {
                const val = translations[defaultLang][key];
                if (val.includes('<') || val.includes('&')) {
                    el.innerHTML = val;
                } else {
                    el.textContent = val;
                }
            }
        });

        // Trigger custom event for dynamic components (modals, video cards)
        window.dispatchEvent(new CustomEvent('site_lang_changed', { detail: { lang } }));
    }
});
