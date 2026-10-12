#!/usr/bin/env bash
# Lanzador del preview local de CHUS BZN. Desacopla el servidor para que NO se
# muera al cerrar la terminal o la sesión (era el motivo de los "localhost que
# fallan"). Uso:  ./preview.sh [start|stop|restart|status]
set -u
cd "$(dirname "$0")"
PORT="${PREVIEW_PORT:-8081}"
PIDFILE="/tmp/chusbzn-preview-$PORT.pid"
LOG="/tmp/chusbzn-preview.log"
IP="$(ipconfig getifaddr en1 2>/dev/null || echo '')"

running() { [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE" 2>/dev/null)" 2>/dev/null; }

case "${1:-start}" in
  start)
    if running; then echo "ya está corriendo (PID $(cat "$PIDFILE"))"; exit 0; fi
    nohup node srv.mjs "$PORT" >"$LOG" 2>&1 &
    echo $! > "$PIDFILE"
    disown 2>/dev/null || true
    sleep 1
    if running; then
      echo "preview listo:"
      echo "  local  -> http://localhost:$PORT/"
      [ -n "$IP" ] && echo "  movil  -> http://$IP:$PORT/"
    else
      echo "ERROR al arrancar; revisa $LOG"; tail -n 20 "$LOG"; exit 1
    fi
    ;;
  stop)
    if running; then kill "$(cat "$PIDFILE")" && rm -f "$PIDFILE" && echo "parado"; else echo "no estaba corriendo"; fi
    ;;
  restart) "$0" stop; sleep 1; "$0" start ;;
  status)
    if running; then
      echo "corriendo (PID $(cat "$PIDFILE"))"
      echo "  local -> http://localhost:$PORT/"
      [ -n "$IP" ] && echo "  movil -> http://$IP:$PORT/"
    else echo "parado"; fi
    ;;
  *) echo "uso: $0 [start|stop|restart|status]"; exit 1 ;;
esac
