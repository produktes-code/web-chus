import re
import os
import json
import urllib.request
import urllib.parse
import time
import concurrent.futures

# 1. Load Spanish translations
with open('temp_updated_es.json', 'r', encoding='utf-8') as f:
    es_dict = json.load(f)

print(f"Loaded {len(es_dict)} Spanish keys to translate.")

# Define target languages
languages = {
    'en': 'English',
    'ca': 'Catalan',
    'it': 'Italian',
    'de': 'German',
    'ru': 'Russian',
    'ja': 'Japanese',
    'uk': 'Ukrainian',
    'zh-CN': 'Chinese',
    'ar': 'Arabic'
}

def translate_via_gtx(text_val, target_lang):
    if not text_val.strip():
        return text_val
    
    # Clean up multiple whitespaces to avoid URL issues
    text_val = re.sub(r'\s+', ' ', text_val).strip()
    
    # Google Translate clients5 API
    q = urllib.parse.quote(text_val)
    url = f"https://clients5.google.com/translate_a/t?client=dict&sl=es&tl={target_lang}&q={q}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5.0) as response:
            res_body = response.read().decode('utf-8')
            data = json.loads(res_body)
            if data:
                if isinstance(data, list) and len(data) > 0:
                    return data[0]
                elif isinstance(data, str):
                    return data
    except Exception as e:
        print(f"Error on translate '{text_val[:20]}' to {target_lang}: {e}")
        
    return text_val

# Protect HTML tags, variables, and specific technical keys (like email, website name, etc.)
ignored_exact_values = ["CHUS BZN", "SGAE", "AISGE", "AEDYP", "AIE", "FastAPI", "FFmpeg", "OBS/QLab", "CCU", "v1.0.0 Stable", "v1.0.0 Stable // Electron + React", "v1.0.0 Stable // FastAPI + FFmpeg", "v1.0.0 Stable // LLM Multimodal"]

def translate_single_key(key, val, lang):
    # If the value is a specific ignored technical string, return it as is
    if val.strip() in ignored_exact_values:
        return key, val
        
    # If value is purely numeric or special characters, return as is
    if not any(c.isalpha() for c in val):
        return key, val
        
    # Protect HTML tags and variables
    vars_found = re.findall(r'\$\{[^\}]+\}', val)
    tags_found = re.findall(r'<[^>]+>', val)
    
    temp_val = val
    for i, v in enumerate(vars_found):
        temp_val = temp_val.replace(v, f" _V{i}_ ")
    for i, t in enumerate(tags_found):
        temp_val = temp_val.replace(t, f" _T{i}_ ")
        
    translated = translate_via_gtx(temp_val, lang)
    
    # Restore HTML tags and variables
    for i, t in enumerate(tags_found):
        translated = re.sub(rf'\s*_T{i}_\s*', t, translated)
    for i, v in enumerate(vars_found):
        translated = re.sub(rf'\s*_V{i}_\s*', v, translated)
        
    # Clean up spaces
    translated = re.sub(r'\s+', ' ', translated).strip()
    return key, translated

# Dictionary to hold translations for all 10 languages
all_translations = {'es': es_dict}

# Process each language
for lang_code, lang_name in languages.items():
    print(f"\nTranslating to {lang_name} ({lang_code})...")
    lang_dict = {}
    
    # We translate in parallel using ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        # Submit all keys
        futures = {
            executor.submit(translate_single_key, k, v, lang_code): k
            for k, v in es_dict.items()
        }
        
        # Gather results with progress indicator
        total_keys = len(futures)
        completed = 0
        for future in concurrent.futures.as_completed(futures):
            key, trans = future.result()
            lang_dict[key] = trans
            completed += 1
            if completed % 30 == 0 or completed == total_keys:
                print(f"  Progress: {completed}/{total_keys} keys translated.")
                
    # Sort language dictionary by key to ensure perfect alignment
    sorted_lang_dict = {k: lang_dict.get(k, es_dict[k]) for k in sorted(es_dict.keys(), key=lambda x: (x.startswith('t_nav'), int(x[2:]) if x.startswith('t_') and x[2:].isdigit() else 9999, x))}
    all_translations[lang_code] = sorted_lang_dict
    time.sleep(0.5) # Polite delay between languages

# Write the final js/translations.js file
output_js = "const translations = {\n"
langs_list = ['es', 'ca', 'en', 'it', 'de', 'ru', 'ja', 'uk', 'zh-CN', 'ar'] # ca and it are now permanently present and ca is directly under es!

for lIdx, lang in enumerate(langs_list):
    output_js += f'  "{lang}": {{\n'
    lang_dict = all_translations[lang]
    keys = list(lang_dict.keys())
    for kIdx, key in enumerate(keys):
        val = lang_dict[key]
        escaped_val = val.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        comma = "" if kIdx == len(keys)-1 else ","
        output_js += f'    "{key}": "{escaped_val}"{comma}\n'
    comma_lang = "" if lIdx == len(langs_list)-1 else ","
    output_js += f'  }}{comma_lang}\n'
    
output_js += "};\n"

with open('js/translations.js', 'w', encoding='utf-8') as f:
    f.write(output_js)
    
print("\njs/translations.js successfully generated!")
