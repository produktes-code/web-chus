
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

const output = "const translations = " + JSON.stringify(translations, null, 4) + ";\n";
fs.writeFileSync('./js/translations.js', output, 'utf8');
console.log("Orthography audit completed successfully. Total corrections made:", fixes);
