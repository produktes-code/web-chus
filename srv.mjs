import http from 'http';
import { createReadStream, statSync } from 'fs';
import { join, normalize, extname } from 'path';
import { fileURLToPath } from 'url';

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

http.createServer((req, res) => {
  const urlPath = decodeURIComponent((req.url || '/').split('?')[0]);
  let filePath = normalize(join(ROOT, urlPath === '/' ? 'index.html' : urlPath));
  if (!filePath.startsWith(ROOT)) { res.writeHead(403); return res.end('403'); }
  let stat; try { stat = statSync(filePath); } catch { res.writeHead(404); return res.end('404'); }
  if (stat.isDirectory()) { try { stat = statSync(join(filePath, 'index.html')); filePath = join(filePath, 'index.html'); } catch { res.writeHead(404); return res.end('404'); } }
  const type = MIME[extname(filePath)] || 'application/octet-stream';
  const range = req.headers.range;
  if (range) {
    const m = /bytes=(\d*)-(\d*)/.exec(range);
    if (m) {
      const start = m[1] ? parseInt(m[1], 10) : 0;
      const end = m[2] ? parseInt(m[2], 10) : stat.size - 1;
      const maxEnd = Math.min(end, stat.size - 1);
      res.writeHead(206, {
        'Content-Type': type, 'Content-Range': `bytes ${start}-${maxEnd}/${stat.size}`,
        'Accept-Ranges': 'bytes', 'Content-Length': maxEnd - start + 1,
        'Cache-Control': 'public, max-age=3600',
      });
      return createReadStream(filePath, { start, end: maxEnd }).pipe(res);
    }
  }
  res.writeHead(200, { 'Content-Type': type, 'Content-Length': stat.size, 'Accept-Ranges': 'bytes', 'Cache-Control': 'public, max-age=3600' });
  createReadStream(filePath).pipe(res);
}).listen(PORT, '0.0.0.0', () => console.log(`[dev-server] http://localhost:${PORT} (Range OK)`));