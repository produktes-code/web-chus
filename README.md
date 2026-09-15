![Security Audit](https://img.shields.io/badge/Security_Audit-Passed_Level_4-brightgreen)

## API Keys
La BLOGGER_API_KEY expuesta en el código debe estar restringida en Google Cloud Console (HTTP referrers: https://www.chusbzn.com/* y https://chusbzn.com/*; restricción de API: solo Blogger API v3). La rotación la realiza el propietario.

## Auditoría de Seguridad
Este repositorio superó satisfactoriamente una auditoría de Nivel 4 (análisis estático, remediación de dependencias y linting de seguridad) con fecha **2026-07-21**.

## Desarrollo local
El sitio se sirve con un servidor Node con soporte de rangos (Range/206), imprescindible para la reproducción de los avances de vídeo en Safari/iOS. No usar `python3 -m http.server` (no responde 206 y deja los vídeos en el primer fotograma).

```bash
node srv.mjs 8081
# vista compartida (opcional)
npx --yes cloudflared tunnel --url http://localhost:8081
```

## Publicación
- GitHub Pages despliega desde la rama `main` (directorio raíz) hacia http://chusbzn.com y https://chusbzn.com.
- El fichero `.nojekyll` evita el preprocesado de Jekyll (imprescindible para servir `css/tailwind.css` y los vídeos tal cual).
