import http from 'http';
import { createReadStream, statSync, readFileSync } from 'fs';
import { join, normalize, extname } from 'path';
import { fileURLToPath } from 'url';
import { gzipSync } from 'zlib';

const ROOT = fileURLToPath(new URL('.', import.meta.url));
const PORT = process.argv[2] ? parseInt(process.argv[2], 10) : 8081;
const MIME = {
  '.html': 'text/html; charset=utf-8', '.htm': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8', '.json': 'application/json',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
  '.webp': 'image/webp', '.svg': 'image/svg+xml', '.ico': 'image/x-icon',
  '.mp4': 'video/mp4', '.webm': 'video/webm', '.mp3': 'audio/mpeg',
  '.wav': 'audio/wav', '.ttf': 'font/ttf', '.woff': 'font/woff', '.woff2': 'font/woff2',
};
const COMPRESSIBLE = new Set(['.html', '.htm', '.css', '.js', '.mjs', '.json', '.svg', '.txt']);
const gzipCache = new Map();

function getGzip(filePath, mtimeMs) {
  const cached = gzipCache.get(filePath);
  if (cached && cached.mtimeMs === mtimeMs) return cached.buf;
  const buf = gzipSync(readFileSync(filePath), { level: 6 });
  gzipCache.set(filePath, { mtimeMs, buf });
  return buf;
}

http.createServer((req, res) => {
  const urlPath = decodeURIComponent((req.url || '/').split('?')[0]);
  let filePath = normalize(join(ROOT, urlPath === '/' ? 'index.html' : urlPath));
  if (!filePath.startsWith(ROOT)) { res.writeHead(403); return res.end('403'); }
  let stat; try { stat = statSync(filePath); } catch { res.writeHead(404); return res.end('404'); }
  if (stat.isDirectory()) { try { stat = statSync(join(filePath, 'index.html')); filePath = join(filePath, 'index.html'); stat = statSync(filePath); } catch { res.writeHead(404); return res.end('404'); } }
  const ext = extname(filePath).toLowerCase();
  const type = MIME[ext] || 'application/octet-stream';
  const range = req.headers.range;
  const acceptsGzip = /\bgzip\b/.test(req.headers['accept-encoding'] || '');

  // Código y HTML siempre revalidan (las traducciones/lógica cambian a menudo);
  // assets estáticos (imagen/vídeo/audio/fuentes) se cachean una semana.
  const volatile = new Set(['.html', '.htm', '.js', '.mjs', '.json', '.css', '.txt']);
  const cacheControl = volatile.has(ext) ? 'no-cache, must-revalidate' : 'public, max-age=604800';

  const lastModified = stat.mtime.toUTCString();
  const baseHeaders = {
    'Content-Type': type,
    'X-Content-Type-Options': 'nosniff',
    'Cache-Control': cacheControl,
    'Last-Modified': lastModified,
  };

  if (req.headers['if-modified-since'] === lastModified) {
    res.writeHead(304, { 'Cache-Control': cacheControl, 'Last-Modified': lastModified });
    return res.end();
  }

  // Compresión gzip para texto (sin Range)
  if (acceptsGzip && COMPRESSIBLE.has(ext) && !range) {
    try {
      const gz = getGzip(filePath, stat.mtimeMs);
      res.writeHead(200, { ...baseHeaders, 'Content-Encoding': 'gzip', 'Vary': 'Accept-Encoding', 'Content-Length': gz.length });
      return res.end(gz);
    } catch { /* fallback a sin comprimir */ }
  }

  // Range (vídeo/audio)
  if (range) {
    const m = /bytes=(\d*)-(\d*)/.exec(range);
    if (m) {
      const start = m[1] ? parseInt(m[1], 10) : 0;
      const end = m[2] ? parseInt(m[2], 10) : stat.size - 1;
      const maxEnd = Math.min(end, stat.size - 1);
      res.writeHead(206, {
        ...baseHeaders,
        'Content-Range': `bytes ${start}-${maxEnd}/${stat.size}`,
        'Accept-Ranges': 'bytes', 'Content-Length': maxEnd - start + 1,
      });
      return createReadStream(filePath, { start, end: maxEnd }).pipe(res);
    }
  }

  res.writeHead(200, { ...baseHeaders, 'Content-Length': stat.size, 'Accept-Ranges': 'bytes' });
  createReadStream(filePath).pipe(res);
}).listen(PORT, '0.0.0.0', () => console.log(`[dev-server] http://localhost:${PORT} (gzip + range)`));
