# AGENTS.md — Contexto de sesión (web chusbzn.com)

> Guardado el 2026-09-28 · Continuamos mañana. Todo lo marcado "verificado ✓" está comprobado en vivo vía CDP/OCR; no repetir.

## Qué es el proyecto
Web de **CHUS BZN** (`www.chusbzn.com`), una sola fuente con 4 páginas estáticas (Tailwind CDN + Vanilla JS, sin build):

| Página | Ruta | i18n clave |
|---|---|---|
| Home | `index.html` (>2860 líneas) | 331 `data-i18n` |
| Perfil | `perfil.html` | 45 |
| Blog | `blog.html` | 19 |
| Post | `post.html` | 30 |

- Previsualización local: `http://localhost:8971` (servida por `srv.mjs`, root con caché no cacheante — hay que recargar con force para ver cambios de vídeo).
- CDP/cabezas experimentales: `http://localhost:9223` (perfil Chrome dedicado, `localStorage.site_lang` persiste entre tests; un visitante real va a `en` por defecto).
- Origen Git: repo `a3e792a` en `/Users/jesusferrer/.gemini/antigravity-ide/scratch/web-chus`. **NO hay commits de este trabajo** (7 ficheros modificados + vídeos sin trackear, ver abajo). Pendiente decisión del usuario sobre commit.

## Mecánica i18n (JS)
- `js/translations.js` (cargado antes): objeto `translations[lang]`, **580 claves × 10 idiomas** (es, ca, en, it, de, ru, ja, uk, zh-CN, ar).
- `js/i18n.js` expone `window.applySiteTranslations(lang)` y gestiona el dropdown custom (clic en `.lang-custom-dropdown button[data-value="es|ca|en|..."]`); el `<select>` nativo NO dispara listener.
- Selectores en `applyTranslations`:
  - `[data-i18n]` → texto/HTML
  - `[data-i18n-ph]` → placeholder
  - `[data-i18n-alt]` → alt (nuevo en esta ronda, ~línea 209)
  - `[data-i18n-aria]` → aria-label
  - `[data-i18n-title]` → title (nuevo, ~línea 221)
  - meta (title/description/og)
- Modal servicios es dinámico: `window.openServiceModal(key)` (index ~2579) lee `t['t_service_${key}_code|title|desc|specs']` con fallback a `serviceData` hardcodeado (index 2477–2567, español) → escribe en `#modal-code/title/desc/specs`.
- post/blog tienen dict `labels` para la UI Blogger; **ambos ya incluyen `zh-CN`** (un `rg` dio 9 por artefacto de patrón, era 10).
- Los "dead keys" `t_1..t_127` son FALSO POSITIVO: los consumen vistas renderizadas por JS (perfil).
- Generador de traducciones: `tools/update_i18n.py` (CATALOG central) + regen → `js/translations.js`.

## Estado del trabajo (todo verificado ✓ salvo lo pendiente)

### Upgrade Hero/vídeo profesional (2026-10-01) ✓
- Objetivo del usuario: el promo del header "no es profesional, no representativo de la calidad". Referencias auditadas: `goagency.es` (hero full-bleed con Vimeo iframe, eyebrow+H1+CTA, H2 grandes, media-kit) y su spot Vimeo "Spot Go! Agency" `/video/1091617981` (57 s). Usuario dijo "procede como creas mejor, confío en ti".
- Descubrimiento: `assets/promo.mp4` (root, 1920×1080 @4.16 Mbps, 33.43 s) es un CORTE DISTINTO más comercial ("SERVICIO 01/08 VÍDEO CORPORATIVO …"/"08/08 CAMPAÑAS & IA") y solo ES. Los proxies servidos eran 960×540 → pixelados al escalar.
- Hecho: **re-render 10 promos localizadas a 1920×1080** (lanczos + unsharp + yuv420p, libx264 CRF18) → `/tmp/promo1080/`, reemplazadas en `assets/proxy/` (backup 960 en `/var/folders/n6/xwxnzz_54vv7rbz2qnl5zndw0000gn/T/opencode/backup_proxy_960/`). Audio copiado intacto (peak −1.1/−0.8 dB, RMS −15, sin barras). Poster regenerado 1920×1080 (backup `promo_poster.old.jpg`).
- **Hero rediseñado** (index ~855–906): full-bleed con `<video id="hero-spot">` autoplay muted loop playing `assets/proxy/promo.mp4` + overlay radial + contenido z-10 + specs strip + botón mute `#hero-spot-toggle`/`#hero-spot-toggle-label` (JS al final del index los conmuta 🔊/🔇). Se retiró el canvas matrix del hero. H2 de 7 secciones subidos a `text-5xl sm:text-7xl`.
- **IMPORTANTE**: la web usa `css/tailwind.css` PRECOMPILADO (v3.4.10). Las utilidades nuevas que NO existen ahí (`z-0`, `min-h-[92vh]`, `drop-shadow-*`, `bg-black/55`, `sm:right-10`, `max-w-[1600px]`) **NO se aplican**. Por eso el wrapper del vídeo computaba `position:relative` y no llenaba la sección. **Fix aplicado**: estilos `inline` en el hero (wrapper `position:absolute;inset:0;z-index:0`, min-height 94vh, text-shadows, z-index botón). Verificado CDP: wrapperPos `absolute`, wrapper 1440×846 == section, vídeo 1080p `cover`, 0 JS errors.
- QA final: OCR es intro (t=1.5 "TU NEGOCIO TIENE HISTORIAS QUE CONTAR/…") y CTA (t=33.5 "TU EMPRESA, EN PANTALLA/15% DE DTO/24/365") legibles a 1080p. T=4.4 = golpe (transición, esperado). Frames 6 s/12 s = metraje sin tarjetas ("NIKE" microtexto del footage, no overlay). OCR árabe no fiable (RTL). `node --check` OK; 11 ficheros promo HTTP 200; toggle/lang-swap OK.
- HTML servido con caché: recargar con que-force para ver el vídeo nuevo.

### Vídeo (QA ronda completada) ✓
- Pipeline final: `promo2/build_localized.sh` → 10 `assets/proxy/promo.{es,ca,en,it,de,ru,ja,uk,zh-CN,ar}.mp4` = **34.7 s**; `seg_open.$L` = 4.4 s; stream vídeo 34.6667 s; `assets/promo_poster.jpg` regenerado desde `promo.es`.
- `mkbeat <out> <src> <ss> <frames> <cropy>`; crop Y por segmento; **fix de open**: `mkopen` crop forzado `0:2333` (antes `$5` indefinido). `seg_08` fuente `veneno.mp4` a `ss=45` (eliminado texto "LG Liceu"; el texto residual al final es marca CHUS BZN).
- Audio: `adelay=2000`, `atrim=duration=34.7`, fades 2.2/1.3. Golpe musical en **4.40 s** (RMS 0.301) → coincide con corte texto→imágenes. `bed_faster.wav` de 40 s.
- Caras: seg_01 face box `[0.6201,0.3786,0.2060,0.3663]` → centrado (~0.44 desde top), no recortado. seg_06 'BRONX 1980' banner eliminado; seg_07 usa `web_beat.png` sin texto.
- OCR final: beats limpios; fotogramas cercanos localizados (ES+EN); promo t=30.3 limpia; t=12.5 muestra microtexto residual **"NKE"** del footage de seg_03 (contenido del metraje, no overlay — pendiente opcional).

### i18n (auditoría ronda completada) ✓
- Fijado: `ar` sin 5 `t_service_*_specs` → añadidas al CATALOG. Verificado en vivo: modal abre specs en árabe.
- Añadidas 6 claves sociales `t_ss_youtube/instagram/spotify/soundcloud/linkedin/github` ×10 → cableado `data-i18n-title` en index 791–811. Verificado es/ar/zh ("YouTube – Canal Oficial", árabe, chino).
- Añadidas 10 claves accesibilidad: `t_aria_dto`, `t_aria_menu`, `t_aria_open_menu`, `t_alt_sps/csp/bmc/rig/mixer/console`, `t_loading_post` ×10; nuevo mecanismo `data-i18n-alt`. Cableado: aria dto index 949; perfil 417/425; blog 397/424; post 495/520/529; alt index 1292/1305/1318, post 675/714/753; `data-i18n="t_loading_post"` post 561.
- Verificado en vivo (CDP): DTO marquee localizado es/ar/zh; aria dto; alt/title en es/ar/zh; perfil(ca) "Menú mòbil"/"Tanca el menú"; blog(en) "Mobile menu"/"Open menu"; post(ar/zh) nav/menu/mmenu; alt_rig árabe.
- **Aclaración crítica**: el "title/alt null en carga inicial" del análisis previo era artefacto de sesión CDP residual. Una navegación limpia aplica y persiste title/alt (comprobado con `cdp_poll2.mjs` y `cdp_bisect.mjs`). **No hay bug.**
- Paridad final: 580 claves × 10 idiomas, `node --check` OK en `js/translations.js`.

### Auditoría final de cadenas ✓
Barrido con regex (`<` inicio de tag + `>` fin, sufijos reales `data-i18n-aria/-ph/-alt/-title`): **0 cadenas de UI en español sin cablear**. Los 4 restantes son nombres propios INTENCIONALES:
- index 1486 `title="BIENVENIDOS A MI CIUDAD 🎭"` (nombre de pieza audiovisual; las tarjetas traducen su texto vía `data-i18n`/`data-title-key`).
- perfil 484/494/504 alts "Studio Pro Suite", "Cine Station Pro", "Brand Music Curator" (marcas puras, sin palabra localizable).
- (Mismo criterio en tooltips de tarjetas de vídeo: nombres de pieza, NO traducir.)

## Pendientes / decisiones mañana
0b. **Hero/vídeo (2026-10-01)**: upgrade completo (1080p + hero agencia) DONE y verificado (ver sección arriba). Quedan opciones en manos del usuario: (a) localizar el corte "services showcase" (`assets/promo.mp4`, ES 1080p) en los 10 idiomas para sustituir el montaje, (b) subir el spot a Vimeo (necesita su cuenta) e insertarlo como goagency, (c) decidir si el texto "NKE"/microtextos del footage molesta. Videos/sin commit.
0. **Pendiente en curso (2026-09-28, última sesión)**: usuario revisará la web paso a paso con instrucciones concretas — `http://localhost:8971/` · `/perfil.html` · `/blog.html` · `/post.html` (+ selector idioma arriba derecha). NO tocar redacción/estructura sin que él lo pida.
   - YA HECHO hoy: **anulada la foto B/N de Jesús Ferrer** (`assets/retrato_formal.webp`) en sus 2 ocurrencias: img `grayscale` del panel hero en `index.html` (~1666) y `div.perfil-photo-bg` (fondo hero, 756×1188) en `perfil.html:434` (toda la línea + el div). Verificado: 0 refs en ficheros ni DOM vivo (`site_lang` en localStorage del perfil CDP puede estar en 'ar'/'es'; resetear para capturas estables).
   - **Aviso de textos**: el árbol de trabajo difiere SUSTANCIALMENTE de HEAD (a3e792a) en `index.html` (bloque plataformas sociales "VER VÍDEOS → YouTube…" fue sustituido por tarjetas "VER QUÉ INCLUYE" por servicio) y `perfil.html` (contenido "TRAYECTORIA AUDITADA"/UCs FPCAT/LEGADO_JFB reemplazado por narrativa "Currículum"). Son cambios SIN commitear acumulados (no decididos). El 2026-09-28 se preguntó al usuario si restaurar → **dismissed**; prefiere revisar página a página y dar pasos concretos.
   - Estado de render verificado hoy: los `data-i18n` de las 4 páginas renderizan texto (0 spans vacíos).
1. **Commit**: 7 ficheros modificados (`index.html`, `perfil.html`, `blog.html`, `post.html`, `js/i18n.js`, `js/translations.js`, `css/tailwind.css`) + sin trackear `assets/promo.mp4`, `assets/promo_poster.jpg`, `assets/proxy/`, `AGENTS.md`. No se ha commiteado nada (no pedido). Ver `git status --short`.
2. **Opcional bajo riesgo**: microtexto residual "NKE" en seg_03 (footage, requeriría otra fuente/ss).
3. Publicación/despliegue del sitio (no iniciado).

## Comandos útiles
```bash
cd "/Users/jesusferrer/.gemini/antigravity-ide/scratch/web-chus"
node srv.mjs &                              # preview en :8971 (ya en marcha)
python3 tools/update_i18n.py                # regenera js/translations.js desde CATALOG
node --check js/translations.js js/i18n.js
# Build vídeo (si se vuelve a tocar el vídeo):
/var/folders/n6/xwxnzz_54vv7rbz2qnl5zndw0000gn/T/opencode/promo2/build_localized.sh <lan> <seg|all>
# Harneses CDP ya listos:
cd /var/folders/n6/xwxnzz_54vv7rbz2qnl5zndw0000gn/T/opencode
node cdp_audit.mjs   # verifica aria/alt/title/marquee/specs cross-lang (es/ar/zh)
node cdp_specs.mjs   # abre modal servicios en ar y lee #modal-specs
node cdp_poll2.mjs / cdp_bisect.mjs  # demo de que title/alt se aplican y persisten
# OCR de un fotograma:
ffmpeg -ss <t> -i <mp4> -frames:v 1 /tmp/f.png && swift ocr.swift /tmp/f.png ...
```

## Rutas clave
- Web: `/Users/jesusferrer/.gemini/antigravity-ide/scratch/web-chus`
- Build vídeo + assets temp (`promo2/`, `seg_*`, `web_beat.png`, `bed_faster.wav`): `/var/folders/n6/xwxnzz_54vv7rbz2qnl5zndw0000gn/T/opencode/promo2`
- Harneses CDP + `faces.swift` + OCR en `/tmp/ocr`: `/var/folders/n6/xwxnzz_54vv7rbz2qnl5zndw0000gn/T/opencode`
- Previews: `http://localhost:8971` · CDP `http://localhost:9223`

## Notas de entorno
- Plataforma macOS, zsh; uso OCR `swift ocr.swift <img>` visiones, no lectura de imágenes "nativas" del modelo.
- En CDP headless: `prefers-reduced-motion: reduce` → `boot()` de la matrix hace early-return (línea ~357 de i18n.js); no es bug real.
- Cámara: al cambiar idioma en CDP usar clics en `.lang-custom-dropdown button[data-value=...]`.