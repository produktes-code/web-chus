import re

def optimize_file(filepath):
    print(f"Optimizing performance in {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace autoplay="" on background video cards with preload="metadata"
    content_mod = re.sub(r'<video\s+autoplay=""\s+class="([^"]+)"\s+loop=""\s+muted=""\s+playsinline=""\s+poster="([^"]+)"\s+src="([^"]+)">',
                         r'<video class="\1" loop="" muted="" playsinline="" preload="metadata" poster="\2" src="\3">', content)

    # 2. Add GPU accelerated transition properties on .glass-panel and .service-card-enhanced
    content_mod = content_mod.replace('transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);',
                                      'transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.3s ease, box-shadow 0.3s ease;\n        will-change: transform;\n        transform: translate3d(0, 0, 0);')
    content_mod = content_mod.replace('transition: all 0.5s duration-500',
                                      'transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.3s ease;\n        will-change: transform;\n        transform: translate3d(0, 0, 0);')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content_mod)

    print(f"File {filepath} optimized!")

for fn in ['index.html', 'perfil.html', 'blog.html', 'post.html']:
    optimize_file(fn)
