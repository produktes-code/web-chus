import json
import time
import sys
import concurrent.futures
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

with open('index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

translations = {'es': {}}
counter = 1

tags_to_translate = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a', 'span', 'li', 'button', 'label', 'th', 'td', 'div']

for tag in soup.find_all(tags_to_translate):
    has_element_child = any(isinstance(child, type(tag)) for child in tag.children)
    if not has_element_child:
        text = tag.get_text(strip=True)
        if text and any(c.isalpha() for c in text):
            if not tag.has_attr('data-i18n'):
                key = f"t_{counter}"
                tag['data-i18n'] = key
                translations['es'][key] = text
                counter += 1

print(f"Found {len(translations['es'])} elements to translate.", flush=True)

languages = {
    'en': 'english',
    'de': 'german',
    'ru': 'russian',
    'ja': 'japanese',
    'uk': 'ukrainian',
    'zh-CN': 'chinese',
    'ar': 'arabic'
}

def translate_item(key, original, lang_code):
    translator = GoogleTranslator(source='es', target=lang_code)
    try:
        return key, translator.translate(original)
    except Exception as e:
        try:
            time.sleep(1)
            return key, translator.translate(original)
        except Exception as e_retry:
            print(f"Error translating {key}: {e_retry}", file=sys.stderr)
            return key, original

for lang_code, lang_name in languages.items():
    print(f"Translating to {lang_name} ({lang_code})...", flush=True)
    translations[lang_code] = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(translate_item, k, v, lang_code): k for k, v in translations['es'].items()}
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            key, trans = future.result()
            translations[lang_code][key] = trans
            if i % 25 == 0:
                print(f"Progress {lang_name}: {i}/{len(futures)}", flush=True)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))

import os
if not os.path.exists('js'):
    os.makedirs('js')

with open('js/translations.js', 'w', encoding='utf-8') as f:
    f.write("const translations = " + json.dumps(translations, ensure_ascii=False, indent=2) + ";\n")

print("Done!", flush=True)
