import re
import os
import json
import urllib.request
import urllib.parse
import time
import concurrent.futures
from bs4 import BeautifulSoup

# --- SERVICE DOSSIER DATA ---
serviceData = {
    'video': {
        'code': "// DOSSIER 01 - VÍDEO & SPOTS CINEMÁTICOS",
        'title': "Producción de Vídeo & Spots Cinemáticos",
        'desc': "CHUS BZN diseña y ejecuta producciones publicitarias de alto nivel, spots para televisión y marcas corporativas, filmación multicámara en plató y dirección técnica cinematográfica asistida por Inteligencia Artificial.",
        'specs': "<strong>Solución Comercial & Entregables:</strong><br/>• Masterización en resolución 4K/8K con espacio de color ACES y LUTs (.cube) propietarias de alta fidelidad.<br/>• Reducción de hasta un 60% en tiempos de previz y generación de planos complejos mediante ComfyUI & Wan 2.1.<br/>• <strong>Aplicación para el cliente:</strong> Campañas publicitarias masivas, videoclips y largometrajes con estándares de emisión cinematográfica internacional."
    },
    'sonido': {
        'code': "// DOSSIER 02 - POSTPRODUCCIÓN & SONIDO EBU R128",
        'title': "Postproducción de Sonido & Masterización EBU R128",
        'desc': "Ingeniería de mezcla sonoras, sonoridad homologada para televisión pública/privada (TV3, TVE1) y plataformas OTT de streaming internacional (Netflix, HBO, Amazon Prime).",
        'specs': "<strong>Solución Comercial & Entregables:</strong><br/>• Control de volumen (-23 LUFS) riguroso bajo la norma internacional EBU R128, evitando rechazos de emisión.<br/>• Limpieza y restauración espectral forense con iZotope RX11 y SpectraLayers Pro.<br/>• <strong>Aplicación para el cliente:</strong> Películas, series de doblaje, publicidad y podcasts premium."
    },
    'streaming': {
        'code': "// DOSSIER 03 - DIRECTOS, STREAMING & COBERTURA 360°",
        'title': "Directos, Streaming & Cobertura Broadcast 360°",
        'desc': "Arquitectura técnica de señal audiovisual en tiempo real para convenciones multinacionales, eventos deportivos, espectáculos y emisiones simultáneas en redes sociales.",
        'specs': "<strong>Solución Comercial & Entregables:</strong><br/>• Automatización de regiduría multimedia mediante OBS Studio, QLab y mezcladores físicos de video.<br/>• Control CCU de exposición y ajuste de color en tiempo real.<br/>• <strong>Aplicación para el cliente:</strong> Cobertura 360° sin latencia, streaming corporativo de alta disponibilidad y garantía de emisión ininterrumpida."
    },
    'dj': {
        'code': "// DOSSIER 04 - DJ SESSIONS, LIVE PERFORMANCE & REMEZCLAS",
        'title': "DJ Live Performance & Producción Musical",
        'desc': "Dirección y ejecución de sesiones de música avanzada para festivales, macroeventos corporativos e identidad sonora de recintos comerciales.",
        'specs': "<strong>Solución Comercial & Entregables:</strong><br/>• Operación con hardware profesional Pioneer de alta gama (DDJ1000 / Rekordbox).<br/>• Estudio acústico de sala y remezclas exclusivas de estudio adaptadas al perfil del evento.<br/>• <strong>Aplicación para el cliente:</strong> Eventos de gran formato, convenciones de marca y producción discográfica."
    },
    'web': {
        'code': "// DOSSIER 05 - DESARROLLO WEB & WEB APPS A MEDIDA",
        'title': "Desarrollo Web & Aplicaciones Interactivas",
        'desc': "Programación de aplicaciones web interactivas a medida, plataformas SaaS de alto rendimiento, landing pages comerciales e integración de pasarelas API de Inteligencia Artificial.",
        'specs': "<strong>Solución Comercial & Entregables:</strong><br/>• Código limpio en HTML5/JS/FastAPI/Electron optimizado para máxima velocidad de carga (FCP < 0.8s).<br/>• Diseño responsivo adaptado a todos los dispositivos móviles y escritorios.<br/>• <strong>Aplicación para el cliente:</strong> Punto de venta digital, automatización de procesos empresariales y presencia web corporativa de impacto."
    },
    'design': {
        'code': "// DOSSIER 06 - MOTION GRAPHICS & DISEÑO GRÁFICO",
        'title': "Motion Graphics & Identidad Visual",
        'desc': "Creación de elementos visuales animados 2D/3D, bumpers para canales de televisión, paquetes de continuidad gráfica para emisiones en vivo y diseño de marca.",
        'specs': "<strong>Solución Comercial & Entregables:</strong><br/>• Animaciones avanzadas en After Effects y Blender.<br/>• Composición fotográfica y gráfica de alta resolución.<br/>• <strong>Aplicación para el cliente:</strong> Imagen corporativa de alto impacto, promociones y gráficos para eventos."
    },
    'ia': {
        'code': "// DOSSIER 07 - IMPLANTACIÓN DE IA EMPRESARIAL",
        'title': "Implantación & Automatización de IA en Empresas",
        'desc': "Integración estratégica de Inteligencia Artificial Generativa, agentes autónomos para empresas y clonación biométrica vocal legal bajo normativa europea.",
        'specs': "<strong>Solución Comercial & Entregables:</strong><br/>• Blindaje y cumplimiento del protocolo europeo EU AI Act y derechos de voz.<br/>• Conexión de modelos multimodales (Claude, ChatGPT, Qwen, DeepSeek) en la infraestructura de la empresa.<br/>• <strong>Aplicación para el cliente:</strong> Reducción masiva de costes operativos, atención automatizada y generación de contenidos en segundos."
    },
    'formacion': {
        'code': "// DOSSIER 08 - FORMACIÓN & CONSULTORÍA TECNOLÓGICA",
        'title': "Formación & Consultoría Tecnológica",
        'desc': "Capacitación a medida para equipos de producción, productoras de televisión y empresas en herramientas emergentes de IA y workflows audiovisuales.",
        'specs': "<strong>Solución Comercial & Entregables:</strong><br/>• Programas intensivos de Vibe Coding, Prompting para vídeo y herramientas de IA.<br/>• Auditoría tecnológica presencial o remota para optimizar flujos de trabajo.<br/>• <strong>Aplicación para el cliente:</strong> Transformación digital rápida de equipos humanos e incremento directo de la productividad."
    }
}

languages = {
    'en': 'en', 'ca': 'ca', 'it': 'it', 'de': 'de', 'ru': 'ru',
    'ja': 'ja', 'uk': 'uk', 'zh-CN': 'zh-CN', 'ar': 'ar'
}

def translate_via_gtx(text_val, target_lang):
    if not text_val.strip():
        return text_val
    text_val = re.sub(r'\s+', ' ', text_val).strip()
    q = urllib.parse.quote(text_val)
    url = f"https://clients5.google.com/translate_a/t?client=dict&sl=es&tl={target_lang}&q={q}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5.0) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data:
                if isinstance(data, list) and len(data) > 0:
                    return data[0]
                elif isinstance(data, str):
                    return data
    except Exception as e:
        print(f"Error on translate '{text_val[:20]}' to {target_lang}: {e}")
    return text_val

# Load the current translations object from js/translations.js
translations_file = 'js/translations.js'
with open(translations_file, 'r', encoding='utf-8') as f:
    text = f.read()

# Evaluate JS in Node to parse it perfectly
import subprocess
eval_code = f"const fs = require('fs'); const vm = require('vm'); const code = fs.readFileSync('{translations_file}', 'utf8'); const trans = vm.runInNewContext(code + '\\ntranslations;'); console.log(JSON.stringify(trans));"
json_str = subprocess.check_output(['node', '-e', eval_code]).decode('utf-8')
translations = json.loads(json_str)

es = translations['es']

# 1. Add services keys to Spanish block
print("Adding service data keys to Spanish block...")
for key, values in serviceData.items():
    es[f"t_service_{key}_code"] = values['code']
    es[f"t_service_{key}_title"] = values['title']
    es[f"t_service_{key}_desc"] = values['desc']
    es[f"t_service_{key}_specs"] = values['specs']

# 2. Align video keys inside index.html and find their data-i18n tags
print("Aligning video keys in index.html...")
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
cards = soup.find_all(class_='video-card')
for idx, card in enumerate(cards):
    # Find h3 (title)
    h3 = card.find('h3')
    p_desc = card.find('p', class_='font-sans')
    # Find span (badge) - it is the first span in the card info header
    span_badge = card.find('span', class_='text-signal-red')
    
    if h3 and h3.has_attr('data-i18n'):
        card['data-title-key'] = h3['data-i18n']
    if span_badge and span_badge.has_attr('data-i18n'):
        card['data-badge-key'] = span_badge['data-i18n']
    if p_desc and p_desc.has_attr('data-i18n'):
        card['data-desc-key'] = p_desc['data-i18n']

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))
print("Successfully modified index.html video-card dataset elements.")

# 3. Translate missing or timeout-failed keys for all languages
# and translate the new service keys!
ignored_exact_values = ["CHUS BZN", "SGAE", "AISGE", "AEDYP", "AIE", "FastAPI", "FFmpeg", "OBS/QLab", "CCU", "v1.0.0 Stable", "v1.0.0 Stable // Electron + React", "v1.0.0 Stable // FastAPI + FFmpeg", "v1.0.0 Stable // LLM Multimodal"]

def clean_text(v):
    return re.sub(r'\s+', ' ', v).strip()

def protect_and_translate(key, val, lang_code):
    if val.strip() in ignored_exact_values:
        return val
    if not any(c.isalpha() for c in val):
        return val
        
    vars_found = re.findall(r'\$\{[^\}]+\}', val)
    tags_found = re.findall(r'<[^>]+>', val)
    
    temp_val = val
    for i, v in enumerate(vars_found):
        temp_val = temp_val.replace(v, f" _V{i}_ ")
    for i, t in enumerate(tags_found):
        temp_val = temp_val.replace(t, f" _T{i}_ ")
        
    trans = translate_via_gtx(temp_val, lang_code)
    
    for i, t in enumerate(tags_found):
        trans = re.sub(rf'\s*_T{i}_\s*', t, trans)
    for i, v in enumerate(vars_found):
        trans = re.sub(rf'\s*_V{i}_\s*', v, trans)
        
    return re.sub(r'\s+', ' ', trans).strip()

# Translate
def process_language(lang_code):
    print(f"Processing translations for {lang_code}...")
    lang_dict = translations.get(lang_code, {})
    
    patched_count = 0
    new_count = 0
    
    # We do a concurrent translation of keys
    keys_to_translate = []
    for key, es_val in es.items():
        lang_val = lang_dict.get(key, '')
        
        # If it is missing, or is identical to Spanish and not an ignored name
        is_missing = not lang_val
        is_same_as_spanish = (lang_val == es_val and es_val.strip() not in ignored_exact_values and any(c.isalpha() for c in es_val))
        
        if is_missing or is_same_as_spanish:
            keys_to_translate.append((key, es_val))
            
    if keys_to_translate:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = {
                executor.submit(protect_and_translate, k, v, lang_code): k
                for k, v in keys_to_translate
            }
            for future in concurrent.futures.as_completed(futures):
                key = futures[future]
                trans_val = future.result()
                lang_dict[key] = trans_val
                if key in translations.get(lang_code, {}):
                    patched_count += 1
                else:
                    new_count += 1
                    
    print(f"  Finished {lang_code}: added {new_count} new keys, patched {patched_count} failed/same keys.")
    # Align sorting
    sorted_dict = {}
    for k in sorted(es.keys(), key=lambda x: (x.startswith('t_nav'), int(x[2:]) if x.startswith('t_') and x[2:].isdigit() else 9999, x)):
        sorted_dict[k] = lang_dict.get(k, es[k])
    return lang_code, sorted_dict

# Process in parallel for languages
final_translations = {'es': es}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(process_language, languages.keys())
    for lang_code, sorted_dict in results:
        final_translations[lang_code] = sorted_dict

# Write back js/translations.js
output_js = "const translations = {\n"
langs_list = ['es', 'ca', 'en', 'it', 'de', 'ru', 'ja', 'uk', 'zh-CN', 'ar']
for lIdx, lang in enumerate(langs_list):
    output_js += f'  "{lang}": {{\n'
    lang_dict = final_translations[lang]
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
    
print("\nProcess complete! translations.js has been audited, patched, and service dossiers have been integrated.")
