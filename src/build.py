#!/usr/bin/env python3
"""Build index.html from src/template.html — inlines images as compressed JPEG
data URIs and injects width/height/decoding attributes (CLS-safe, async decode)."""
import base64, io, os
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# token -> (file, max width, quality, width attr, height attr, extra attrs)
JOBS = {
    '%%IMG_HERO%%': ('images/hero.jpg',               1376, 77, 1376, 768, ''),
    '%%IMG_ABOUT%%': ('images/photo_2026-07-19_10-31-38.jpg', 1100, 72, 1408, 768, 'decoding="async" '),
    '%%IMG_G1%%':    ('images/gallery-ceiling.jpg',   1100, 72, 1408, 768, 'decoding="async" '),
    '%%IMG_G2%%':    ('images/gallery-tvwall.jpg',    1100, 72, 1408, 768, 'decoding="async" '),
    '%%IMG_G3%%':    ('images/gallery-kitchen.jpg',   1100, 72, 1408, 768, 'decoding="async" '),
    '%%IMG_G4%%':    ('images/gallery-bathroom.jpg',  1100, 72, 1408, 768, 'decoding="async" '),
    '%%IMG_G5%%':    ('images/gallery-bedroom.jpg',   1100, 72, 1408, 768, 'decoding="async" '),
    '%%IMG_G6%%':    ('images/gallery-commercial.jpg',1300, 73, 1408, 768, 'decoding="async" '),
    '%%IMG_G7%%':    ('images/gallery-staircase.jpg', 1100, 72, 1408, 768, 'decoding="async" '),
    '%%IMG_G8%%':    ('images/gallery-wardrobe.jpg',  1100, 72, 1408, 768, 'decoding="async" '),
    '%%IMG_G9%%':    ('images/gallery-samples.jpg',   1100, 72, 1408, 768, 'decoding="async" '),
    '%%IMG_G10%%':   ('images/gallery-exterior.jpg',  1300, 73, 1408, 768, 'decoding="async" '),
    '%%IMG_G11%%':   ('images/gallery-solar.jpg',     1100, 72, 1408, 768, 'decoding="async" '),
    '%%IMG_G12%%':   ('images/photo_2026-07-19_10-31-38.jpg', 1100, 72, 1408, 768, 'decoding="async" '),
    '%%IMG_G13%%':   ('images/photo_2026-07-19_10-31-42.jpg', 1100, 72, 1408, 768, 'decoding="async" '),
    '%%IMG_G14%%':   ('images/photo_2026-07-19_10-31-45.jpg', 1100, 72, 1408, 768, 'decoding="async" '),
    '%%IMG_G15%%':   ('images/photo_2026-07-19_10-31-46.jpg', 1100, 72, 1408, 768, 'decoding="async" '),
    '%%IMG_G16%%':   ('images/photo_2026-07-19_10-31-49.jpg', 1100, 72, 1408, 768, 'decoding="async" '),
    '%%IMG_G17%%':   ('images/photo_2026-07-19_10-31-53.jpg', 1100, 72, 1408, 768, 'decoding="async" '),
    '%%IMG_G18%%':   ('images/photo_2026-07-19_10-31-56.jpg', 1100, 72, 1408, 768, 'decoding="async" '),
    '%%IMG_G19%%':   ('images/photo_2026-07-19_10-31-58.jpg', 1100, 72, 1408, 768, 'decoding="async" '),
    '%%IMG_G20%%':   ('images/photo_2026-07-19_10-32-01.jpg', 1100, 72, 1408, 768, 'decoding="async" '),
    '%%IMG_G21%%':   ('images/photo_2026-07-19_10-32-03.jpg', 1100, 72, 1408, 768, 'decoding="async" '),
    '%%IMG_G22%%':   ('images/photo_2026-07-19_10-32-06.jpg', 1100, 72, 1408, 768, 'decoding="async" '),
    '%%IMG_G23%%':   ('images/photo_2026-07-19_10-32-18.jpg', 1100, 72, 1408, 768, 'decoding="async" '),
    '%%IMG_G24%%':   ('images/photo_2026-07-19_10-32-20.jpg', 1100, 72, 1408, 768, 'decoding="async" '),
    '%%IMG_G25%%':   ('images/photo_2026-07-19_10-32-23.jpg', 1100, 72, 1408, 768, 'decoding="async" '),
}

def enc(path, maxw, q):
    im = Image.open(os.path.join(ROOT, path)).convert('RGB')
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    b = io.BytesIO()
    im.save(b, 'JPEG', quality=q, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()

html = open(os.path.join(ROOT, 'src/template.html'), encoding='utf-8').read()
for token, (p, w, q, wa, ha, extra) in JOBS.items():
    assert f'src="{token}"' in html, f'MISSING {token}'
    uri = enc(p, w, q)
    html = html.replace(f'src="{token}"', f'width="{wa}" height="{ha}" {extra}src="{uri}"')
    print(f'  {p:34s} -> {len(uri)/1024:6.0f} KB')

assert '%%IMG' not in html, 'unreplaced tokens remain'
out = os.path.join(ROOT, 'index.html')
open(out, 'w', encoding='utf-8').write(html)
print(f'\nindex.html: {len(html.encode())/1048576:.2f} MB — BUILD OK')
