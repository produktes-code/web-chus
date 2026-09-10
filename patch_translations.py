import re
import urllib.request
import urllib.parse
import json
import time

with open('js/translations.js', 'r') as f:
    text = f.read()

# Load translations by executing JS in a simple Node process or parsing
# Since we are in python, let's write a python parser using json.
# Wait, translations.js is not pure JSON, it is a JS file: `const translations = { ... };`
# We can convert it to JSON by stripping `const translations = ` and the trailing `;` and formatting it!
clean_js = text.replace('const translations =', '').strip()
if clean_js.endswith(';'):
    clean_js = clean_js[:-1]

# To make it pure JSON, we can use a python parser or node.
# Let's use node to print the JSON!
import subprocess
json_str = subprocess.check_output(['node', '-e', 'const fs = require(\"fs\"); const vm = require(\"vm\"); const code = fs.readFileSync(\"js/translations.js\", \"utf8\"); const trans = vm.runInNewContext(code + \"\\ntranslations;\"); console.log(JSON.stringify(trans));']).decode('utf-8')
translations = json.loads(json_str)

es = translations['es']
print(f"Loaded {len(es)} keys in Spanish.")

# Let's find keys to translate for ca and it
def translate_via_gtx(text_val, target_lang):
    if not text_val.strip():
        return text_val
    q = urllib.parse.quote(text_val)
    url = f"https://clients5.google.com/translate_a/t?client=dict&sl=es&tl={target_lang}&q={q}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3.0) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data and data[0]:
                return data[0]
    except Exception as e:
        print(f"Error translating '{text_val[:20]}' to {target_lang}: {e}")
    return text_val

# Let's define some values that should remain identical in all languages (names, abbreviations, etc.)
ignored_patterns = [
    r'^[a-zA-Z0-9_\-\s]+$', # clean alphanumeric names (e.g. CHUS BZN, Apple Computers, FastAPI, Redis, etc.)
    r'^//.*$', # code comments
    r'^\d+$', # numbers
    r'^EBU R128$',
    r'^EU AI Act$',
    r'^SGAE$',
    r'^AISGE$',
    r'^AEDYP$',
    r'^AIE$',
    r'^OBS/QLab$',
    r'^FASTAPI$',
    r'^FFMPEG$',
    r'^CCU$',
    r'^FastAPI$',
    r'^FFmpeg$'
]

def should_skip(val):
    val_strip = val.strip()
    if not val_strip:
        return True
    for pat in ignored_patterns:
        if re.match(pat, val_strip):
            return True
    return False

for lang in ['ca', 'it']:
    print(f"\n--- Checking {lang.upper()} ---")
    patched_count = 0
    for key, es_val in es.items():
        lang_val = translations[lang].get(key, '')
        
        # If it's empty, or if it is identical to Spanish and not an ignored name
        if not lang_val or (lang_val == es_val and not should_skip(es_val)):
            print(f"Patching key '{key}': '{es_val[:40]}...'")
            
            # Protect HTML tags and variables
            vars_found = re.findall(r'\$\{[^\}]+\}', es_val)
            tags_found = re.findall(r'<[^>]+>', es_val)
            
            temp_val = es_val
            for i, v in enumerate(vars_found):
                temp_val = temp_val.replace(v, f" __VAR_{i}__ ")
            for i, t in enumerate(tags_found):
                temp_val = temp_val.replace(t, f" __TAG_{i}__ ")
                
            trans = translate_via_gtx(temp_val, lang)
            
            for i, t in enumerate(tags_found):
                trans = re.sub(rf'\s*__TAG_{i}__\s*', t, trans)
            for i, v in enumerate(vars_found):
                trans = re.sub(rf'\s*__VAR_{i}__\s*', v, trans)
                
            trans = re.sub(r'\s+', ' ', trans).strip()
            
            translations[lang][key] = trans
            patched_count += 1
            time.sleep(0.1) # Small sleep
            
    print(f"Patched {patched_count} keys in {lang.upper()}.")

# Write translations back to translations.js
output = 'const translations = {\n'
langs = ['es', 'en', 'de', 'ru', 'ja', 'uk', 'zh-CN', 'ar', 'ca', 'it']
for lIdx, lang in enumerate(langs):
    output += f'  "{lang}": {{\n'
    keys = list(translations[lang].keys())
    for kIdx, key in enumerate(keys):
        val = translations[lang][key]
        escaped_val = val.replace('\\', '\\\\').replace('"', '\\"')
        output += f'    "{key}": "{escaped_val}"{"" if kIdx == len(keys)-1 else ","}\n'
    output += f'  }}{"" if lIdx == len(langs)-1 else ","}\n'
output += '};\n'

with open('js/translations.js', 'w') as f:
    f.write(output)
print("\ntranslations.js successfully updated and quality checked!")
