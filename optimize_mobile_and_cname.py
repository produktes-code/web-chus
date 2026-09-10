import os
import re

print("=== OPTIMIZING FOR IPHONE MOBILE & REMOVING CNAME ===")

# 1. Delete CNAME file if exists
cname_path = "/Users/jesusferrer/.gemini/antigravity-ide/scratch/web-chus/CNAME"
if os.path.exists(cname_path):
    os.remove(cname_path)
    print("✅ Deleted CNAME file so GitHub Pages doesn't redirect to chusbzn.com")

# 2. Update index.html for Mobile Reveal, Matrix Canvas, and GPU Orbs
index_path = "/Users/jesusferrer/.gemini/antigravity-ide/scratch/web-chus/index.html"
with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

# CSS Fix for Mobile Reveal & Organic Orbs Performance
css_fix = """
    /* Mobile Reveal Fallback & GPU Acceleration */
    @media (max-width: 1024px) {
        .reveal {
            opacity: 1 !important;
            transform: none !important;
            transition: none !important;
        }
        .organic-orb-1, .organic-orb-2 {
            display: none !important;
        }
    }

    /* Optimized Organic Orbs Keyframes without blur re-rasterization */
    @keyframes organic-morph {
        0% { transform: translate3d(0, 0, 0) scale(1); }
        50% { transform: translate3d(30px, -20px, 0) scale(1.06); }
        100% { transform: translate3d(-20px, 20px, 0) scale(0.95); }
    }
"""

if "/* Mobile Reveal Fallback" not in html:
    html = html.replace("/* Scroll reveal */", css_fix + "\n    /* Scroll reveal */")

# Matrix Rain Engine with ResizeObserver and RequestAnimationFrame
new_matrix_js = """    // ═══ BULLETPROOF MATRIX DATA STREAM CANVAS (MOBILE & DESKTOP) ═══
    const mCanvas = document.getElementById('matrix-canvas');
    if (mCanvas) {
        const ctx = mCanvas.getContext('2d');
        const chars = 'CHUSBZN0123456789EBUR128AI@#$890';
        const fontSize = 12;
        let columns = 0;
        let drops = [];
        let curW = 0, curH = 0;

        function updateCanvasDimensions() {
            const parent = mCanvas.parentElement;
            const w = (parent && parent.clientWidth) ? parent.clientWidth : (window.innerWidth < 480 ? 320 : 360);
            const h = (parent && parent.clientHeight) ? parent.clientHeight : 256;
            
            if (curW !== w || curH !== h || mCanvas.width !== w || mCanvas.height !== h) {
                curW = w;
                curH = h;
                mCanvas.width = w;
                mCanvas.height = h;
                columns = Math.max(10, Math.floor(w / fontSize));
                drops = Array(columns).fill(0).map(() => Math.floor(Math.random() * -25));
            }
        }

        updateCanvasDimensions();
        window.addEventListener('resize', updateCanvasDimensions);
        window.addEventListener('orientationchange', () => setTimeout(updateCanvasDimensions, 200));

        if (window.ResizeObserver && mCanvas.parentElement) {
            try {
                new ResizeObserver(() => updateCanvasDimensions()).observe(mCanvas.parentElement);
            } catch (e) {}
        }

        let lastDrawTime = 0;
        const fpsInterval = 35; // ~30 FPS throttle

        function renderMatrix(timestamp) {
            requestAnimationFrame(renderMatrix);

            if (timestamp - lastDrawTime < fpsInterval) return;
            lastDrawTime = timestamp;

            if (!curW || !curH || mCanvas.width !== curW) {
                updateCanvasDimensions();
            }

            ctx.fillStyle = 'rgba(0, 0, 0, 0.12)';
            ctx.fillRect(0, 0, curW, curH);

            ctx.font = '12px "JetBrains Mono", monospace';

            for (let i = 0; i < drops.length; i++) {
                const text = chars.charAt(Math.floor(Math.random() * chars.length));
                const x = i * fontSize;
                const y = drops[i] * fontSize;

                if (Math.random() > 0.88) {
                    ctx.fillStyle = '#FFFFFF';
                } else {
                    ctx.fillStyle = '#00FF41';
                }

                if (y > 0) {
                    ctx.fillText(text, x, y);
                }

                if (y > curH && Math.random() > 0.975) {
                    drops[i] = 0;
                }
                drops[i]++;
            }
        }

        requestAnimationFrame(renderMatrix);
    }"""

start_m = html.find("// ═══ MATRIX DATA STREAM CANVAS")
end_m = html.find("// ═══ GARANTÍA DE MOVIMIENTO Y HOVER EN VÍDEOS DEL SHOWCASE ═══")

if start_m != -1 and end_m != -1:
    html = html[:start_m] + new_matrix_js.strip() + "\n\n    " + html[end_m:]
    print("✅ Updated Matrix Rain Canvas engine with ResizeObserver & RequestAnimationFrame")

# Ensure Scroll reveal activates all elements on mobile
reveal_fix_js = """    // Scroll reveal observer
    const reveals = document.querySelectorAll('.reveal');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) entry.target.classList.add('active');
        });
    }, { threshold: 0.01, rootMargin: '0px 0px 100px 0px' });
    reveals.forEach(r => observer.observe(r));

    // Force active class on mobile load
    if (window.innerWidth <= 1024) {
        reveals.forEach(r => r.classList.add('active'));
    }"""

if "// Scroll reveal observer" in html:
    start_r = html.find("// Scroll reveal observer")
    end_r = html.find("// Form submit simulation")
    if start_r != -1 and end_r != -1:
        html = html[:start_r] + reveal_fix_js.strip() + "\n\n    " + html[end_r:]
        print("✅ Updated Scroll Reveal for iPhone mobile compatibility")

with open(index_path, "w", encoding="utf-8") as f:
    f.write(html)

print("✅ index.html updated successfully!")
