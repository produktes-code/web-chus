#!/usr/bin/env bash
# Recupera los promos ORIGINALES del usuario desde el histórico de git.
#
# Por qué: assets/proxy/promo.<lang>.mp4 se sobrescribió con la salida del
# propio pipeline (commit 848ffb6). Si el montaje se alimentara de ahí, la
# apertura y el audio saldrían de un promo ya generado por nosotros y la
# apertura se realimentaría con las tarjetas viejas. El original (34.77s,
# 1280x720, con la locución de cada idioma) está en ad2a48f.
#
# Uso:  bash promo2/restore_originals.sh [directorio destino]
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${1:-${PROMO_TMP:-/tmp/promoV2}/original}"
COMMIT="ad2a48f"
LANGS="es ca en it de ru ja uk zh-CN ar"

mkdir -p "$DEST"
cd "$REPO"

for l in $LANGS; do
  out="$DEST/promo.$l.mp4"
  git show "$COMMIT:assets/proxy/promo.$l.mp4" > "$out"
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$out")
  size=$(du -h "$out" | cut -f1)
  printf '  %-6s %8s  %ss\n' "$l" "$size" "$dur"
done

echo
echo "Originales en: $DEST"
echo "Comprueba que la duración sea ~34.77s en los 10 idiomas antes de montar."
