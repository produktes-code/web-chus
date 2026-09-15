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

## Tarjetas de vídeo (8)

Cada tarjeta abre en el modal un **reproductor HTML5 uniforme** con el vídeo real del reel/short (`data-local` → `assets/full/…`, máxima calidad que sirve la plataforma, H.264/AAC, reproducido en la propia web sin plantilla de la red social). Solo si fallara el vídeo local se recurre al **embed oficial** (`https://www.instagram.com/reel/{id}/embed` o `https://www.youtube.com/embed/{id}`) como respaldo. El botón "Abrir en fuente original" enlaza el post oficial (`data-link`). Enlaces (formato "copiar enlace" de Instagram/YouTube, sin tokens de sesión `stkn`):

| Tarjeta | Plataforma | ID / URL |
| --- | --- | --- |
| America'n Job 🇺🇸 | Instagram | `https://www.instagram.com/reel/DQh86inDDTm/` |
| BRONX 1980 | Instagram | `https://www.instagram.com/reel/DZOoxthKQ7-/` |
| DORITOS A.C 🌋🧀 | Instagram | `https://www.instagram.com/reel/DIFPAaMKcAJ/` |
| COCA-COLA CREATIVITY 🥤🔥 | Instagram | `https://www.instagram.com/reel/DIB6gmPqn8E/` |
| VENENO (BreakBeat Mix) | YouTube | `https://www.youtube.com/shorts/sSIBsZEcKTk` |
| BIENVENIDOS A MI CIUDAD 🎭 | YouTube | `https://www.youtube.com/shorts/xsjyo_bV5RA` |
| KILLA — Deus Ex Machina 🎶🔥 | Instagram | `https://www.instagram.com/reel/DH_X3ZrML1h/` |
| NIKE WEREWOLF 🐺 | Instagram | `https://www.instagram.com/reel/DIG3CvtqKWl/` |

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