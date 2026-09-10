import re
import os

print("=== APPLYING MASTER ENGINEERING OPTIMIZATIONS & MOBILE FIXES ===")

# --- 1. UPDATE INDEX.HTML ---
index_path = "/Users/jesusferrer/.gemini/antigravity-ide/scratch/web-chus/index.html"
with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

# Fix YouTube Shorts card title
html = html.replace('YouTube Shorts (48 Clips IA)', 'YouTube Shorts IA')

# CSS Updates: Add SVG Grain, Retro Red Ambient Orbs, and Mobile Menu styling
css_master = """
    /* SVG Retro Noise / Film Grain Texture Overlay */
    .bg-grain {
        position: fixed;
        inset: 0;
        width: 100%;
        height: 100%;
        opacity: 0.035;
        pointer-events: none;
        z-index: 1;
        background: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
    }

    /* Red Retro Organic Ambient Orbs (GPU Accelerated with Lerp) */
    .organic-orb-1 {
        position: fixed;
        top: -10%; left: -10%;
        width: 50vw; height: 50vw;
        max-width: 650px; max-height: 650px;
        background: radial-gradient(circle, rgba(255, 31, 31, 0.22) 0%, rgba(255, 0, 0, 0.05) 50%, transparent 75%);
        pointer-events: none;
        z-index: 0;
        filter: blur(60px);
        will-change: transform;
        transform: translate3d(0, 0, 0);
    }
    .organic-orb-2 {
        position: fixed;
        bottom: -10%; right: -10%;
        width: 45vw; height: 45vw;
        max-width: 550px; max-height: 550px;
        background: radial-gradient(circle, rgba(255, 31, 31, 0.16) 0%, rgba(255, 255, 255, 0.04) 45%, transparent 70%);
        pointer-events: none;
        z-index: 0;
        filter: blur(55px);
        will-change: transform;
        transform: translate3d(0, 0, 0);
    }

    /* Mobile Nav Overlay */
    #mobile-menu {
        display: none;
        position: fixed;
        inset: 0;
        background: rgba(0,0,0,0.98);
        z-index: 9999;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 24px;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
    }
    #mobile-menu.open { display: flex !important; }

    /* Mobile Reveal Fallback & Clean Transitions */
    @media (max-width: 1024px) {
        .reveal {
            opacity: 1 !important;
            transform: none !important;
            transition: none !important;
        }
    }
"""

# Replace CSS section or insert before </style>
if "/* SVG Retro Noise / Film Grain" not in html:
    html = html.replace("</style>", css_master + "\n</style>")

# Ensure SVG Grain div is inside <body> right after <body> tag
if '<div class="bg-grain"></div>' not in html:
    html = html.replace('<body class="bg-black text-white selection:bg-signal-red selection:text-white blueprint-grid" id="top">', '<body class="bg-black text-white selection:bg-signal-red selection:text-white blueprint-grid" id="top">\n<div class="bg-grain"></div>')

# Update #mobile-menu HTML to include dedicated close button X
mobile_menu_html = """<!-- Mobile Navigation Overlay -->
<div id="mobile-menu">
<button id="close-mobile-menu" aria-label="Cerrar menú" class="absolute top-6 right-6 text-white text-3xl font-mono p-3 hover:text-signal-red focus:outline-none cursor-pointer z-50">✕</button>
<a class="mobile-link text-xl font-headline uppercase tracking-widest text-white hover:text-signal-red" data-i18n="t_nav_services" href="#servicios">01. Servicios</a>
<a class="mobile-link text-xl font-headline uppercase tracking-widest text-white hover:text-signal-red" data-i18n="t_129" href="#redes">02. Dónde Ver Trabajos</a>
<a class="mobile-link text-xl font-headline uppercase tracking-widest text-white hover:text-signal-red" data-i18n="t_nav_ai" href="#ecosistema">03. Ecosistema IA</a>
<a class="mobile-link text-xl font-headline uppercase tracking-widest text-white hover:text-signal-red" data-i18n="t_130" href="#showcase">04. Vídeos en Vivo</a>
<a class="mobile-link text-xl font-headline uppercase tracking-widest text-white hover:text-signal-red" data-i18n="t_131" href="#metodologia">05. Perfil &amp; Trayectoria</a>
<a class="mobile-link text-xl font-headline uppercase tracking-widest text-white hover:text-signal-red" data-i18n="t_132" href="blog.html">06. Blog</a>
<a class="mobile-link text-xl font-headline uppercase tracking-widest text-signal-red" data-i18n="t_142" href="#presupuesto">07. Encargo 24h</a>
</div>"""

if '<button id="close-mobile-menu"' not in html:
    html = re.sub(
        r'<!-- Mobile Navigation Overlay -->\s*<div id="mobile-menu">[\s\S]*?</div>',
        mobile_menu_html,
        html,
        count=1
    )

# Now update JavaScript section for Matrix Rain, Mobile Menu, Orbs, and Video Modal
new_master_js = """
    // ═══ MATRIX DATA STREAM CANVAS (60FPS CONTINUO Y ESTABLE EN IPHONE & DESKTOP) ═══
    const mCanvas = document.getElementById('matrix-canvas');
    if (mCanvas) {
        const ctx = mCanvas.getContext('2d');
        const chars = 'CHUSBZN0123456789EBUR128AI@#$890';
        const fontSize = 12;
        let columns = 0;
        let drops = [];

        function updateCanvasDimensions() {
            const parent = mCanvas.parentElement;
            const w = (parent && parent.clientWidth > 0) ? parent.clientWidth : (window.innerWidth < 480 ? 320 : 360);
            const h = (parent && parent.clientHeight > 0) ? parent.clientHeight : 250;
            
            if (mCanvas.width !== w || mCanvas.height !== h) {
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
        const fpsInterval = 35; // ~30 FPS constante

        function renderMatrix(timestamp) {
            requestAnimationFrame(renderMatrix);

            if (timestamp - lastDrawTime < fpsInterval) return;
            lastDrawTime = timestamp;

            const parent = mCanvas.parentElement;
            if (parent && (mCanvas.width !== parent.clientWidth || mCanvas.height !== parent.clientHeight)) {
                updateCanvasDimensions();
            }

            ctx.fillStyle = 'rgba(0, 0, 0, 0.12)';
            ctx.fillRect(0, 0, mCanvas.width, mCanvas.height);

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

                if (y > mCanvas.height && Math.random() > 0.975) {
                    drops[i] = 0;
                }
                drops[i]++;
            }
        }

        requestAnimationFrame(renderMatrix);
    }

    // ═══ RECTIFICACIÓN LERP & MOVIMIENTO AMBIENTAL ROJO DE FONDO ═══
    const orb1 = document.querySelector('.organic-orb-1');
    const orb2 = document.querySelector('.organic-orb-2');
    let targetX = window.innerWidth / 2, targetY = window.innerHeight / 2;
    let currentX1 = 0, currentY1 = 0, currentX2 = 0, currentY2 = 0;

    window.addEventListener('pointermove', (e) => {
        targetX = e.clientX;
        targetY = e.clientY;
    }, { passive: true });

    window.addEventListener('touchmove', (e) => {
        if (e.touches && e.touches[0]) {
            targetX = e.touches[0].clientX;
            targetY = e.touches[0].clientY;
        }
    }, { passive: true });

    window.addEventListener('scroll', () => {
        targetY = (window.scrollY * 0.12) % window.innerHeight;
    }, { passive: true });

    function updateOrbs() {
        requestAnimationFrame(updateOrbs);
        currentX1 += (targetX * 0.06 - currentX1) * 0.04;
        currentY1 += (targetY * 0.06 - currentY1) * 0.04;
        currentX2 += (-targetX * 0.05 - currentX2) * 0.03;
        currentY2 += (-targetY * 0.05 - currentY2) * 0.03;

        if (orb1) orb1.style.transform = `translate3d(${currentX1}px, ${currentY1}px, 0)`;
        if (orb2) orb2.style.transform = `translate3d(${currentX2}px, ${currentY2}px, 0)`;
    }
    requestAnimationFrame(updateOrbs);

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
    window.addEventListener('load', initShowcaseVideos);

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
        card.addEventListener('pointerdown', ensurePlay, { passive: true });
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

    // ═══ LIGHTBOX REPRODUCTOR VÍDEO CON AUDIO COMPLETO ═══
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

        setTimeout(() => {
            const vel = modalContent.querySelector('video');
            if (vel) vel.play().catch(() => {});
        }, 50);
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

    // ═══ NAVEGACIÓN MÓVIL HAMBURGUESA & LISTENERS DE TOQUE ═══
    const mobileBtn = document.getElementById('mobile-btn');
    const closeMobileBtn = document.getElementById('close-mobile-menu');
    const mobileMenu = document.getElementById('mobile-menu');
    const mobileLinks = document.querySelectorAll('.mobile-link');

    const toggleMobileMenu = (e) => {
        if (e) {
            e.preventDefault();
            e.stopPropagation();
        }
        if (mobileMenu) mobileMenu.classList.toggle('open');
    };

    const closeMobileDrawer = (e) => {
        if (e) {
            e.preventDefault();
            e.stopPropagation();
        }
        if (mobileMenu) mobileMenu.classList.remove('open');
    };

    if (mobileBtn) {
        mobileBtn.addEventListener('click', toggleMobileMenu);
        mobileBtn.addEventListener('touchstart', toggleMobileMenu, { passive: false });
    }
    if (closeMobileBtn) {
        closeMobileBtn.addEventListener('click', closeMobileDrawer);
        closeMobileBtn.addEventListener('touchstart', closeMobileDrawer, { passive: false });
    }
    mobileLinks.forEach(link => {
        link.addEventListener('click', closeMobileDrawer);
        link.addEventListener('touchstart', closeMobileDrawer, { passive: true });
    });

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
    }, { threshold: 0.01, rootMargin: '0px 0px 100px 0px' });
    reveals.forEach(r => observer.observe(r));

    if (window.innerWidth <= 1024) {
        reveals.forEach(r => r.classList.add('active'));
    }

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

start_pos = html.find("// ═══ MATRIX DATA STREAM CANVAS")
if start_pos != -1:
    end_pos = html.find("// Mouse reactive background orbs with inertial Lerp")
    if end_pos == -1:
        end_pos = html.find("<!-- i18n Scripts -->")
    if end_pos != -1:
        html = html[:start_pos] + new_master_js.strip() + "\n</script>\n<!-- i18n Scripts -->" + html[end_pos:]

with open(index_path, "w", encoding="utf-8") as f:
    f.write(html)

print("✅ index.html master optimizations applied successfully!")

# --- 2. UPDATE BLOG.HTML ---
blog_path = "/Users/jesusferrer/.gemini/antigravity-ide/scratch/web-chus/blog.html"
with open(blog_path, "r", encoding="utf-8") as f:
    b_html = f.read()

# Add bg-grain texture in blog.html
if '<div class="bg-grain"></div>' not in b_html:
    b_html = b_html.replace('<body>', '<body>\n<div class="bg-grain"></div>')

with open(blog_path, "w", encoding="utf-8") as f:
    f.write(b_html)

print("✅ blog.html master optimizations applied successfully!")

# --- 3. UPDATE POST.HTML ---
post_path = "/Users/jesusferrer/.gemini/antigravity-ide/scratch/web-chus/post.html"
with open(post_path, "r", encoding="utf-8") as f:
    p_html = f.read()

if '<div class="bg-grain"></div>' not in p_html:
    p_html = p_html.replace('<body>', '<body>\n<div class="bg-grain"></div>')

with open(post_path, "w", encoding="utf-8") as f:
    f.write(p_html)

print("✅ post.html master optimizations applied successfully!")

print("All master engineering optimizations completed!")
