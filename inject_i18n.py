import re
import os
import json
import subprocess
from bs4 import BeautifulSoup

def clean_html(html_str):
    # Normalize whitespaces
    return re.sub(r'\s+', ' ', html_str).strip()

def get_inner_html(tag):
    return "".join([str(c) for c in tag.contents])

# 1. Load existing translations
translations_file = 'js/translations.js'
existing_es = {}
max_t_num = 127 # default fallback

if os.path.exists(translations_file):
    # We run a small node snippet to print the JSON of translations
    # because it is a JS file and not pure JSON.
    eval_code = f"const fs = require('fs'); const vm = require('vm'); const code = fs.readFileSync('{translations_file}', 'utf8'); const trans = vm.runInNewContext(code + '\\ntranslations;'); console.log(JSON.stringify(trans['es']));"
    try:
        json_str = subprocess.check_output(['node', '-e', eval_code]).decode('utf-8')
        existing_es = json.loads(json_str)
        print(f"Loaded {len(existing_es)} existing Spanish translation keys.")
        # Find maximum key number
        for k in existing_es.keys():
            if k.startswith('t_') and k[2:].isdigit():
                max_t_num = max(max_t_num, int(k[2:]))
        print(f"Maximum sequential key number found: t_{max_t_num}")
    except Exception as e:
        print(f"Error loading existing translations: {e}. Starting fresh.")

# Dictionary to collect all final Spanish translations
final_es = existing_es.copy()
new_key_counter = max_t_num + 1

# List of tags to consider for translation
tags_to_translate = ["h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "button", "label", "option", "span", "a"]

# Define elements we should never translate (like icons, code, language selects, etc.)
ignored_classes = ["fa-", "icon-", "material-icons"]
ignored_tags = ["script", "style", "noscript", "svg", "path", "code", "select", "iframe"]

def should_translate(tag):
    # If the tag is an ignored tag, skip
    if tag.name in ignored_tags:
        return False
    
    # If the tag has any ignored class, skip
    if tag.has_attr('class'):
        for cls in tag['class']:
            if any(ic in cls for ic in ignored_classes):
                return False
                
    # If the tag has no text content, skip
    text = tag.get_text(strip=True)
    if not text:
        return False
        
    # Check if there is any alphabetic character
    if not any(c.isalpha() for c in text):
        return False
        
    # Ignore specific items like "-->" or "&rarr;" or similar arrows
    if text in ["&rarr;", "→", "←", "←", "»", "«", "×"]:
        return False
        
    # Check if any parent tag is in the translate list
    parent = tag.parent
    while parent:
        if parent.name in tags_to_translate:
            # The parent will be translated as a whole block, so skip this child tag
            return False
        parent = parent.parent
        
    return True

def process_html_file(file_path):
    global new_key_counter
    print(f"\nProcessing {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    soup = BeautifulSoup(html_content, 'html.parser')
    
    tagged_count = 0
    reused_count = 0
    new_count = 0
    
    # Find all elements matching the target tags
    for tag in soup.find_all(tags_to_translate):
        if not should_translate(tag):
            continue
            
        # Extract and clean inner HTML
        inner_html = get_inner_html(tag)
        cleaned_val = clean_html(inner_html)
        
        if not cleaned_val:
            continue
            
        # Check if the tag already has a data-i18n attribute
        if tag.has_attr('data-i18n'):
            key = tag['data-i18n']
            final_es[key] = cleaned_val
            tagged_count += 1
            continue
            
        # Try to find if this value is already mapped in our dictionary
        existing_key = None
        for k, v in final_es.items():
            if clean_html(v) == cleaned_val:
                existing_key = k
                break
                
        if existing_key:
            tag['data-i18n'] = existing_key
            reused_count += 1
        else:
            # Create a new key
            new_key = f"t_{new_key_counter}"
            tag['data-i18n'] = new_key
            final_es[new_key] = cleaned_val
            new_key_counter += 1
            new_count += 1
            
    # Save the updated HTML file
    # We output str(soup) back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
    print(f"Finished {file_path}: Tagged total {tagged_count + reused_count + new_count} elements.")
    print(f"  - Already tagged: {tagged_count}")
    print(f"  - Reused keys: {reused_count}")
    print(f"  - New keys created: {new_count}")

# Run for index.html and perfil.html
process_html_file('index.html')
process_html_file('perfil.html')

# Write the updated es translation dictionary to a temporary file
# to let the next script know the exact updated Spanish keys
with open('temp_updated_es.json', 'w', encoding='utf-8') as f:
    json.dump(final_es, f, ensure_ascii=False, indent=2)

print("\ni18n injection complete. New Spanish translation dictionary written to temp_updated_es.json.")
