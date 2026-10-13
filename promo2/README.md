# promo2 — generación de los promos localizados (10 idiomas)

Rehace `assets/proxy/promo.<lang>.mp4` y `assets/promo.mp4` (copia ES) a partir de
los 8 clips de showcase en `assets/`, con **tarjeta de servicio** en cada plano.

## Qué resuelve

- **Titulación por servicio**: cada plano lleva una tarjeta con el **servicio** que el
  metraje ilustra (`SERVICIO 08` + «IA para tu comunicación»), no el nombre del
  proyecto. Los 16 nombres de servicio se extraen de `js/translations.js`
  (`t_service_<clave>_title`), ya traducidos en los 10 idiomas, así que no hay títulos
  duplicados que mantener.
- **Sin metraje raro**: se corta el tramo sin rótulo entre los proyectos y la oferta;
  la secuencia va directa a la tarjeta final «¿Hablamos de tu proyecto?».
- **Caras centradas**: el metraje es 9:16 vertical y antes se recortaba a 16:9, lo que
  descentraba las caras. Ahora el plano vertical se centra **completo** sobre un fondo
  desenfocado del propio clip; no se recorta nada.
- **Barra de servicio legible**: velo opaco (`#06060B` al 95 %) + filo rojo, con el
  texto generado por CoreText (`card.swift`) para que árabe (RTL + shaping) y CJK
  se dibujen correctamente — PIL/raqm no están disponibles en esta máquina.
- **Más ligero**: ~5,4 MB por idioma (antes ~8,5 MB) y 26,8 s (antes 34,8 s).

## Mapeo proyecto → servicio

Cada clip del showcase ilustra un servicio, no un nombre propio. El orden de los planos
es el de las tarjetas de `index.html` (`data-local`):

| # | Clip | Servicio | Nº |
|---|---|---|---|
| 1 | american_job | IA para tu comunicación | 08 |
| 2 | doritos | Spots para redes | 02 |
| 3 | cocacola | Postproducción & contenido con IA | 06 |
| 4 | veneno | Sonido & música para tu marca | 05 |
| 5 | barcelona_clown | Vídeo corporativo | 01 |
| 6 | bronx_1980 | Videoclips & música en vivo | 11 |
| 7 | killa_ig | Postproducción & contenido con IA | 06 |
| 8 | code_black_ig | Spots para redes | 02 |

El proyecto sigue identificándose en el propio metraje (el rótulo es parte del vídeo);
lo que cambia es el rótulo superpuesto, que ahora nombra el servicio.

## Uso

```bash
# 1) originales del usuario desde el histórico de git -> /tmp/promoV2/original
bash promo2/restore_originals.sh

# 2) títulos de servicio (lee js/translations.js) -> /tmp/promoV2/titles.json
python3 promo2/extract_titles.py

# 3) 80 tarjetas PNG (10 idiomas x 8 servicios)
swiftc -O promo2/card.swift -o /tmp/cardbin
python3 promo2/make_cards.py          # invoca /tmp/cardbin

# 4) montaje (los 10 idiomas, en paralelo o seguidos)
for lg in es ca en it de ru ja uk zh-CN ar; do python3 promo2/build_promos.py $lg & done; wait

# 5) instalar
for lg in es ca en it de ru ja uk zh-CN ar; do
  cp /tmp/promoV2/$lg/promo.$lg.mp4 assets/proxy/promo.$lg.mp4
done
cp /tmp/promoV2/es/promo.es.mp4 assets/promo.mp4
ffmpeg -y -ss 8 -i assets/promo.mp4 -frames:v 1 -q:v 3 assets/promo_poster.jpg
```

## ⚠️ Los originales no son `assets/proxy/`

`assets/proxy/promo.<lang>.mp4` **es la salida de este mismo pipeline**: se sobrescribe
en el paso 5. Si `build_promos.py` se alimentara de ahí, la apertura y el cierre saldrían
de un promo ya generado por nosotros, el montaje se realimentaría con las tarjetas
viejas y el resultado quedaría corrido (pasó: la apertura medía 8,8 s en vez de 4,4 s y
las tarjetas antiguas aparecían al principio).

Por eso la apertura, el cierre y el audio se leen de un directorio aparte:

- `PROMO_SRC` (por defecto `/tmp/promoV2/original`), que `restore_originals.sh` rellena
  desde el commit `ad2a48f`, donde los promos originales del usuario duran 34,766667 s.
- `build_promos.py` **aborta** si falta el original o si su duración no es 34,77 s, en
  lugar de continuar con un archivo contaminado.

## Estructura del montaje

| Tramo | Duración | Origen |
|---|---|---|
| Apertura («TU NEGOCIO TIENE HISTORIAS…») | 4,4 s | frames del promo original del idioma |
| 8 proyectos con tarjeta de servicio | 2,4–2,8 s c/u | `assets/<clip>.mp4` + tarjeta |
| Oferta («¿HABLAMOS DE TU PROYECTO?») | 2,57 s | frames del promo original del idioma |

El **audio** y los frames de apertura/cierre se toman siempre del promo original de cada
idioma, de modo que la locución y la música localizadas se conservan. Los 10 originales
duran exactamente 34,766667 s, por lo que los puntos de corte (`32,2 s`) son válidos
para todos.

Orden de los proyectos = orden de las tarjetas del showcase en `index.html`
(`data-local` → `data-title-key`).

## Requisitos

`ffmpeg` **con** `overlay` y `boxblur` (no necesita `drawtext`), `libx264`, Python 3 con
Pillow, y las herramientas de línea de comandos de Swift (solo para `card.swift`).
`Anton-Regular.ttf` va en `promo2/`; CoreText solo cubre alfabetos latinos, así que
árabe, cirílico y CJK usan la fuente del sistema para el shaping.
