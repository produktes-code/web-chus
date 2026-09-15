# CHUS BZN — Sitio web oficial

Sitio oficial y portfolio interactivo de **Jesús Ferrer García (CHUS BZN)**, Ingeniero de Sistemas Audiovisuales y especialista en integración de IA generativa (Barcelona).

- Producción en producción: **https://chusbzn.com/** (GitHub Pages)
- Rama de producción: `main` · Rama espejo/backup: `dev-redesign` · Rama histórica: `staging`

## Estructura

| Fichero | Contenido |
| --- | --- |
| `index.html` | Portada principal (manifiesto, servicios, 8 tarjetas de vídeo, retrato marquee/nameplate, timeline, compliance) |
| `perfil.html` | Perfil/trayectoria profesional (nameplate y cinta de créditos incluidos) |
| `blog.html` | Blog y novedades (consume la Blogger API) |
| `post.html` | Página de artículo del blog |
| `js/translations.js` | Diccionarios i18n (10 idiomas) |
| `js/i18n.js` | Motor de cambio de idioma (es/ca/en/it/de/ru/ja/uk/zh-CN/ar), persistencia en `localStorage` |
| `css/tailwind.css` | Estilos (Tailwind compilado a fichero plano) |
| `assets/` | Vídeos: previews ligeros (bucle de tarjeta) en `assets/` y piezas íntegras (máxima calidad) en `assets/full/`, imágenes, favicon |
| `srv.mjs` | Servidor local con soporte de rangos (Range/206) |
| `CNAME` | `chusbzn.com` |
| `.nojekyll` | Evita el preprocesado Jekyll de GitHub Pages |

El sitio tiene **10 idiomas**: `es ca en it de ru ja uk zh-CN ar`.
Atributos de traducción (`data-i18n`): 203 únicos en `index.html`, 66 en `perfil.html`, 13 en `post.html`, 9 en `blog.html`.

### Internacionalización (2026-09 añadida)

- **Módulo `js/i18n.js`** ampliado: además del texto (`data-i18n`) soporta **placeholders** (`data-i18n-ph`), **aria-labels** (`data-i18n-aria`) y **meta description** (`data-i18n-desc`).
- **RTL para árabe**: `dir="rtl"` automático cuando el idioma es `ar`; las marquesinas (`cine-marquee` y marquee de scroll) mantienen `direction:ltr` para preservar la animación.
- **Tipografías por script** (`#i18n-dir-css`): cliente de fuentes Noto/Naskh para árabe, Noto Sans SC/PingFang para chino y Noto Sans JP para japonés.
- **Título y meta description por idioma** en las 4 páginas (`<title data-i18n="t_title_*">` + `<meta ... data-i18n-desc="t_desc_*">`) con valores localizados.
- **Cobertura completa** del texto hardcodeado detectado en la auditoría: cita del manifiesto, métricas del "33+", marquesinas `CINE & BROADCAST / DIRECTOS & STREAMING / PRODUCCIÓN MUSICAL / VÍDEO CREATIVO / AUDIO · SONIDO` (index y perfil), copyright del footer, placeholders del formulario y aria-labels de navegación/idioma/menú/modal.
- Diccionario: **447 claves por idioma** (416 + 31 nuevas). Las claves nuevas usan nombres semánticos (`t_mission`, `t_metric_*`, `t_marq_*`, `t_copyright`, `t_ph_*`, `t_aria_*`, `t_(title|desc)_*`) para no colisionar con la numeración existente de la sección Studio de `perfil.html` (`t_330..t_363`).
- El contenido de los artículos del blog proviene de la Blogger API y está redactado originalmente en español (no forma parte de los diccionarios de UI).

## Tarjetas de vídeo (8)

Cada tarjeta abre en el modal un **reproductor HTML5 uniforme** con el vídeo real del reel (`data-local` → `assets/full/…`, reproducido en la propia web sin plantilla de la red social). Todos los vídeos del modal se sirven en **H.264/AAC a 1080×1920 (calidad uniforme)**: las piezas cuyo post publica 1440×2560 nativo (VENENO, BRONX 1980 y MI CIUDAD) se sirven en 1080 para igualar la serie, y las publicadas en 720×1280 (America'n Job, DORITOS, COCA-COLA, KILLA y NIKE — el techo real del servidor de Instagram, verificado incluso con sesión iniciada) se suben a 1080 con escalado de alta calidad (lanczos + unsharp), de modo que las 8 piezas quedan a la misma resolución. Solo si fallara el vídeo local se recurre al **embed oficial** (`https://www.instagram.com/reel/{id}/embed` o `https://www.youtube.com/embed/{id}`) como respaldo. El botón "Abrir en fuente original" enlaza el post oficial (`data-link`). Enlaces (formato "copiar enlace" de Instagram/YouTube, sin tokens de sesión `stkn`):

| Tarjeta | Plataforma | ID / URL |
| --- | --- | --- |
| America'n Job 🇺🇸 | Instagram | `https://www.instagram.com/reel/DQh86inDDTm/` |
| BRONX 1980 | Instagram | `https://www.instagram.com/reel/DZOoxthKQ7-/` |
| DORITOS A.C 🌋🧀 | Instagram | `https://www.instagram.com/reel/DIFPAaMKcAJ/` |
| COCA-COLA CREATIVITY 🥤🔥 | Instagram | `https://www.instagram.com/reel/DIB6gmPqn8E/` |
| VENENO (BreakBeat Mix) | Instagram | `https://www.instagram.com/reel/Da8mEpyAddG/` |
| BIENVENIDOS A MI CIUDAD 🎭 | YouTube | `https://www.youtube.com/shorts/xsjyo_bV5RA` |
| KILLA — Deus Ex Machina 🎶🔥 | Instagram | `https://www.instagram.com/reel/DH_X3ZrML1h/` |
| NIKE WEREWOLF 🐺 | Instagram | `https://www.instagram.com/reel/DIG3CvtqKWl/` |

## Animación y rendimiento

Vivacidad ambiental sin sobrecarga: se anima únicamente con **transform/opacity** (solo GPU, sin reflow ni re-rastreado) y no se añaden bucles extra de canvas.

- **Reveal por scroll** en escritorio (los `.reveal` entran con desvanecido/desplazamiento al cruzar el viewport, una sola vez) y en móvil se muestran directos para mantener la fluidez.
- **Titulares de sección**: subrayado rojo con latido y marcador `///` con parpadeo sutil, animados permanentemente, más un **glitch de entrada** (split RGB + skew) al revelarse su sección.
- **Iconos y grafismos**: los iconos de servicio y los imagotipos del ecosistema flotan con brillo orgánico (`animated-icon`, transform).
- **Aparición escalonada por rejillas**: contenidos (redes, servicios, ecosistema, metodología) entran en cascada —'*stagger*'— al revelarse su sección (retraso de 60ms por tarjeta, solo CSS + transform/opacity).
- **Parallax sutil del hero** (escritorio): titular y terminal/matrix se desplazan a velocidades distintas con el scroll (solo `transform`, throttled con `requestAnimationFrame`, listener `passive`).
- **Elevación al hover**: las tarjetas de servicio y los paneles de cristal se elevan ligeramente (transform de una capa, transición existente).
- **La matrix** gana vida con "astros" esporádicos: un rayo blanco brillante que cruza de vez en cuando una columna (muy ocasional, sin coste).
- **Previews de vídeo**: intactos (acceso y visualización sin tocar). Siguen pausándose al salir de pantalla.
- **Marquesina inicial**: con una segunda capa en **contracorriente** (misma cinta al 26% de opacidad, dirección opuesta) para dar profundidad.
- **Rótulo regenerado** (JESÚS FERRER GARCÍA): destello verde al completar cada ciclo del scramble.
- **Barra de progreso de scroll** (superior, `signal-red`): transform `scaleX`, escala en compositor.
- **Indicador REC** pulsante en las tarjetas de vídeo al estar en pantalla, en hover o al tocarlas (IntersectionObserver ligero, 8 nodos).
- Movimientos preexistentes conservados: orbes orgánicos, shimmer de titulares, la lluvia de la matrix (canvas con pausa fuera de pantalla y DPR limitado a 1.5 para aligerar retina), cinta de créditos lateral y nombre que se regenera (scramble), rotación de logs del terminal.
- **Nota:** las animaciones corren también con "Reducir movimiento" activado en el sistema (ajuste deliberado para este proyecto).

## Blog (Blogger API)

- `index.html` / `blog.html` / `post.html` cargan los artículos con la **Blogger API v3**.
- `BLOGGER_BLOG_ID = "8737045333650211847"`
- `BLOGGER_API_KEY` está en el HTML (pública) y **debe permanecer restringida** en Google Cloud Console:

> Credenciales → Clave de API → Restricciones de aplicaciones: **Sitios web (referrers)** con 4 entradas:
> `https://chusbzn.com/*`, `http://chusbzn.com/*`, `https://*.chusbzn.com/*`, `http://*.chusbzn.com/*`
>
> Restricciones de API: **solo Blogger API v3**.

Mientras exista esa restricción, las peticiones que no lleguen desde `chusbzn.com` reciben `403 "Requests from referer … are blocked"` (comportamiento correcto). Nota: extensiones/privacy que eliminen la cabecera `Referer` impedirán cargar el blog a esos usuarios.

## Desarrollo local

El sitio **requiere** un servidor con soporte de rangos (HTTP Range/206) para la reproducción de los vídeos en Safari/iOS (en ordenadores también evita estados de vídeo pausado). **No usar** `python3 -m http.server`.

```bash
node srv.mjs 8081            # servidor local con Range/206
npx --yes cloudflared tunnel --url http://localhost:8081   # vista compartida (opcional)
```

## Publicación

- GitHub Pages despliega desde la rama **`main`**, directorio raíz.
- `CNAME = chusbzn.com`; HTTPS forzado y verificado en Pages.
- `www.chusbzn.com` redirige (301) al apex.
- `.nojekyll` es imprescindible: evita que Jekyll procese `css/tailwind.css` y los vídeos.
- Tras cada publicación se verifica byte a byte (SHA-256) local vs producción y se comprueba el estado `built` de Pages.