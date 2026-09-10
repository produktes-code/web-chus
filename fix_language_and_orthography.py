import json
import subprocess

# Run node script to process js/translations.js
js_code = """
const fs = require('fs');
const vm = require('vm');

const fileContent = fs.readFileSync('./js/translations.js', 'utf8');
vm.runInThisContext(fileContent);

let fixes = 0;

if (translations.ca) {
    for (let k in translations.ca) {
        let val = translations.ca[k];
        if (typeof val === 'string') {
            if (val.includes('EMPRESAS')) {
                translations.ca[k] = val.replace(/EMPRESAS/g, 'EMPRESES');
                fixes++;
            }
            if (val.includes('empresas')) {
                translations.ca[k] = val.replace(/empresas/g, 'empreses');
                fixes++;
            }
            if (val.includes('REMESES')) {
                translations.ca[k] = val.replace(/REMESES/g, 'REMESTLES');
                fixes++;
            }
            if (val.includes('REMESAS')) {
                translations.ca[k] = val.replace(/REMESAS/g, 'REMESTLES');
                fixes++;
            }
        }
    }
}

const output = "const translations = " + JSON.stringify(translations, null, 4) + ";\\n";
fs.writeFileSync('./js/translations.js', output, 'utf8');
console.log("Orthography audit completed successfully. Total corrections made:", fixes);
"""

with open('scratch_fix_ortho.js', 'w', encoding='utf-8') as f:
    f.write(js_code)

res = subprocess.run(['node', 'scratch_fix_ortho.js'], capture_output=True, text=True)
print(res.stdout)

# Run verify_html.py to confirm key integrity
res_v = subprocess.run(['python3', 'verify_html.py'], capture_output=True, text=True)
print(res_v.stdout)
