import re
import os

print("=== Fixing All Web App Mechanics & Bugs ===")

# --- 1. FIX INDEX.HTML ---
index_path = "/Users/jesusferrer/.gemini/antigravity-ide/scratch/web-chus/index.html"
with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

# Fix video tags boolean attributes in showcase grid
html = html.replace('autoplay="" loop="" muted="" playsinline=""', 'autoplay loop muted playsinline')
html = html.replace('autoplay="" loop="" muted=""', 'autoplay loop muted playsinline')

# Update video modal HTML for X button and backdrop
new_modal_snippet = """<div class="modal-backdrop" id="video-modal">
<div class="glass-panel p-4 sm:p-6 max-w-4xl w-full max-h-[92vh] overflow-y-auto border border-signal-red/50 relative space-y-4 shadow-2xl" onclick="event.stopPropagation()">
<!-- Botón de Cerrar Modal -->
<button type="button" class="absolute top-3 right-3 text-white hover:text-signal-red font-mono text-2xl z-50 w-12 h-12 bg-black/90 rounded-full flex items-center justify-center border border-white/40 transition-all cursor-pointer shadow-2xl" id="close-modal" aria-label="Cerrar modal">×</button>"""

if 'id="close-modal"' in html:
    html = re.sub(
        r'<div class="modal-backdrop" id="video-modal"[^>]*>[\s\S]*?<button [^>]*id="close-modal"[^>]*>×</button>',
        new_modal_snippet,
        html,
        count=1
    )

new_js_block = """    // ═══ MATRIX DATA STREAM CANVAS (60FPS CONTINUO Y ESTABLE) ═══
    const mCanvas = document.getElementById('matrix-canvas');
    if (mCanvas) {
        const ctx = mCanvas.getContext('2d');
        const chars = 'CHUSBZN0123456789EBUR128AI@#$890';
        const fontSize = 12;
        let columns = 0;
        let drops = [];
        let curW = 0, curH = 0;

        function initMatrixSize() {
            const parent = mCanvas.parentElement;
            const w = (parent && parent.clientWidth) ? parent.clientWidth : 360;
            const h = (parent && parent.clientHeight) ? parent.clientHeight : 256;
            
            if (curW !== w || curH !== h) {
                curW = w;
                curH = h;
                mCanvas.width = w;
                mCanvas.height = h;
                columns = Math.max(10, Math.floor(w / fontSize));
                drops = Array(columns).fill(0).map(() => Math.floor(Math.random() * -20));
            }
        }

        initMatrixSize();
        window.addEventListener('resize', initMatrixSize);

        function drawMatrix() {
            if (!curW || !curH) initMatrixSize();
            
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

        setInterval(drawMatrix, 35);
    }

    // ═══ GARANTÍA DE MOVIMIENTO Y HOVER EN VÍDEOS DEL SHOWCASE ═══
    const initShowcaseVideos = () => {
        const videos = document.querySelectorAll('#showcase-grid video');
        videos.forEach(v => {
            v.muted = true;
            v.setAttribute('playsinline', '');
            v.setAttribute('muted', '');
            v.setAttribute('loop', '');
            v.setAttribute('autoplay', '');
            const p = v.play();
            if (p !== undefined) {
                p.catch(() => {});
            }
        });
    };
    initShowcaseVideos();
    window.addEventListener('DOMContentLoaded', initShowcaseVideos);

    document.querySelectorAll('.video-card').forEach(card => {
        const v = card.querySelector('video');
        if (!v) return;
        const ensurePlay = () => {
            v.muted = true;
            v.play().catch(() => {});
        };
        card.addEventListener('mouseenter', ensurePlay);
        card.addEventListener('pointerenter', ensurePlay);
        card.addEventListener('touchstart', ensurePlay, { passive: true });
    });

    // Toggle Desplegable OTROS
    function toggleOtherServiceInput() {
        const select = document.getElementById('service-select');
        const wrap = document.getElementById('other-service-wrap');
        const input = document.getElementById('other-service-input');
        if (select && wrap && input) {
            if (select.value === 'otros') {
                wrap.classList.remove('hidden');
                input.setAttribute('required', 'true');
            } else {
                wrap.classList.add('hidden');
                input.removeAttribute('required');
            }
        }
    }

    // Modal Explicativo de Servicios
    const serviceData = {
        video: {
            code: "// DOSSIER 01 - VÍDEO & SPOTS CINEMÁTICOS",
            title: "Producción de Vídeo & Spots Cinemáticos",
            desc: "CHUS BZN diseña y ejecuta producciones publicitarias de alto nivel, spots para televisión y marcas corporativas, filmación multicámara en plató y dirección técnica cinematográfica asistida por Inteligencia Artificial.",
            specs: "<strong>Solución Comercial & Entregables:</strong><br/>• Masterización en resolución 4K/8K con espacio de color ACES y LUTs (.cube) propietarias de alta fidelidad.<br/>• Reducción de hasta un 60% en tiempos de previz y generación de planos complejos mediante ComfyUI & Wan 2.1.<br/>• <strong>Aplicación para el cliente:</strong> Campañas publicitarias masivas, videoclips y largometrajes con estándares de emisión cinematográfica internacional."
        },
        sonido: {
            code: "// DOSSIER 02 - POSTPRODUCCIÓN & SONIDO EBU R128",
            title: "Postproducción de Sonido & Masterización EBU R128",
            desc: "Ingeniería de mezcla sonoras, sonoridad homologada para televisión pública/privada (TV3, TVE1) y plataformas OTT de streaming internacional (Netflix, HBO, Amazon Prime).",
            specs: "<strong>Solución Comercial & Entregables:</strong><br/>• Control de volumen (-23 LUFS) riguroso bajo la norma internacional EBU R128, evitando rechazos de emisión.<br/>• Limpieza y restauración espectral forense con iZotope RX11 y SpectraLayers Pro.<br/>• <strong>Aplicación para el cliente:</strong> Películas, series de doblaje, publicidad y podcasts premium."
        },
        streaming: {
            code: "// DOSSIER 03 - DIRECTOS, STREAMING & COBERTURA 360°",
            title: "Directos, Streaming & Cobertura Broadcast 360°",
            desc: "Arquitectura técnica de señal audiovisual en tiempo real para convenciones multinacionales, eventos deportivos, espectáculos y emisiones simultáneas en redes sociales.",
            specs: "<strong>Solución Comercial & Entregables:</strong><br/>• Automatización de regiduría multimedia mediante OBS Studio, QLab y mezcladores físicos de video.<br/>• Control CCU de exposición y ajuste de color en tiempo real.<br/>• <strong>Aplicación para el cliente:</strong> Cobertura 360° sin latencia, streaming corporativo de alta disponibilidad y garantía de emisión ininterrumpida."
        },
        dj: {
            code: "// DOSSIER 04 - DJ SESSIONS, LIVE PERFORMANCE & REMEZCLAS",
            title: "DJ Live Performance & Producción Musical",
            desc: "Dirección y ejecución de sesiones de música avanzada para festivales, macroeventos corporativos e identidad sonora de recintos comerciales.",
            specs: "<strong>Solución Comercial & Entregables:</strong><br/>• Operación con hardware profesional Pioneer de alta gama (DDJ1000 / Rekordbox).<br/>• Estudio acústico de sala y remezclas exclusivas de estudio adaptadas al perfil del evento.<br/>• <strong>Aplicación para el cliente:</strong> Eventos de gran formato, convenciones de marca y producción discográfica."
        },
        web: {
            code: "// DOSSIER 05 - DESARROLLO WEB & WEB APPS A MEDIDA",
            title: "Desarrollo Web & Aplicaciones Interactivas",
            desc: "Programación de aplicaciones web interactivas a medida, plataformas SaaS de alto rendimiento, landing pages comerciales e integración de pasarelas API de Inteligencia Artificial.",
            specs: "<strong>Solución Comercial & Entregables:</strong><br/>• Código limpio en HTML5/JS/FastAPI/Electron optimizado para máxima velocidad de carga (FCP < 0.8s).<br/>• Diseño responsivo adaptado a todos los dispositivos móviles y escritorios.<br/>• <strong>Aplicación para el cliente:</strong> Punto de venta digital, automatización de procesos empresariales y presencia web corporativa de impacto."
        },
        design: {
            code: "// DOSSIER 06 - MOTION GRAPHICS & DISEÑO GRÁFICO",
            title: "Motion Graphics & Identidad Visual",
            desc: "Creación de elementos visuales animados 2D/3D, bumpers para canales de televisión, paquetes de continuidad gráfica para emisiones en vivo y diseño de marca.",
            specs: "<strong>Solución Comercial & Entregables:</strong><br/>• Animaciones avanzadas en After Effects y Blender.<br/>• Composición fotográfica y gráfica de alta resolución.<br/>• <strong>Aplicación para el cliente:</strong> Imagen corporativa de alto impacto, promociones y gráficos para eventos."
        },
        ia: {
            code: "// DOSSIER 07 - IMPLANTACIÓN DE IA EMPRESARIAL",
            title: "Implantación & Automatización de IA en Empresas",
            desc: "Integración estratégica de Inteligencia Artificial Generativa, agentes autónomos para empresas y clonación biométrica vocal legal bajo normativa europea.",
            specs: "<strong>Solución Comercial & Entregables:</strong><br/>• Blindaje y cumplimiento del protocolo europeo EU AI Act y derechos de voz.<br/>• Conexión de modelos multimodales (Claude, ChatGPT, Qwen, DeepSeek) en la infraestructura de la empresa.<br/>• <strong>Aplicación para el cliente:</strong> Reducción masiva de costes operativos, atención automatizada y generación de contenidos en segundos."
        },
        formacion: {
            code: "// DOSSIER 08 - FORMACIÓN & CONSULTORÍA TECNOLÓGICA",
            title: "Formación & Consultoría Tecnológica",
            desc: "Capacitación a medida para equipos de producción, productoras de televisión y empresas en herramientas emergentes de IA y workflows audiovisuales.",
            specs: "<strong>Solución Comercial & Entregables:</strong><br/>• Programas intensivos de Vibe Coding, Prompting para vídeo y herramientas de IA.<br/>• Auditoría tecnológica presencial o remota para optimizar flujos de trabajo.<br/>• <strong>Aplicación para el cliente:</strong> Transformación digital rápida de equipos humanos e incremento directo de la productividad."
        }
    };

    function openServiceModal(key) {
        const currentLang = localStorage.getItem('site_lang') || 'es';
        const t = (typeof translations !== 'undefined' && translations[currentLang]) || (typeof translations !== 'undefined' && translations['es']) || {};
        
        const code = t[`t_service_${key}_code`] || (serviceData[key] && serviceData[key].code) || '';
        const title = t[`t_service_${key}_title`] || (serviceData[key] && serviceData[key].title) || '';
        const desc = t[`t_service_${key}_desc`] || (serviceData[key] && serviceData[key].desc) || '';
        const specs = t[`t_service_${key}_specs`] || (serviceData[key] && serviceData[key].specs) || '';

        document.getElementById('modal-code').textContent = code;
        document.getElementById('modal-title').textContent = title;
        document.getElementById('modal-desc').textContent = desc;
        document.getElementById('modal-specs').innerHTML = specs;
        document.getElementById('service-modal').classList.add('open');
    }

    function closeServiceModal(e) {
        document.getElementById('service-modal').classList.remove('open');
    }

    // ═══ LIGHTBOX REPRODUCTOR VÍDEO CON AUDIO ═══
    const showcaseGrid = document.getElementById('showcase-grid');
    const videoModal = document.getElementById('video-modal');
    const modalContent = document.getElementById('modal-content');
    const vmodalTitle = document.getElementById('vmodal-title');
    const vmodalBadge = document.getElementById('vmodal-badge');
    const vmodalDesc = document.getElementById('vmodal-desc');
    const vmodalLink = document.getElementById('vmodal-link');

    const openVideoModal = (platform, id, ratio, localVideo, title, badge, desc, link) => {
        console.log(`[Analytics] Reproducido: ${platform}-${id} ("${title || 'Producción'}")`);

        if (vmodalTitle) vmodalTitle.textContent = title || '---';
        if (vmodalBadge) vmodalBadge.textContent = badge || '// REPRODUCTOR VIVO CON AUDIO';
        if (vmodalDesc) vmodalDesc.textContent = desc || '---';
        if (vmodalLink) vmodalLink.href = link || '#';

        if (modalContent) {
            if (ratio === '9/16' || platform === 'instagram') {
                modalContent.style.width = 'auto';
                modalContent.style.maxWidth = '100%';
                modalContent.style.aspectRatio = '9/16';
                modalContent.style.maxHeight = '62vh';
                modalContent.style.margin = '0 auto';
            } else {
                modalContent.style.width = '100%';
                modalContent.style.maxWidth = 'none';
                modalContent.style.aspectRatio = '16/9';
                modalContent.style.maxHeight = 'none';
                modalContent.style.margin = '0';
            }
        }

        let embedHTML = '';
        if (localVideo) {
            embedHTML = `<video src="${localVideo}" controls autoplay playsinline class="w-full h-full object-contain rounded shadow-2xl" type="video/mp4"></video>`;
        } else if (platform === 'youtube' && id) {
            embedHTML = `<iframe class="w-full h-full rounded border-0" style="aspect-ratio: ${ratio || '16/9'};" src="https://www.youtube.com/embed/${id}?autoplay=1&rel=0&modestbranding=1" allow="autoplay; encrypted-media; fullscreen" allowfullscreen></iframe>`;
        } else if (platform === 'instagram' && id) {
            embedHTML = `<iframe class="w-full h-full rounded border-0" style="aspect-ratio: ${ratio || '9/16'};" src="https://www.instagram.com/p/${id}/embed" allowfullscreen></iframe>`;
        }

        if (modalContent) modalContent.innerHTML = embedHTML;
        if (videoModal) videoModal.classList.add('open');
        document.body.style.overflow = 'hidden';
    };

    const closeVideoModal = (e) => {
        if (e && e.preventDefault) e.preventDefault();
        if (e && e.stopPropagation) e.stopPropagation();
        if (videoModal) videoModal.classList.remove('open');
        document.body.style.overflow = '';
        if (modalContent) {
            modalContent.innerHTML = '';
            modalContent.style.width = '';
            modalContent.style.maxWidth = '';
            modalContent.style.aspectRatio = '';
            modalContent.style.maxHeight = '';
            modalContent.style.margin = '';
        }
    };

    // Listeners instantáneos de cierre para Touch / Click
    const closeBtn = document.getElementById('close-modal');
    if (closeBtn) {
        const handleClose = (e) => {
            if (e) {
                e.preventDefault();
                e.stopPropagation();
            }
            closeVideoModal(e);
        };
        closeBtn.addEventListener('click', handleClose);
        closeBtn.addEventListener('touchstart', handleClose, { passive: false });
    }

    if (videoModal) {
        videoModal.addEventListener('click', (e) => {
            if (e.target === videoModal) closeVideoModal(e);
        });
    }

    if (showcaseGrid) {
        showcaseGrid.addEventListener('click', (e) => {
            const card = e.target.closest('.video-card');
            if (!card) return;

            const platform = card.dataset.platform;
            const id = card.dataset.id;
            const ratio = card.dataset.ratio;
            const local = card.dataset.local;
            const link = card.dataset.link;

            const currentLang = localStorage.getItem('site_lang') || 'es';
            const t = (typeof translations !== 'undefined' && translations[currentLang]) || {};

            const title = t[card.dataset.titleKey] || card.dataset.title || '';
            const badge = t[card.dataset.badgeKey] || card.dataset.badge || '';
            const desc = t[card.dataset.descKey] || card.dataset.desc || '';

            openVideoModal(platform, id, ratio, local, title, badge, desc, link);
        });
    }

    // Teclas ESC / Space para control de cierre
    document.addEventListener('keydown', (e) => {
        if (!videoModal || !videoModal.classList.contains('open')) return;
        if (e.key === 'Escape') {
            closeVideoModal(e);
        }
    });

    // Mobile Navigation Toggle & Smooth Scroll
    const mobileBtn = document.getElementById('mobile-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const mobileLinks = document.querySelectorAll('.mobile-link');
    if (mobileBtn && mobileMenu) {
        mobileBtn.addEventListener('click', () => mobileMenu.classList.toggle('open'));
    }
    mobileLinks.forEach(link => link.addEventListener('click', () => {
        if (mobileMenu) mobileMenu.classList.remove('open');
    }));

    // Navegación suave responsiva para enlaces de ancla
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (!targetId || targetId === '#') return;
            if (targetId === '#top') {
                e.preventDefault();
                window.scrollTo({ top: 0, behavior: 'smooth' });
                if (mobileMenu) mobileMenu.classList.remove('open');
                return;
            }
            const targetEl = document.querySelector(targetId);
            if (targetEl) {
                e.preventDefault();
                targetEl.scrollIntoView({ behavior: 'smooth' });
                if (mobileMenu) mobileMenu.classList.remove('open');
            }
        });
    });

    // Scroll reveal observer
    const reveals = document.querySelectorAll('.reveal');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) entry.target.classList.add('active');
        });
    }, { threshold: 0.1 });
    reveals.forEach(r => observer.observe(r));

    // Form submit simulation
    const form = document.getElementById('order-form');
    const successMsg = document.getElementById('form-success');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            if (successMsg) successMsg.classList.remove('hidden');
            form.reset();
            toggleOtherServiceInput();
            setTimeout(() => { if (successMsg) successMsg.classList.add('hidden'); }, 6000);
        });
    }

    // Terminal rotator
    const termMsg = document.getElementById('terminal-msg');
    const termLogs = [
        "[ SYS_LOG: VÍNCULO_BROADCAST_ESTABLECIDO ]",
        "[ SYS_LOG: AUDIO_EBU_R128_SAMPLED_48KHZ ]",
        "[ SYS_LOG: PIPELINE_IA_ACTIVO_60FPS ]",
        "[ SYS_LOG: NODO_BARCELONA_ONLINE ]"
    ];
    let termIdx = 0;
    if (termMsg) {
        setInterval(() => {
            termIdx = (termIdx + 1) % termLogs.length;
            termMsg.textContent = termLogs[termIdx];
        }, 4000);
    }
"""

start_pos = html.find("// Matrix Rain Stream Canvas (Animación Continua Garantizada)")
end_pos = html.find("// Mouse reactive background orbs with inertial Lerp")

if start_pos != -1 and end_pos != -1:
    html = html[:start_pos] + new_js_block.strip() + "\n\n    " + html[end_pos:]
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ index.html updated via substring replacement!")
else:
    print(f"Warning: position markers not found: start={start_pos}, end={end_pos}")

# --- 2. FIX POST.HTML ---
post_path = "/Users/jesusferrer/.gemini/antigravity-ide/scratch/web-chus/post.html"
with open(post_path, "r", encoding="utf-8") as f:
    post_html = f.read()

# Update loadPostData to fallback to 'mock-1' if no postId provided
old_load_check = """        if (!postId) {
            pageState.status = 'no-id';
            renderState();
            return;
        }"""

new_load_check = """        const targetPostId = postId || 'mock-1';
        
        if (targetPostId.startsWith('mock-')) {
            const post = mockPosts[targetPostId] || mockPosts['mock-1'];
            if (post) {
                pageState.status = 'loaded';
                pageState.post = post;
            } else {
                pageState.status = 'not-found';
            }
            renderState();
            initCommentsSystem(targetPostId);
            return;
        }"""

if "if (!postId) {" in post_html:
    post_html = post_html.replace(old_load_check, new_load_check)

comments_system_js = """
    // Sistema dinámico de comentarios interactivos con persistencia localStorage
    function initCommentsSystem(postId) {
        setTimeout(() => {
            const form = document.getElementById('comment-form');
            if (!form) return;
            
            const storageKey = `post_comments_${postId}`;
            const existingComments = JSON.parse(localStorage.getItem(storageKey) || '[]');
            
            const countEl = document.getElementById('comments-count');
            const userBlock = document.getElementById('user-comments-block');
            
            function renderComments() {
                const baseCount = 3 + existingComments.length;
                if (countEl) countEl.textContent = `[ ${baseCount} COMENTARIOS AUDITADOS ]`;
                
                if (userBlock) {
                    userBlock.innerHTML = existingComments.map(c => `
                        <div class="glass-panel p-5 border border-terminal-green/30 rounded space-y-2 animate-fadeIn">
                            <div class="flex justify-between items-center text-text-secondary font-mono text-[10px]">
                                <span class="text-terminal-green font-bold">${escapeHtml(c.name)} (${escapeHtml(c.email || 'Verificado')})</span>
                                <span>${c.date}</span>
                            </div>
                            <p class="text-white/90 leading-relaxed font-light">«${escapeHtml(c.text)}»</p>
                        </div>
                    `).join('');
                }
            }

            renderComments();

            form.addEventListener('submit', (e) => {
                e.preventDefault();
                const nameInput = document.getElementById('c-name');
                const emailInput = document.getElementById('c-email');
                const textInput = document.getElementById('c-text');
                const alertSuccess = document.getElementById('comment-success');

                if (!nameInput.value.trim() || !textInput.value.trim()) return;

                const newComment = {
                    name: nameInput.value.trim(),
                    email: emailInput.value.trim(),
                    text: textInput.value.trim(),
                    date: new Date().toISOString().replace('T', ' ').substring(0, 16)
                };

                existingComments.unshift(newComment);
                localStorage.setItem(storageKey, JSON.stringify(existingComments));

                nameInput.value = '';
                emailInput.value = '';
                textInput.value = '';

                if (alertSuccess) {
                    alertSuccess.classList.remove('hidden');
                    setTimeout(() => alertSuccess.classList.add('hidden'), 5000);
                }

                renderComments();
            });
        }, 100);
    }

    function escapeHtml(str) {
        return (str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }
"""

new_comments_markup = """<!-- ═══ SECCIÓN DE COMENTARIOS & DEBATE PROFESIONAL ═══ -->
                <div class="mt-16 pt-10 border-t border-white/15 space-y-8">
                    <div class="flex items-center justify-between">
                        <h3 class="font-headline text-2xl text-white uppercase tracking-tight">// COMENTARIOS &amp; DEBATE TÉCNICO</h3>
                        <span class="font-mono text-xs text-signal-red font-bold" id="comments-count">[ 3 COMENTARIOS AUDITADOS ]</span>
                    </div>
                    <div class="space-y-4 font-sans text-xs" id="comments-list">
                        <div class="glass-panel p-5 border border-white/10 rounded space-y-2">
                            <div class="flex justify-between items-center text-text-secondary font-mono text-[10px]">
                                <span class="text-white font-bold">Ing. Marc Soler (Broadcast Tech)</span>
                                <span>2026-06-16 • 14:20</span>
                            </div>
                            <p class="text-white/90 leading-relaxed font-light">«Impresionante la integración de la previsualización asistida por IA. Nos ahorró más de 4 horas de set en el ajuste de iluminación anamórfica.»</p>
                        </div>
                        <div class="glass-panel p-5 border border-white/10 rounded space-y-2">
                            <div class="flex justify-between items-center text-text-secondary font-mono text-[10px]">
                                <span class="text-white font-bold">Elena Rivas (Directora de Fotografía)</span>
                                <span>2026-06-16 • 18:45</span>
                            </div>
                            <p class="text-white/90 leading-relaxed font-light">«La precisión del estándar EBU R128 en el diseño sonoro complementa perfectamente el tratamiento cromático. Excelente trabajo.»</p>
                        </div>
                        <div class="glass-panel p-5 border border-white/10 rounded space-y-2">
                            <div class="flex justify-between items-center text-text-secondary font-mono text-[10px]">
                                <span class="text-white font-bold">David V. (Postproducción Audio)</span>
                                <span>2026-06-17 • 09:15</span>
                            </div>
                            <p class="text-white/90 leading-relaxed font-light">«El flujo híbrido de prompting con LoRA de referencia ahorra tiempo valiosísimo en preproducción. Totalmente recomendado.»</p>
                        </div>
                        <div id="user-comments-block" class="space-y-4"></div>
                    </div>
                    <!-- Formulario de comentario nuevo -->
                    <form id="comment-form" class="glass-panel p-6 border border-white/15 rounded space-y-4">
                        <div class="flex justify-between items-center">
                            <span class="font-mono text-xs text-signal-red uppercase font-bold">// AÑADIR COMENTARIO TÉCNICO</span>
                            <span id="comment-success" class="hidden text-terminal-green font-mono text-xs font-bold animate-pulse">✓ Comentario registrado en el protocolo de auditoría.</span>
                        </div>
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <input type="text" id="c-name" required placeholder="Nombre completo / Firma" class="bg-black/80 border border-white/20 p-3 text-xs font-mono text-white rounded outline-none focus:border-signal-red">
                            <input type="email" id="c-email" placeholder="Email corporativo (opcional)" class="bg-black/80 border border-white/20 p-3 text-xs font-mono text-white rounded outline-none focus:border-signal-red">
                        </div>
                        <textarea id="c-text" rows="3" required placeholder="Escribe tu observación o comentario técnico..." class="w-full bg-black/80 border border-white/20 p-3 text-xs font-mono text-white rounded outline-none focus:border-signal-red"></textarea>
                        <button type="submit" class="bg-signal-red hover:bg-white text-white hover:text-signal-red font-mono text-xs px-6 py-2.5 uppercase font-bold tracking-wider transition-all rounded shadow-lg cursor-pointer">ENVIAR COMENTARIO →</button>
                    </form>
                </div>
            `;"""

c_start = post_html.find("<!-- ═══ SECCIÓN DE COMENTARIOS & DEBATE PROFESIONAL ═══ -->")
c_end = post_html.find("<!-- Formulario de comentario nuevo -->")

if c_start != -1:
    post_html = re.sub(
        r'<!-- ═══ SECCIÓN DE COMENTARIOS & DEBATE PROFESIONAL ═══ -->[\s\S]*?</button>\s*</div>\s*</div>\s*`;',
        new_comments_markup,
        post_html,
        count=1
    )

if "window.addEventListener('DOMContentLoaded', loadPostData);" in post_html and "function initCommentsSystem" not in post_html:
    post_html = post_html.replace(
        "window.addEventListener('DOMContentLoaded', loadPostData);",
        comments_system_js + "\n    window.addEventListener('DOMContentLoaded', loadPostData);"
    )

with open(post_path, "w", encoding="utf-8") as f:
    f.write(post_html)

print("✅ post.html comments system updated successfully!")
