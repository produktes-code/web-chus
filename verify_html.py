import re
import json
import subprocess
from bs4 import BeautifulSoup

# Load translations.js
translations_file = 'js/translations.js'
eval_code = f"const fs = require('fs'); const vm = require('vm'); const code = fs.readFileSync('{translations_file}', 'utf8'); const trans = vm.runInNewContext(code + '\\ntranslations;'); console.log(JSON.stringify(trans));"
json_str = subprocess.check_output(['node', '-e', eval_code]).decode('utf-8')
translations = json.loads(json_str)

languages = list(translations.keys())
print(f"Loaded translation dictionary. Languages: {languages}")

# Target files
files = ['index.html', 'perfil.html', 'blog.html', 'post.html']
missing_count = 0

for file_path in files:
    print(f"\nChecking translations in {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    soup = BeautifulSoup(html, 'html.parser')
    
    # 1. Check data-i18n elements
    elements = soup.find_all(attrs={"data-i18n": True})
    for el in elements:
        key = el['data-i18n']
        for lang in languages:
            if key not in translations[lang]:
                print(f"  [ERROR] Key '{key}' (text: '{el.get_text(strip=True)[:30]}') not found in '{lang}' block!")
                missing_count += 1
                
    # 2. Check special dataset attributes on video cards (for index.html)
    if file_path == 'index.html':
        cards = soup.find_all(class_='video-card')
        for card in cards:
            for attr in ['data-title-key', 'data-badge-key', 'data-desc-key']:
                if card.has_attr(attr):
                    key = card[attr]
                    for lang in languages:
                        if key not in translations[lang]:
                            print(f"  [ERROR] VideoCard attr '{attr}' key '{key}' not found in '{lang}' block!")
                            missing_count += 1

print(f"\nAudit complete. Total missing keys: {missing_count}")
if missing_count == 0:
    print("SUCCESS: All translation keys are fully aligned and valid!")
else:
    print("WARNING: Some translation keys are missing. Please fix them.")
