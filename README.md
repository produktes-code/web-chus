# CHUS BZN — Sitio web oficial

Sitio oficial y portfolio interactivo de **Jesús Ferrer García (CHUS BZN)**, Ingeniero de Sistemas Audiovisuales y especialista en integración de IA generativa (Barcelona).

- Producción: **https://chusbzn.com/** (GitHub Pages)
- Repositorio: **https://github.com/produktes-code/web-chus** (público)
- Rama de producción: `main` · Ramas espejo/backup: `dev-redesign`, `dev-red-design` · Rama histórica: `staging`

## Estructura

| Fichero | Contenido |
| --- | --- |
| `index.html` | Portada principal (manifiesto, servicios, 8 tarjetas de vídeo, retrato marquee/nameplate, timeline, compliance, formulario de contacto) |
| `perfil.html` | Perfil/trayectoria profesional (nameplate y cinta de créditos incluidos) |
| `blog.html` | Blog y novedades (consume la Blogger API) |
| `post.html` | Página de artículo del blog + sistema de comentarios local |
| `js/translations.js` | Diccionarios i18n (**10 idiomas, 511 claves por idioma**) |
| `js/i18n.js` | Motor de cambio de idioma y accesibilidad (persistencia en `localStorage`) |
| `css/tailwind.css` | Estilos (Tailwind compilado a fichero plano) + regla global `:focus-visible` |
| `assets/` | Previews ligeros (`.webp`), piezas íntegras en `assets/full/` (mp4), imágenes y favicon |
| `srv.mjs` | Servidor local: gzip, HTTP Range/206, caché y 304 (`If-Modified-Since`) |
| `CNAME` | `chusbzn.com` |
| `.nojekyll` | Evita el preprocesado Jekyll de GitHub Pages |

El sitio tiene **10 idiomas**: `es ca en it de ru ja uk zh-CN ar`.
Atributos de traducción (`data-i18n`): **241 únicos en `index.html`, 82 en `perfil.html`, 20 en `post.html`, 12 en `blog.html`**.

## Internacionalización (i18n)

El motor `js/i18n.js` soporta:

- **Texto** (`data-i18n`).
- **Placeholders** de formulario (`data-i18n-ph`).
- **aria-labels** (`data-i18n-aria`).
- **Meta description** (`data-i18n-desc`).
- **Contenido de meta tags** para redes (`data-i18n-content`): `og:title`, `og:description`, `twitter:title`, `twitter:description`.
- **`og:locale` dinámico** por idioma (`data-i18n-og-locale`): `es_ES ca_ES en_US it_IT de_DE ru_RU ja_JP uk_UA zh_CN ar_AR`.
- **`<title>`** de cada página traducido (`<title data-i18n="t_title_*">`).
- **Tipografías por script** (`#i18n-dir-css`): Noto Naskh Arabic para árabe, Noto Sans SC/PingFang para chino y Noto Sans JP para japonés.

Detalles de comportamiento:

- **Árabe sin espejar**: se marca `dir="rtl"` pero el CSS fuerza `direction: ltr; text-align: left`, de modo que la estructura (grid/flex, logo, hero) es idéntica al resto de idiomas. El texto árabe se compone correctamente por el algoritmo bidi.
- **Dropdown de idioma accesible**: botón con `aria-haspopup="listbox"`, `aria-expanded` (sincronizado al abrir/cerrar) y `aria-label` localizado (`t_aria_lang` + nombre del idioma). El `<select>` nativo se oculta pero se mantiene para sincronía y se le despacha un evento `change` nativo al elegir, para que los componentes dinámicos reaccionen.
- **Contenido inyectado** (blog/post): se expone `window.applySiteTranslations(lang)` para re-aplicar traducciones sobre HTML añadido después de la carga inicial (p. ej. comentarios renderizados por JS).
- **Cobertura completa** de texto hardcodeado (cita del manifiesto, métricas "33+", marquesinas, copyright del footer, placeholders, aria-labels, casos de estudio, menú móvil, footer del blog/post y UI de comentarios).
- El contenido de los artículos del blog proviene de la Blogger API y está redactado originalmente en español (no forma parte de los diccionarios de UI).

### Claves del diccionario

`js/translations.js` contiene **511 claves por idioma × 10 idiomas**. Las claves usan nombres semánticos (`t_mission`, `t_metric_*`, `t_marq_*`, `t_title_*`, `t_desc_*`, `t_form_*`, `t_modal_*`, `t_case1/2`, `t_comment_*`, `t_aria_*`, `t_ui_*`, `t_footer_*`…) además del bloque numerado histórico de Studio (`t_330..t_363`).

## Formulario de contacto

- Envío AJAX a **FormSubmit.co** (`https://formsubmit.co/ajax/info@chusbzn.com`) con `_subject`, `_template`, `_captcha:false` y `_replyto`.
- **Honeypot** anti-spam `_honey` (invisible, sin `label` de forma deliberada).
- Estados de éxito y error localizados (`t_form_ok` / `t_form_err`).
- Requiere **activar el destino** la primera vez (correo de "Activate Form"); en producción puede necesitar reactivación desde `chusbzn.com`.

## Comentarios del blog (`post.html`)

- Persistencia en `localStorage`, recuento y títulos localizados.
- Delegación del evento `submit` en `document` (guard `window.__commentsBound`), render con lookups frescos de DOM y `commentsStorageKey` a nivel de módulo: el formulario sobrevive a los re-render por cambio de idioma.
- Re-render estable al cambiar de idioma (sin bucles).

## Accesibilidad

- Imágenes con `alt`, botones con nombre accesible y `h1` única por página.
- `:focus-visible` global (contorno rojo de teclado) para enlaces, botones, inputs, selects, textarea, `summary` y elementos con `tabindex`.
- `aria-label` en los selects/dropdowns de idioma, navegación y modal.
- El único campo sin `label` visible es el honeypot `_honey` (esperado y fuera del flujo de foco).

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

## Imágenes

- Hero con `assets/vintage_mixing.webp` (sin marcas de agua ni estampado del logo).
- Conversión de imágenes a **WebP** para aligerar la carga (`vintage_mixing`, `camera_rig`, `consola_mezcla`, `mixing_console_bg`, `server_room`, `retrato_formal`, `blog_*`).
- Eliminado `broadcast_control.png` (en desuso).

## Blog (Blogger API)

- `index.html` / `blog.html` / `post.html` cargan los artículos con la **Blogger API v3**.
- `BLOGGER_BLOG_ID = "8737045333650211847"`
- `BLOGGER_API_KEY` está en el HTML (pública) y **debe permanecer restringida** en Google Cloud Console:

> Credenciales → Clave de API → Restricciones de aplicaciones: **Sitios web (referrers)** con 4 entradas:
> `https://chusbzn.com/*`, `http://chusbzn.com/*`, `https://*.chusbzn.com/*`, `http://*.chusbzn.com/*`
>
> Restricciones de API: **solo Blogger API v3**.

Mientras exista esa restricción, las peticiones que no lleguen desde `chusbzn.com` reciben `403 "Requests from referer … are blocked"` (comportamiento correcto: en `localhost` se usa el **fallback con contenido de ejemplo**). Nota: extensiones/privacy que eliminen la cabecera `Referer` impedirán cargar el blog a esos usuarios.

## Desarrollo local

El sitio **requiere** un servidor con soporte de rangos (HTTP Range/206) para la reproducción de los vídeos en Safari/iOS (en ordenadores también evita estados de vídeo pausado). **No usar** `python3 -m http.server`.

```bash
node srv.mjs 8081            # servidor local: gzip + Range/206 + caché/304
npx --yes cloudflared tunnel --url http://localhost:8081   # vista compartida (opcional)
```

Cabeceras de caché del servidor local:

- `index.html`, `.js`, `.css`, `.json`, `.txt` → `Cache-Control: no-cache, must-revalidate` (evita contenido obsoleto durante el desarrollo).
- Imágenes y demás assets → `Cache-Control: public, max-age=604800`.
- Soporte de `304 Not Modified` vía `Last-Modified` + `If-Modified-Since`.

## Publicación

- GitHub Pages despliega desde la rama **`main`**, directorio raíz.
- `CNAME = chusbzn.com`; HTTPS forzado y verificado en Pages.
- `www.chusbzn.com` redirige (301) al apex.
- `.nojekyll` es imprescindible: evita que Jekyll procese `css/tailwind.css` y los vídeos.
- Tras cada publicación se verifica byte a byte (SHA-256) local vs producción y se comprueba el estado `built` de Pages.

## Verificación (batería de pruebas)

Antes de publicar se ejecuta una batería automática (Chrome headless vía CDP) que comprueba:

- **i18n**: las 4 páginas × 10 idiomas (índice, perfil, blog, post) con 0 claves vacías/incorrectas y 0 errores JS.
- **Meta/redes**: `og:title`, `og:description`, `twitter:*`, `meta description` y `og:locale` correctos por idioma.
- **Responsive**: sin scroll horizontal a 390px y 756px en las 4 páginas.
- **Formularios**: contacto del index (payload, éxito y error) y comentario del post (persistencia y render).
- **Interacción**: cambio de idioma en contenido dinámico, modal de vídeo y menú móvil.
- **Enlaces**: solo el `403` esperado de la Blogger API en localhost.

## Documentos internos

`STRATEGIA.md` y `STRATEGIA_COPY.md` son documentos de trabajo internos y **no se publican** (excluidos en `.gitignore`).
