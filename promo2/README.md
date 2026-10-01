# promo2 — generación de los promos localizados (10 idiomas)

Rehace `assets/proxy/promo.<lang>.mp4` y `assets/promo.mp4` (copia ES) a partir de
los 8 clips de showcase en `assets/`, con **tarjeta de servicio** en cada plano.

## Qué resuelve

- **Titulación por servicio**: cada plano lleva una tarjeta (`SERVICIO 0X/08` + nombre
  del proyecto). Los nombres se extraen de `js/translations.js` (`t_216`, `t_221`,
  `t_224`, `t_228`, `t_232`, `t_236`, `t_240`, `t_243`), que ya están traducidos en los
  10 idiomas, así que no hay Titles duplicados que mantener.
- **Sin metraje raro**: se corta el tramo sin rótulo entre los proyectos y la oferta;
  la secuencia va directa a la tarjeta final «¿Hablamos de tu proyecto?».
- **Caras centradas**: el metraje es 9:16 vertical y antes se recortaba a 16:9, lo que
  descentraba las caras. Ahora el plano vertical se centra **completo** sobre un fondo
  desenfocado del propio clip; no se recorta nada.
- **Barra de servicio legible**: velo opaco (`#06060B` al 95 %) + filo rojo, con el
  texto generado por CoreText (`card.swift`) para que árabe (RTL + shaping) y CJK
  se dibujen correctamente — PIL/raqm no están disponibles en esta máquina.
- **Más ligero**: ~5,5 MB por idioma (antes ~8,5 MB) y 26,8 s (antes 34,8 s).

## Uso

```bash
# 1) títulos (lee js/translations.js) -> /tmp/promoV2/titles.json
python3 promo2/extract_titles.py

# 2) 80 tarjetas PNG (10 idiomas x 8 servicios)
swiftc -O promo2/card.swift -o /tmp/cardbin
python3 promo2/make_cards.py          # invoca /tmp/cardbin

# 3) montaje (los 10 idiomas en paralelo)
for lg in es ca en it de ru ja uk zh-CN ar; do python3 promo2/build_promos.py $lg & done; wait

# 4) instalar
for lg in es ca en it de ru ja uk zh-CN ar; do
  cp /tmp/promoV2/$lg/promo.$lg.mp4 assets/proxy/promo.$lg.mp4
done
cp /tmp/promoV2/es/promo.es.mp4 assets/promo.mp4
ffmpeg -y -ss 8 -i assets/promo.mp4 -frames:v 1 -q:v 3 assets/promo_poster.jpg
```

## Estructura del montaje

| Tramo | Duración | Origen |
|---|---|---|
| Apertura («TU NEGOCIO TIENE HISTORIAS…») | 4,4 s | frames del promo nativo del idioma |
| 8 proyectos con tarjeta | 2,4–2,8 s c/u | `assets/<clip>.mp4` + tarjeta |
| Oferta («¿HABLAMOS DE TU PROYECTO?») | 2,57 s | frames del promo nativo del idioma |

El **audio** y los frames de apertura/cierre se toman siempre del promo nativo de cada
idioma (`assets/proxy/promo.<lang>.mp4`), de modo que la locución y la música
localizadas se conservan. Los 10 promos de origen duran exactamente 34,766667 s, por
lo que los puntos de corte (`32,2 s`) son válidos para todos.

Orden de los proyectos = orden de las tarjetas del showcase en `index.html`
(`data-local` → `data-title-key`).

## Requisitos

`ffmpeg` **con** `overlay` y `boxblur` (no necesita `drawtext`), `libx264`, Python 3 con
Pillow, y las herramientas de línea de comandos de Swift (solo para `card.swift`).
