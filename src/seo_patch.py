#!/usr/bin/env python3
"""SEO overhaul patcher for build/template.html.
Every replacement is anchored and asserted; JSON-LD is built via json.dumps (guaranteed valid).
FAQ schema + visible FAQ HTML are generated from ONE source of truth so they always match.
"""
import json, re, html as htmllib

SITE = "https://www.ogidibrown77.com/"
tpl = open('/home/user/src/template.html', encoding='utf-8').read()
n0 = len(tpl)

def rep(old, new, label):
    global tpl
    assert tpl.count(old) >= 1, f'ANCHOR NOT FOUND: {label}\n---\n{old[:140]}'
    tpl = tpl.replace(old, new, 1)
    print(f'  ✔ {label}')

# =====================================================================
# FAQ — single source of truth for schema + visible HTML (req 8 + 24)
# =====================================================================
FAQS = [
    ("What is Kingmarble?",
     "Kingmarble is a modern decorative panel that reproduces the depth, veining and polished finish of natural marble. It is lighter and more versatile than quarried stone, which makes it ideal for wall panelling, wall cladding, ceilings, cabinetry and washroom finishing."),
    ("Where can Kingmarble be used in a home or office?",
     "Kingmarble works almost anywhere: TV and feature walls, hallway and staircase cladding, sculpted ceilings, wardrobe and cabinet fronts, kitchen surfaces and full washroom finishes — as well as reception desks and facades in commercial spaces."),
    ("Is Kingmarble durable and easy to maintain?",
     "Yes. Kingmarble is hard-wearing and moisture-resistant, with a non-porous surface that simply wipes clean. Unlike paint it never needs repainting, and unlike ceramic tiles there are no grout lines to scrub."),
    ("Do you work outside Kumasi and Accra?",
     "Yes. Our head office is at Ahenema-Kokoben, Kumasi and our branch is at Achimota Overhead, Accra, but we take on residential and commercial projects across Ghana. Send us your location on WhatsApp and we will confirm coverage for your area."),
    ("How do I get a quote, and how long does installation take?",
     "Message us on WhatsApp or call +233 20 206 5920 with photos and rough measurements of your space. Quotes are free, and most feature walls and ceilings are completed within a few days once the design and materials are agreed."),
    ("What other services does Ogidibrown 77 Enterprise offer?",
     "Beyond Kingmarble, we design and build kitchens, wardrobes and furniture, ceilings, bedroom and bathroom schemes, full commercial interiors, and we handle custom art selection, CCTV installation and solar panel installation — one team for the whole project."),
]

# =====================================================================
# JSON-LD @graph (req 8) — WebSite, WebPage, Breadcrumb, Business, FAQ
# =====================================================================
graph = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebSite",
     "@id": SITE + "#website",
     "url": SITE,
     "name": "Ogidibrown 77 Enterprise",
     "inLanguage": "en-GH",
     "publisher": {"@id": SITE + "#business"}},
    {"@type": "WebPage",
     "@id": SITE + "#webpage",
     "url": SITE,
     "name": "Kingmarble Wall Panels in Kumasi | Ogidibrown 77 Enterprise",
     "description": "Premium Kingmarble wall panelling, cladding, ceilings, cabinetry & washroom finishing in Kumasi & Accra, Ghana. 5.0★ rated — get a free quote today.",
     "isPartOf": {"@id": SITE + "#website"},
     "about": {"@id": SITE + "#business"},
     "inLanguage": "en-GH",
     "breadcrumb": {"@id": SITE + "#breadcrumb"},
     "primaryImageOfPage": {"@type": "ImageObject", "url": SITE + "images/hero.jpg", "width": 1376, "height": 768}},
    {"@type": "BreadcrumbList",
     "@id": SITE + "#breadcrumb",
     "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
        {"@type": "ListItem", "position": 2, "name": "Kingmarble Interiors — Kumasi & Accra", "item": SITE + "#main"}]},
    {"@type": "HomeAndConstructionBusiness",
     "@id": SITE + "#business",
     "name": "Ogidibrown 77 Enterprise",
     "alternateName": "Ogidibrown Enterprise",
     "slogan": "Building Your Home with Kingmarble — The Feeling Beyond Nature.",
     "description": "Ogidibrown 77 Enterprise is a Kumasi-based interior décor and building materials company specialising in Kingmarble wall panelling, wall cladding, ceiling design, cabinetry, furniture and washroom finishing, with branches in Ahenema-Kokoben, Kumasi and Achimota Overhead, Accra, Ghana.",
     "url": SITE,
     "telephone": "+233202065920",
     "priceRange": "₵₵",
     "currenciesAccepted": "GHS",
     "paymentAccepted": "Cash, Mobile Money, Bank Transfer",
     "image": SITE + "images/hero.jpg",
     "logo": {"@type": "ImageObject", "url": SITE + "images/logo.png", "width": 512, "height": 512},
     "knowsAbout": ["Kingmarble wall panels", "Wall cladding", "Ceiling design", "Cabinetry and wardrobe design", "Washroom finishing", "Commercial interior design", "CCTV installation", "Solar panel installation"],
     "address": {"@type": "PostalAddress", "streetAddress": "Ahenema-Kokoben", "addressLocality": "Kumasi", "addressRegion": "Ashanti Region", "addressCountry": "GH"},
     "geo": {"@type": "GeoCoordinates", "latitude": 6.6214, "longitude": -1.6169},
     "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "08:00", "closes": "17:30"}],
     "areaServed": [{"@type": "City", "name": "Kumasi"}, {"@type": "City", "name": "Accra"}, {"@type": "Country", "name": "Ghana"}],
     "sameAs": ["https://www.facebook.com/ogidibrownentgh", "https://www.instagram.com/ogb_ghana_limited"],
     "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0", "bestRating": "5", "worstRating": "1", "reviewCount": "3"},
     "review": [
        {"@type": "Review", "author": {"@type": "Person", "name": "Rabeea Almelli"}, "reviewRating": {"@type": "Rating", "ratingValue": "5", "bestRating": "5"}, "reviewBody": "I simply love my new Kingmarble wall. The finish is flawless and the team worked so neatly — my living room in Kumasi now feels like a completely different home."},
        {"@type": "Review", "author": {"@type": "Person", "name": "Nitin K"}, "reviewRating": {"@type": "Rating", "ratingValue": "5", "bestRating": "5"}, "reviewBody": "Professional from the first call to the final polish. The ceiling design and cabinetry were delivered on time and exactly as promised. Five stars, well earned."},
        {"@type": "Review", "author": {"@type": "Person", "name": "Anthony Nana Kofi"}, "reviewRating": {"@type": "Rating", "ratingValue": "5", "bestRating": "5"}, "reviewBody": "Quality materials, honest pricing and craftsmanship you can see. The reception wall they built for my business gets compliments every single day."}],
     "contactPoint": [
        {"@type": "ContactPoint", "telephone": "+233202065920", "contactType": "customer service", "areaServed": "GH", "availableLanguage": ["English", "Twi"]},
        {"@type": "ContactPoint", "telephone": "+233248625845", "contactType": "customer service", "areaServed": "GH"},
        {"@type": "ContactPoint", "telephone": "+233549397382", "contactType": "customer service", "areaServed": "GH"}],
     "department": [
        {"@type": "HomeAndConstructionBusiness", "name": "Ogidibrown 77 Enterprise — Kumasi (Head Office)", "telephone": "+233202065920", "address": {"@type": "PostalAddress", "streetAddress": "Ahenema-Kokoben", "addressLocality": "Kumasi", "addressRegion": "Ashanti Region", "addressCountry": "GH"}},
        {"@type": "HomeAndConstructionBusiness", "name": "Ogidibrown 77 Enterprise — Accra Branch", "telephone": "+233202065920", "address": {"@type": "PostalAddress", "streetAddress": "Achimota Overhead", "addressLocality": "Accra", "addressRegion": "Greater Accra Region", "addressCountry": "GH"}}],
     "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Interior Décor & Installation Services", "itemListElement": [
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s}} for s in
        ["Kingmarble Wall Paneling", "Kingmarble Wall Cladding", "Ceiling Design", "Cabinetry, Wardrobe & Furniture Design", "Washroom Finishing", "Bedroom & Bathroom Design", "Commercial Interior Design", "Custom Art & Appliance Selection", "CCTV Installation", "Solar Panel Installation"]]}
    },
    {"@type": "FAQPage",
     "@id": SITE + "#faq",
     "mainEntity": [{"@type": "Question", "name": q,
                     "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]}
]}
ld_json = json.dumps(graph, ensure_ascii=False, indent=2)
json.loads(ld_json)  # validity gate

start = tpl.index('<script type="application/ld+json">')
end = tpl.index('</script>', start) + len('</script>')
tpl = tpl[:start] + '<script type="application/ld+json">\n' + ld_json + '\n</script>' + tpl[end:]
print('  ✔ JSON-LD replaced with @graph (7 schema types)')

# =====================================================================
# HEAD — title, description, robots, canonical, hreflang (req 4, 6, 12)
# =====================================================================
rep('<title>Ogidibrown 77 Enterprise | Kingmarble Wall Panels, Ceilings &amp; Interiors — Kumasi, Ghana</title>',
    '<title>Kingmarble Wall Panels in Kumasi | Ogidibrown 77 Enterprise</title>',
    'title rewritten (60 chars, keyword-first)')

rep('<meta name="description" content="Ogidibrown 77 Enterprise designs and installs Kingmarble wall panelling, wall cladding, ceilings, cabinetry, furniture and washroom finishing in Kumasi and Accra, Ghana. 5.0★ rated. Get a free quote today.">',
    '<meta name="description" content="Premium Kingmarble wall panelling, cladding, ceilings, cabinetry &amp; washroom finishing in Kumasi &amp; Accra, Ghana. 5.0★ rated — get a free quote today.">',
    'meta description tightened to ~152 chars')

rep('<meta name="robots" content="index, follow">',
    '<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">\n'
    '<meta name="author" content="Ogidibrown 77 Enterprise">\n'
    '<link rel="canonical" href="' + SITE + '">\n'
    '<link rel="alternate" hreflang="en-gh" href="' + SITE + '">\n'
    '<link rel="alternate" hreflang="x-default" href="' + SITE + '">\n'
    '<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">',
    'robots directives + canonical + hreflang + HTTPS-upgrade CSP (req 6, 18, 20)')

# =====================================================================
# Open Graph / Twitter — absolute URLs, url, site_name, dims (req 7)
# =====================================================================
old_og = '''<meta property="og:type" content="website">
<meta property="og:title" content="Ogidibrown 77 Enterprise — Kingmarble Interiors, Kumasi &amp; Accra">
<meta property="og:description" content="Building Your Home with Kingmarble — The Feeling Beyond Nature. Wall panelling, cladding, ceilings, cabinetry, washroom finishing &amp; more. Two branches: Kumasi HQ &amp; Achimota, Accra.">
<meta property="og:image" content="images/hero.jpg">
<meta property="og:locale" content="en_GH">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Ogidibrown 77 Enterprise — Kingmarble Interiors, Kumasi &amp; Accra">
<meta name="twitter:description" content="Premium Kingmarble wall panelling, ceilings, cabinetry and complete interior finishing — crafted in Kumasi, delivered across Ghana.">'''
new_og = '''<meta property="og:type" content="website">
<meta property="og:url" content="''' + SITE + '''">
<meta property="og:site_name" content="Ogidibrown 77 Enterprise">
<meta property="og:title" content="Kingmarble Wall Panels in Kumasi | Ogidibrown 77 Enterprise">
<meta property="og:description" content="Premium Kingmarble wall panelling, cladding, ceilings, cabinetry &amp; washroom finishing in Kumasi &amp; Accra, Ghana. 5.0★ rated — get a free quote today.">
<meta property="og:image" content="''' + SITE + '''images/hero.jpg">
<meta property="og:image:width" content="1376">
<meta property="og:image:height" content="768">
<meta property="og:image:alt" content="Luxurious living room with a book-matched Kingmarble feature wall by Ogidibrown 77 Enterprise, Kumasi">
<meta property="og:locale" content="en_GH">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Kingmarble Wall Panels in Kumasi | Ogidibrown 77 Enterprise">
<meta name="twitter:description" content="Premium Kingmarble wall panelling, cladding, ceilings, cabinetry &amp; washroom finishing in Kumasi &amp; Accra, Ghana. 5.0★ rated — get a free quote today.">
<meta name="twitter:image" content="''' + SITE + '''images/hero.jpg">'''
rep(old_og, new_og, 'Open Graph + Twitter Card hardened (req 7)')

# === GSC verification placeholder (req 21) ===
rep('<meta name="ICBM" content="6.6214, -1.6169">',
    '<meta name="ICBM" content="6.6214, -1.6169">\n\n'
    '<!-- Google Search Console verification — paste your token from https://search.google.com/search-console (HTML tag method) -->\n'
    '<meta name="google-site-verification" content="PASTE_YOUR_GSC_VERIFICATION_TOKEN_HERE">',
    'Google Search Console verification placeholder (req 21)')

# === dns-prefetch + GA4 placeholder (req 10, 22) ===
fonts_line = '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Jost:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">'
ga4 = fonts_line + '''
<link rel="dns-prefetch" href="https://fonts.googleapis.com">
<link rel="dns-prefetch" href="https://fonts.gstatic.com">
<link rel="dns-prefetch" href="https://www.googletagmanager.com">

<!-- Google Analytics 4 — replace G-XXXXXXXXXX with your Measurement ID; loader self-activates once set (req 22) -->
<script>
(function () {
  var GA_MEASUREMENT_ID = 'G-XXXXXXXXXX'; /* TODO: replace with your real GA4 Measurement ID */
  if (!GA_MEASUREMENT_ID || GA_MEASUREMENT_ID.indexOf('XXXX') !== -1) return;
  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_MEASUREMENT_ID;
  document.head.appendChild(s);
  window.dataLayer = window.dataLayer || [];
  function gtag(){ window.dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag('js', new Date());
  gtag('config', GA_MEASUREMENT_ID);
})();
</script>'''
rep(fonts_line, ga4, 'GA4 placeholder loader + dns-prefetch resource hints (req 22, 10)')

# =====================================================================
# CSS — contrast (WCAG, req 19), perf (req 10), FAQ styles (req 24)
# =====================================================================
rep('--gold-deep:#8C6C3F;', '--gold-deep:#7E6136;', 'gold-deep darkened for 4.5:1 contrast (WCAG AA)')
rep('.loc-city{font-size:.82rem;letter-spacing:.2em;text-transform:uppercase;color:var(--taupe);margin-bottom:20px}',
    '.loc-city{font-size:.82rem;letter-spacing:.2em;text-transform:uppercase;color:#7C7466;margin-bottom:20px}',
    'loc-city contrast fix')
rep('.svc-num{position:absolute;top:18px;right:22px;font-family:var(--serif);font-size:1.5rem;color:var(--taupe);opacity:.5;font-style:italic}',
    '.svc-num{position:absolute;top:18px;right:22px;font-family:var(--serif);font-size:1.5rem;color:#8F887A;opacity:.55;font-style:italic}',
    'svc-num contrast bump')
rep('.compare-cell.old{color:rgba(247,243,234,.55);background:rgba(0,0,0,.14)}',
    '.compare-cell.old{color:rgba(247,243,234,.62);background:rgba(0,0,0,.14)}',
    'compare-cell contrast bump')
rep('.site-header.scrolled .b-name strong{color:var(--ink)}',
    '.site-header.scrolled .b-name strong{color:var(--ink)}\n.site-header.scrolled .b-name span{color:var(--gold-deep)}',
    'scrolled brand subtitle contrast fix')

a11y_perf_faq_css = '''
/* ---------- accessibility & rendering performance (req 10, 19) ---------- */
:focus-visible{outline:2px solid var(--gold);outline-offset:3px;border-radius:3px}
main section:not(#home){content-visibility:auto;contain-intrinsic-size:auto 880px}

/* ---------- faq accordion (req 24) ---------- */
.faq-list{max-width:860px;margin:0 auto;display:grid;gap:14px}
.faq-item{background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;transition:border-color .3s,box-shadow .3s}
.faq-item[open]{border-color:var(--line-strong);box-shadow:var(--shadow)}
.faq-item summary{list-style:none;cursor:pointer;display:flex;align-items:center;justify-content:space-between;gap:16px;padding:20px 26px;font-family:var(--serif);font-weight:600;font-size:1.18rem;color:var(--ink)}
.faq-item summary::-webkit-details-marker{display:none}
.faq-item summary:hover{color:var(--gold-deep)}
.faq-ic{flex:none;width:30px;height:30px;border-radius:50%;border:1px solid var(--line-strong);display:grid;place-items:center;color:var(--gold-deep);transition:transform .35s,background .35s,color .35s,border-color .35s}
.faq-ic .icon{width:14px;height:14px}
.faq-item[open] .faq-ic{transform:rotate(45deg);background:var(--gold);color:#fff;border-color:var(--gold)}
.faq-a{padding:0 26px 22px;color:var(--ink-2);font-size:.95rem}
.faq-a p{max-width:64ch}
.faq-more{margin-top:30px;font-size:.92rem;color:var(--ink-2)}
.faq-more a{color:var(--gold-deep);font-weight:500;border-bottom:1px solid var(--line-strong)}
.faq-more a:hover{color:var(--gold)}
'''
rep('/* ---------- responsive ---------- */', a11y_perf_faq_css + '\n/* ---------- responsive ---------- */',
    'focus-visible, content-visibility, FAQ CSS added')

# breakpoint switch so the new FAQ nav link never collides with the CTA
rep('@media(max-width:1080px){\n  .nav-menu{gap:18px}\n  .nav-cta{display:none}\n}',
    '@media(max-width:1180px){\n  .nav-menu{gap:16px}\n  .nav-cta{display:none}\n}',
    'nav breakpoint widened for new FAQ link')

# heading-hierarchy fixes (req 5): info-block + footer h4 → h3
rep('.info-block h4{', '.info-block h3{', 'info-block selector h4→h3')
rep('.f-col h4{', '.f-col h3{', 'footer selector h4→h3')
for t in ['Call or Chat — We Answer', 'Opening Hours', 'Follow Our Latest Work']:
    rep(f'<h4>{t}</h4>', f'<h3>{t}</h3>', f'info-block heading "{t[:20]}…" → h3')
for t in ['Explore', 'Popular Services', 'Talk to Us']:
    rep(f'<h4>{t}</h4>', f'<h3>{t}</h3>', f'footer heading "{t}" → h3')

# =====================================================================
# BODY — icon, nav link, FAQ section, footer link (req 15, 24)
# =====================================================================
rep('    <g stroke-linecap="round" stroke-linejoin="round">',
    '    <symbol id="i-plus" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" d="M12 5v14M5 12h14"/></symbol>\n    <g stroke-linecap="round" stroke-linejoin="round">',
    'i-plus icon added to sprite')

rep('        <li><a class="nav-link" href="#why">Why Kingmarble</a></li>',
    '        <li><a class="nav-link" href="#why">Why Kingmarble</a></li>\n        <li><a class="nav-link" href="#faq">FAQ</a></li>',
    'FAQ added to primary nav')

faq_items = '\n'.join(
    f'''      <details class="faq-item">
        <summary><span>{htmllib.escape(q)}</span><span class="faq-ic" aria-hidden="true"><svg class="icon"><use href="#i-plus"/></svg></span></summary>
        <div class="faq-a"><p>{htmllib.escape(a)}</p></div>
      </details>''' for q, a in FAQS)

faq_section = f'''<!-- ======================= FAQ ======================= -->
<section class="sec sec-faq" id="faq" aria-labelledby="faq-title">
  <div class="wrap">
    <header class="sec-head center reveal">
      <p class="eyebrow">Good to Know</p>
      <h2 id="faq-title">Kingmarble <em>Questions, Answered</em></h2>
      <div class="divider" aria-hidden="true"><span class="line"></span><span class="diamond"></span><span class="line"></span></div>
      <p class="sec-sub">Everything homeowners and business clients ask us before their first Kingmarble project in Kumasi or Accra.</p>
    </header>
    <div class="faq-list reveal">
{faq_items}
    </div>
    <p class="faq-more center reveal">Still deciding? <a href="#contact">Send us your space on WhatsApp</a> — we reply within hours.</p>
  </div>
</section>

'''
rep('<!-- ======================= TESTIMONIALS ======================= -->',
    faq_section + '<!-- ======================= TESTIMONIALS ======================= -->',
    'FAQ section inserted (visible content matches FAQPage schema)')

rep('          <li><a href="#why">Why Kingmarble</a></li>',
    '          <li><a href="#why">Why Kingmarble</a></li>\n          <li><a href="#faq">FAQ</a></li>',
    'FAQ added to footer links')

# === 10 service cards: span.svc-link → internal anchor that pre-selects the form (req 15) ===
SVC_MAP = {
    'Wall Paneling': 'Kingmarble Wall Paneling',
    'Wall Cladding': 'Kingmarble Wall Cladding',
    'Ceiling Design': 'Ceiling Design',
    'Cabinetry &amp; Furniture': 'Cabinetry &amp; Furniture',
    'Washroom Finishing': 'Washroom Finishing',
    'Bedroom &amp; Bathroom Design': 'Bedroom &amp; Bathroom Design',
    'Commercial Interior Design': 'Commercial Interior Design',
    'Custom Art Selection': 'Custom Art Selection',
    'CCTV Installation': 'CCTV Installation',
    'Solar Panel Installation': 'Solar Panel Installation',
}
chunks = tpl.split('</article>')
converted = 0
for i, ch in enumerate(chunks):
    if 'class="svc-link"' in ch:
        m = re.search(r'<h3>(.*?)</h3>', ch)
        assert m, 'svc card missing h3'
        svc = SVC_MAP[m.group(1)]
        ch = ch.replace('<span class="svc-link">', f'<a class="svc-link" href="#contact" data-service="{svc}">', 1)
        ch = ch.replace('</svg></span>', '</svg></a>', 1)
        chunks[i] = ch
        converted += 1
tpl = '</article>'.join(chunks)
assert converted == 10, f'svc-link conversions: {converted}'
print('  ✔ 10 service cards now deep-link to the quote form (internal linking, req 15)')

# =====================================================================
# JS — aria-current, svc preselect, lightbox focus management, FAQ accordion (req 19)
# =====================================================================
rep('        links.forEach(l => l.classList.remove(\'active\'));',
    '        links.forEach(l => { l.classList.remove(\'active\'); l.removeAttribute(\'aria-current\'); });',
    'spy clears aria-current')
rep('        if (l) l.classList.add(\'active\');',
    '        if (l) { l.classList.add(\'active\'); l.setAttribute(\'aria-current\', \'true\'); }',
    'spy sets aria-current (WCAG)')
rep('  let gIndex = 0;\n  function openLb(i){\n    gIndex = (i + tiles.length) % tiles.length;',
    '  let gIndex = 0, lbOpener = null;\n  function openLb(i){\n    if (!lb.classList.contains(\'open\')) lbOpener = document.activeElement;\n    gIndex = (i + tiles.length) % tiles.length;',
    'lightbox remembers opener')
rep('    lb.classList.add(\'open\');\n    document.body.style.overflow = \'hidden\';\n  }',
    '    lb.classList.add(\'open\');\n    document.body.style.overflow = \'hidden\';\n    document.getElementById(\'lbClose\').focus();\n  }',
    'lightbox moves focus on open')
rep('  function closeLb(){\n    lb.classList.remove(\'open\');\n    document.body.style.overflow = \'\';\n  }',
    '  function closeLb(){\n    lb.classList.remove(\'open\');\n    document.body.style.overflow = \'\';\n    if (lbOpener && lbOpener.focus) lbOpener.focus();\n  }',
    'lightbox returns focus on close')

js_add = '''
  /* ---------- service card clicks pre-select the matching quote-form service ---------- */
  const fServiceSel = document.getElementById('fService');
  document.querySelectorAll('.svc-link').forEach(a => {
    a.addEventListener('click', () => { if (a.dataset.service && fServiceSel) fServiceSel.value = a.dataset.service; });
  });

  /* ---------- FAQ accordion: one item open at a time ---------- */
  document.querySelectorAll('.faq-item').forEach(d => {
    d.addEventListener('toggle', () => {
      if (d.open) document.querySelectorAll('.faq-item[open]').forEach(o => { if (o !== d) o.open = false; });
    });
  });

'''
rep('  /* ---------- footer year ---------- */', js_add + '  /* ---------- footer year ---------- */',
    'svc preselect + FAQ accordion JS')

open('/home/user/src/template.html', 'w', encoding='utf-8').write(tpl)
print(f'\nPATCH COMPLETE: {n0:,} → {len(tpl):,} chars | all anchors matched')
