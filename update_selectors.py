import re
from bs4 import BeautifulSoup

def update_html_selectors(file_path):
    print(f"Updating selectors in {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    soup = BeautifulSoup(html, 'html.parser')
    
    # 1. Update desktop selector #lang-select
    desktop_select = soup.find('select', id='lang-select')
    if desktop_select:
        is_blog_or_post = "blog" in file_path or "post" in file_path
        
        if is_blog_or_post:
            new_options = """
            <option value="es" style="background: #000;">🇪🇸 ESPAÑOL</option>
            <option value="ca" style="background: #000;">🚩 CATALÀ</option>
            <option value="en" style="background: #000;">🇬🇧 ENGLISH</option>
            <option value="it" style="background: #000;">🇮🇹 ITALIANO</option>
            <option value="de" style="background: #000;">🇩🇪 DEUTSCH</option>
            <option value="ru" style="background: #000;">🇷🇺 РУССКИЙ</option>
            <option value="ja" style="background: #000;">🇯🇵 日本語</option>
            <option value="uk" style="background: #000;">🇺🇦 УКРАЇНСЬКА</option>
            <option value="zh-CN" style="background: #000;">🇨🇳 中文</option>
            <option value="ar" style="background: #000;">🇸🇦 العربية</option>
            """
        else:
            new_options = """
            <option value="es">🇪🇸 ES</option>
            <option value="ca">🚩 CA</option>
            <option value="en">🇬🇧 EN</option>
            <option value="it">🇮🇹 IT</option>
            <option value="de">🇩🇪 DE</option>
            <option value="ru">🇷🇺 RU</option>
            <option value="ja">🇯🇵 JA</option>
            <option value="uk">🇺🇦 UK</option>
            <option value="zh-CN">🇨🇳 ZH</option>
            <option value="ar">🇸🇦 AR</option>
            """
        desktop_select.clear()
        desktop_select.append(BeautifulSoup(new_options, 'html.parser'))
        
    # 2. Update mobile selector #mobile-lang-select (if present)
    mobile_select = soup.find('select', id='mobile-lang-select')
    if mobile_select:
        new_mobile_options = """
        <option value="es" style="background: #000;">🇪🇸 ESPAÑOL</option>
        <option value="ca" style="background: #000;">🚩 CATALÀ</option>
        <option value="en" style="background: #000;">🇬🇧 ENGLISH</option>
        <option value="it" style="background: #000;">🇮🇹 ITALIANO</option>
        <option value="de" style="background: #000;">🇩🇪 DEUTSCH</option>
        <option value="ru" style="background: #000;">🇷🇺 РУССКИЙ</option>
        <option value="ja" style="background: #000;">🇯🇵 日本語</option>
        <option value="uk" style="background: #000;">🇺🇦 УКРАЇНСЬКА</option>
        <option value="zh-CN" style="background: #000;">🇨🇳 中文</option>
        <option value="ar" style="background: #000;">🇸🇦 العربية</option>
        """
        mobile_select.clear()
        mobile_select.append(BeautifulSoup(new_mobile_options, 'html.parser'))
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Successfully updated selectors in {file_path}")

for fn in ['index.html', 'perfil.html', 'blog.html', 'post.html']:
    update_html_selectors(fn)
