import re
import time
from deep_translator import MyMemoryTranslator

# Load translations.js
with open('js/translations.js', 'r') as f:
    text = f.read()

# Extract 'es' block
start_idx = text.find('"es": {')
if start_idx == -1:
    start_idx = text.find("'es': {")
    
brace_count = 0
end_idx = -1
for i in range(start_idx, len(text)):
    if text[i] == '{':
        brace_count += 1
    elif text[i] == '}':
        brace_count -= 1
        if brace_count == 0:
            end_idx = i
            break
es_block = text[start_idx:end_idx+1]

# Extract KVs
kvs = re.findall(r'"([a-zA-Z0-9_]+)"\s*:\s*"([^"]*)"', es_block)
print(f"Extracted {len(kvs)} keys from es block.")

def translate_lang(kvs_list, target_lang_code):
    print(f"Translating {len(kvs_list)} keys to {target_lang_code}...")
    translated_kvs = []
    translator = MyMemoryTranslator(source='es-ES', target=target_lang_code)
    
    for idx, (key, val) in enumerate(kvs_list):
        if not val.strip():
            translated_kvs.append((key, val))
            continue
            
        # Protect HTML tags and variables
        vars_found = re.findall(r'\$\{[^\}]+\}', val)
        tags_found = re.findall(r'<[^>]+>', val)
        
        temp_val = val
        for i, v in enumerate(vars_found):
            temp_val = temp_val.replace(v, f" __VAR_{i}__ ")
        for i, t in enumerate(tags_found):
            temp_val = temp_val.replace(t, f" __TAG_{i}__ ")
            
        # Translate
        try:
            trans = translator.translate(temp_val)
        except Exception as e:
            print(f"Error translating {key}: {e}")
            trans = temp_val
            
        # Restore HTML tags and variables
        for i, t in enumerate(tags_found):
            trans = re.sub(rf'\s*__TAG_{i}__\s*', t, trans)
        for i, v in enumerate(vars_found):
            trans = re.sub(rf'\s*__VAR_{i}__\s*', v, trans)
            
        # Clean up double spaces
        trans = re.sub(r'\s+', ' ', trans).strip()
        translated_kvs.append((key, trans))
        
        # Print progress every 20 keys
        if (idx + 1) % 20 == 0:
            print(f"  Translated {idx+1}/{len(kvs_list)} keys...")
            
        time.sleep(0.05) # Polite delay
        
    return translated_kvs

# Translate to Catalan (ca-ES) and Italian (it-IT)
ca_translated = translate_lang(kvs, 'ca-ES')
it_translated = translate_lang(kvs, 'it-IT')

# Format blocks
def format_block(lang, kvs_list):
    block = f'  "{lang}": {{\n'
    for k, v in kvs_list:
        v_esc = v.replace('"', '\\"')
        block += f'    "{k}": "{v_esc}",\n'
    # remove last comma
    if block.endswith(',\n'):
        block = block[:-2] + '\n'
    block += '  },\n'
    return block

ca_block = format_block('ca', ca_translated)
it_block = format_block('it', it_translated)

# We want to replace the previously injected ca and it blocks in translations.js,
# OR since translations.js already has the old ca and it blocks, we can just replace them!
# Let's locate the beginning of the "ca" block: "ca": {
# We will read translations.js and remove everything from the start of "ca": { to the end before };
# Let's find "ca": { in translations.js
ca_start_idx = text.find('  "ca": {')
if ca_start_idx == -1:
    ca_start_idx = text.find('  \'ca\': {')

if ca_start_idx != -1:
    # We remove everything from ca_start_idx to the end };
    # Let's find the closing }; of translations.js
    last_br_idx = text.rfind('};')
    if last_br_idx != -1:
        new_text = text[:ca_start_idx] + ca_block + it_block + text[last_br_idx:]
        with open('js/translations.js', 'w') as f:
            f.write(new_text)
        print("translations.js successfully updated with real Catalan (ca) and Italian (it) blocks!")
    else:
        print("Error: Could not find closing };")
else:
    print("Error: Could not find ca block start to replace.")
