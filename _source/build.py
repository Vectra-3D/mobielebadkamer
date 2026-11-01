#!/usr/bin/env python3
"""Static site builder for the Mobiele Badkamer redesign.
Shared header/footer + per-page bodies -> ../**/index.html
Links are written as relative .../index.html so the site works from disk and on any host.
"""
import json, os, html

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://mobielebadkamer.info"
PHONE_D = "06 54 25 47 40"
PHONE_T = "+31654254740"
MAIL = "info@mobielebadkamer.info"
REVIEWS = "https://www.google.com/maps/place/Mobiele+Badkamer+-+Een+tijdelijke+mobiele+badkamer+huren%3F+Wij+bieden+interessante+opties!/@52.9297283,5.705707,15z/data=!4m6!3m5!1s0x47b8089ed1d982dd:0xed24cf59d8aee0cb!8m2!3d52.9297283!4d5.705707!16s%2Fg%2F11bzywgtc5"
NONSTOP = "https://nonstop-riool.nl/"
VIMEO = "1084533544"

# ---------------------------------------------------------------- icons
I = {
 "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>',
 "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12Z"/><circle cx="12" cy="9" r="2.5"/></svg>',
 "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
 "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg>',
 "minus": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M6 12h12"/></svg>',
 "plus": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>',
 "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
 "close": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>',
 "left": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m15 5-7 7 7 7"/></svg>',
 "right": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 5 7 7-7 7"/></svg>',
 "play": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 4.5v15l13-7.5z"/></svg>',
 "alert": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7.5v5.5M12 16.5h.01"/></svg>',
 "star": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/></svg>',
 "bulb": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9c.6.4 1 1.1 1 1.8V16h5v-.3c0-.7.4-1.4 1-1.8A6 6 0 0 0 12 3"/></svg>',
 "hanger": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 8a2 2 0 1 1 2-2c0 1-2 1.5-2 3l9 6.5a1.4 1.4 0 0 1-.8 2.5H3.8a1.4 1.4 0 0 1-.8-2.5L12 9"/></svg>',
 "curtain": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 4h18M6 4c0 6 1 10-1 16M10 4c0 6 1 10-1 16M14 4c0 6-1 10 1 16M18 4c0 6-1 10 1 16"/></svg>',
}
def ic(n): return I[n]

def picture(name, alt, sizes, widths=(480, 960, 1600), cls="", eager=False, w=None, h=None, root=""):
    srcset = ", ".join(f"{root}assets/img/{name}-{x}.webp {x}w" for x in widths if os.path.exists(f"{OUT}/assets/img/{name}-{x}.webp"))
    biggest = [x for x in widths if os.path.exists(f"{OUT}/assets/img/{name}-{x}.webp")][-1]
    if w is None:
        from PIL import Image
        im = Image.open(f"{OUT}/assets/img/{name}-{biggest}.webp"); w, h = im.size
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    avail = [x for x in widths if os.path.exists(f"{OUT}/assets/img/{name}-{x}.webp")]
    srcw = max([x for x in avail if x <= 960] or avail[:1])
    return f'<img{c} src="{root}assets/img/{name}-{srcw}.webp" srcset="{srcset}" sizes="{sizes}" width="{w}" height="{h}" alt="{html.escape(alt)}" {load}>'

# ---------------------------------------------------------------- shared FAQ data (said once, reused)
FAQ_BADKAMER = [
 ("Wat kost een mobiele badkamer huren?", "<strong>€137,50 per week, exclusief 21% btw</strong> (€166,38 inclusief btw). De minimale huurperiode is 14 dagen."),
 ("Wat zit er in de mobiele badkamer?", "Een douche met warm water en douchegordijn, een gewoon toilet, een wastafel met spiegel en stopcontact, een elektrische convectorkachel, verlichting en kledinghaakjes."),
 ("Hoe komt de badkamer bij mij thuis?", "Wij zetten de badkamer op de juiste plek en sluiten water en stroom aan. Na de verbouwing halen we hem weer op. Liever zelf? Je mag hem achter iedere auto met een trekhaak vervoeren."),
 ("Is de badkamer verwarmd?", "Ja. Elke unit heeft een elektrische convectorkachel, dus ook in de winter douche je warm."),
 ("Heeft de badkamer stroom en licht?", "Ja. Er is verlichting en naast de wastafel zit een stopcontact, handig voor scheren, föhnen of het opladen van je tandenborstel."),
 ("Hoe groot is de mobiele badkamer?", "199 cm breed, 305 cm lang (zonder dissel) en 280 cm hoog. De dissel is 150 cm, dus reken op ongeveer 4,6 × 2 meter ruimte. De unit weegt 1300 kg en de boiler is 2500 watt."),
]
FAQ_CABINE = [
 ("Wat kost een mobiele douchecabine huren?", "<strong>€129 voor de eerste week en €99 per volgende week, inclusief btw.</strong>"),
 ("Wat heb ik nodig om de douchecabine aan te sluiten?", "Alleen een stopcontact en een koudwaterkraan. De aan- en afvoerslang krijg je mee; de ingebouwde boiler maakt het water warm en een pompje voert het af."),
 ("Past de douchecabine door mijn deur en onder mijn plafond?", "Ja. Hij is 78 cm breed en 200 cm hoog, en staat op wieltjes."),
 ("Hoe vervoer ik de douchecabine?", "In vrijwel iedere ruimere auto of op een aanhanger. We kunnen hem ook voor je plaatsen."),
]
FAQ_GENERAL = [
 ("Zijn de prijzen inclusief of exclusief btw?", "De mobiele badkamer is geprijsd <strong>exclusief</strong> btw, de douchecabine <strong>inclusief</strong> btw. Op elke pagina staat het er steeds bij."),
 ("Hoe snel kan ik huren?", "Vraag je periode aan via het formulier of bel ons op werkdagen tussen 08:00 en 17:00. We laten je zo snel mogelijk weten of er een unit vrij is."),
]

def faq_html(items, open_first=False):
    out = ['<div class="faq">']
    for n, (q, a) in enumerate(items):
        o = " open" if (open_first and n == 0) else ""
        out.append(f'<details{o}><summary><span>{q}</span><span class="pm">{ic("plus")}</span></summary><div class="answer"><p>{a}</p></div></details>')
    out.append("</div>")
    return "\n".join(out)

def faq_schema(items):
    import re
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in items]}

LOCAL_BUSINESS = {
 "@context": "https://schema.org", "@type": "LocalBusiness", "name": "Mobiele Badkamer",
 "url": SITE + "/", "telephone": PHONE_T, "email": MAIL,
 "image": SITE + "/assets/img/badkamer-oprit-og.jpg",
 "parentOrganization": {"@type": "Organization", "name": "Nonstop Rioolreiniging", "url": NONSTOP},
 "address": {"@type": "PostalAddress", "streetAddress": "Lytse Mar 4", "postalCode": "8523 NN", "addressLocality": "Idskenhuizen", "addressRegion": "Friesland", "addressCountry": "NL"},
 "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "17:00"}],
 "makesOffer": [
   {"@type": "Offer", "name": "Mobiele badkamer huren", "price": "137.50", "priceCurrency": "EUR", "priceSpecification": {"@type": "UnitPriceSpecification", "price": "137.50", "priceCurrency": "EUR", "unitText": "week", "valueAddedTaxIncluded": False}},
   {"@type": "Offer", "name": "Mobiele douchecabine huren", "price": "129.00", "priceCurrency": "EUR", "priceSpecification": {"@type": "UnitPriceSpecification", "price": "129.00", "priceCurrency": "EUR", "unitText": "eerste week", "valueAddedTaxIncluded": True}}],
}

NAV = [("onze-badkamers", "Mobiele badkamer"), ("mobiele-douchecabines", "Douchecabine"), ("veelgestelde-vragen", "Vragen & prijzen"), ("contact", "Contact")]

def page(slug, title, desc, body, schema=(), og_img="badkamer-oprit-og.jpg", body_class=""):
    depth = 0 if slug == "" else 1
    root = "../" * depth
    link = lambda s: f"{root}{s + '/' if s else ''}index.html"
    canon = f"{SITE}/{slug + '/' if slug else ''}"
    cur = lambda s: ' aria-current="page"' if s == slug else ""
    nav = "".join(f'<li><a href="{link(s)}"{cur(s)}>{t}</a></li>' for s, t in NAV)
    mnav = "".join(f'<li><a href="{link(s)}"{cur(s)}>{t} <span aria-hidden="true">→</span></a></li>' for s, t in [("", "Home")] + NAV)
    schemas = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schema)
    b = body.replace("{root}", root)
    return f"""<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:locale" content="nl_NL">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}/assets/img/{og_img}">
<meta name="theme-color" content="#0963b5">
<link rel="icon" href="{root}assets/img/favicon.png">
<link rel="preload" href="{root}assets/fonts/bricolage.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{root}assets/fonts/atkinson.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{root}assets/css/site.css">
{schemas}
</head>
<body class="{body_class}">
<a class="skip-link" href="#main">Naar de inhoud</a>
<header class="site-header">
  <div class="wrap site-header__inner">
    <a class="brand" href="{link('')}"><img src="{root}assets/img/logo-kleur.png" width="397" height="71" alt="Mobiele Badkamer, naar de homepage"></a>
    <nav class="nav" aria-label="Hoofdmenu"><ul>{nav}</ul></nav>
    <div class="header-actions">
      <a class="header-phone" href="tel:{PHONE_T}">{ic('phone')}<span class="num">{PHONE_D}</span><span class="visually-hidden"> (bellen)</span></a>
      <a class="btn btn--primary" href="{link('contact')}">Beschikbaarheid aanvragen</a>
      <button class="menu-toggle" type="button" data-menu-open aria-expanded="false" aria-controls="menu">{ic('menu')}Menu</button>
    </div>
  </div>
</header>
<dialog class="menu-dialog" id="menu" aria-label="Menu">
  <div class="menu-dialog__top">
    <a class="brand" href="{link('')}"><img src="{root}assets/img/logo-kleur.png" width="397" height="71" alt="Mobiele Badkamer, naar de homepage" style="width:168px"></a>
    <button class="icon-btn" type="button" data-menu-close aria-label="Menu sluiten">{ic('close')}</button>
  </div>
  <nav aria-label="Mobiel menu"><ul>{mnav}</ul></nav>
  <div class="menu-dialog__cta">
    <a class="btn btn--primary btn--lg" href="{link('contact')}">Beschikbaarheid aanvragen</a>
    <a class="btn btn--lg" href="tel:{PHONE_T}">{ic('phone')}Bel {PHONE_D}</a>
    <p class="small muted">Bereikbaar ma t/m vr, 08:00–17:00</p>
  </div>
</dialog>

<main id="main">
{b}
</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="{root}assets/img/logo-wit.png" width="397" height="71" alt="Mobiele Badkamer" loading="lazy">
        <p>Tijdelijke badkamers en douchecabines voor tijdens de verbouwing. Onderdeel van <a href="{NONSTOP}">Nonstop Rioolreiniging</a>.</p>
      </div>
      <div>
        <h2>Huren</h2>
        <ul>
          <li><a href="{link('onze-badkamers')}">Mobiele badkamer</a></li>
          <li><a href="{link('mobiele-douchecabines')}">Mobiele douchecabine</a></li>
          <li><a href="{link('veelgestelde-vragen')}">Vragen &amp; prijzen</a></li>
          <li><a href="{link('douchen-tijdens-verbouwing-badkamer')}">Douchen tijdens de verbouwing</a></li>
        </ul>
      </div>
      <div>
        <h2>Contact</h2>
        <ul>
          <li><a href="tel:{PHONE_T}" class="num">{PHONE_D}</a></li>
          <li><a href="mailto:{MAIL}">{MAIL}</a></li>
          <li>Ma t/m vr, <span class="num">08:00–17:00</span></li>
        </ul>
      </div>
      <div>
        <h2>Adres</h2>
        <address style="font-style:normal">Lytse Mar 4<br>8523 NN Idskenhuizen<br>Friesland</address>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 Mobiele Badkamer</span>
      <a href="{REVIEWS}">Bekijk onze reviews op Google</a>
    </div>
  </div>
</footer>

<div class="action-bar" aria-label="Snelle acties">
  <a class="btn" href="tel:{PHONE_T}">{ic('phone')}Bellen</a>
  <a class="btn btn--primary" href="{link('contact')}">Aanvragen</a>
</div>
<script src="{root}assets/js/site.js" defer></script>
</body>
</html>
"""

def write(slug, content):
    d = os.path.join(OUT, slug) if slug else OUT
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(content)

# shared fragments ---------------------------------------------------------
def band(root_hint=True):
    return f"""
<section class="band" aria-labelledby="band-title">
  <div class="wrap band__inner">
    <div>
      <h2 id="band-title">Wanneer begint je verbouwing?</h2>
      <p>Geef je periode door. We laten je snel weten of er een badkamer vrij is, en wat het kost.</p>
    </div>
    <form class="quick-form" action="{{root}}contact/index.html" method="get" data-quick>
      <div class="field"><label for="q-vanaf">Vanaf</label><input id="q-vanaf" name="vanaf" type="date" required></div>
      <div class="field"><label for="q-tot">Tot en met</label><input id="q-tot" name="tot" type="date" required></div>
      <div class="field field--full"><label for="q-product">Wat wil je huren?</label>
        <select id="q-product" name="product"><option value="badkamer">Mobiele badkamer (buiten)</option><option value="douchecabine">Mobiele douchecabine (binnen)</option></select></div>
      <button class="btn btn--primary btn--lg" type="submit">Verder naar aanvraag</button>
      <p class="hint">Nog niets vast. Liever bellen? <a href="tel:{PHONE_T}" class="num">{PHONE_D}</a></p>
    </form>
  </div>
</section>"""

def amenities_list():
    return f"""
<ol class="amenities">
  <li><span class="n">1</span><div><h3>Toilet</h3><p>Een gewoon toilet, ook fijn als je huis maar één wc heeft.</p></div></li>
  <li><span class="n">2</span><div><h3>Wastafel</h3><p>Met warm water. Tandenpoetsen hoeft niet meer in de keuken.</p></div></li>
  <li><span class="n">3</span><div><h3>Spiegel en plankje</h3><p>Voor scheren, make-up en je spullen.</p></div></li>
  <li><span class="n">4</span><div><h3>Stopcontact</h3><p>Voor de föhn, scheerapparaat of tandenborstel.</p></div></li>
  <li><span class="n">5</span><div><h3>Elektrische kachel</h3><p>Een convectorkachel houdt de unit lekker warm.</p></div></li>
  <li><span class="n">6</span><div><h3>Kledinghaakje</h3><p>Je kleren blijven droog terwijl je doucht.</p></div></li>
  <li><span class="n n--plain">{ic('curtain')}</span><div><h3>Douche met gordijn</h3><p>Warme douche (boiler 2500 W) met een stevig douchegordijn.</p></div></li>
  <li><span class="n n--plain">{ic('bulb')}</span><div><h3>Verlichting</h3><p>Ook 's avonds en in de winter goed licht.</p></div></li>
</ol>"""

HOTSPOTS = [("27%", "64%", "Toilet"), ("74%", "46%", "Wastafel"), ("63%", "21%", "Spiegel"), ("50%", "17%", "Stopcontact"), ("91%", "66%", "Kachel"), ("6%", "45%", "Kledinghaakje")]
def hotspot_photo(root="{root}"):
    spots = "".join(f'<span class="hotspot" style="--x:{x};--y:{y};--i:{n}" aria-hidden="true">{n+1}</span>' for n, (x, y, _) in enumerate(HOTSPOTS))
    return f"""<figure class="hotspots" style="margin:0">
  {picture('interieur-toilet-wastafel', 'Binnen in de mobiele badkamer: toilet, wastafel met spiegel, stopcontact, kachel en kledinghaakje', '(max-width: 860px) 92vw, 30rem', root=root)}
  {spots}
</figure>"""

# ======================================================================= HOME
home = f"""
<section class="hero" aria-labelledby="hero-title">
  <div class="wrap hero__grid">
    <div class="hero__copy">
      <h1 id="hero-title">Gewoon thuis douchen, <span class="accent">ook tijdens de verbouwing.</span></h1>
      <p class="hero__lead">Een complete badkamer op je oprit: warme douche, toilet, wastafel en verwarming. Wij brengen hem, sluiten water en stroom aan en halen hem weer op als je klaar bent.</p>
      <div class="btn-row">
        <a class="btn btn--primary btn--lg" href="{{root}}contact/index.html">Beschikbaarheid aanvragen</a>
        <a class="btn btn--on-blue btn--lg" href="tel:{PHONE_T}">{ic('phone')}<span>Bel <span class="num">{PHONE_D}</span></span></a>
      </div>
      <ul class="checks">
        <li>{ic('check')}Bezorgd en aangesloten</li>
        <li>{ic('check')}Of zelf ophalen met trekhaak</li>
        <li>{ic('check')}Verwarmd, ook in de winter</li>
      </ul>
    </div>
    <div class="hero__media">
      <div class="hero__photo">{picture('badkamer-oprit', 'De mobiele badkamer op wielen, klaar om bij je thuis neergezet te worden', '(max-width: 860px) 100vw, 46vw', eager=True, root='{root}')}</div>
      <p class="price-tag" aria-label="Prijs: 137 euro 50 per week, exclusief btw">
        <span class="price-tag__label">Huurprijs</span>
        <span class="price-tag__amount">€137,50</span>
        <span class="price-tag__note">per week, excl. btw</span>
      </p>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="choose-title">
  <div class="wrap">
    <div class="section-head">
      <h2 id="choose-title">Buiten een hele badkamer, of binnen alleen een douche?</h2>
      <p class="lead">We verhuren twee oplossingen. Het verschil zit vooral in hoeveel ruimte je hebt en of je ook een toilet nodig hebt.</p>
    </div>
    <div class="chooser reveal-stagger">
      <article class="option">
        <div class="option__media">{picture('badkamer-kraan', 'Een mobiele badkamer met het Mobiele Badkamer-logo wordt geplaatst', '(max-width: 860px) 92vw, 44rem', root='{root}')}</div>
        <div class="option__body">
          <p class="option__where">Voor buiten: op je oprit of erf</p>
          <h3><a href="{{root}}onze-badkamers/index.html">Mobiele badkamer</a></h3>
          <ul class="facts">
            <li>{ic('check')}<span>Douche, toilet en wastafel met spiegel</span></li>
            <li>{ic('check')}<span>Verwarmd, met licht en stopcontact</span></li>
            <li>{ic('check')}<span>Wij plaatsen en sluiten aan, of je haalt hem zelf op</span></li>
            <li>{ic('check')}<span>Ruimte nodig: ongeveer 4,6 × 2 meter</span></li>
          </ul>
          <div class="option__foot">
            <span class="option__price num">€137,50 <small>/ week, excl. btw · min. 2 weken</small></span>
            <span class="option__more" aria-hidden="true">Bekijk de badkamer →</span>
          </div>
        </div>
      </article>
      <article class="option option--alt">
        <div class="option__media">{picture('cabine-vierkant', 'De mobiele douchecabine wordt op wieltjes naar binnen gereden', '(max-width: 860px) 92vw, 32rem', root='{root}')}</div>
        <div class="option__body">
          <p class="option__where">Voor binnen: past door elke deur</p>
          <h3><a href="{{root}}mobiele-douchecabines/index.html">Mobiele douchecabine</a></h3>
          <ul class="facts">
            <li>{ic('check')}<span>Warme douche met eigen boiler</span></li>
            <li>{ic('check')}<span>78 cm breed, 200 cm hoog</span></li>
            <li>{ic('check')}<span>Alleen stopcontact en koudwaterkraan nodig</span></li>
            <li class="no">{ic('minus')}<span>Geen toilet of wastafel</span></li>
          </ul>
          <div class="option__foot">
            <span class="option__price num">€129 <small>eerste week, daarna €99 · incl. btw</small></span>
            <span class="option__more" aria-hidden="true">Bekijk de cabine →</span>
          </div>
        </div>
      </article>
    </div>
  </div>
</section>

<section class="section section--tight tiles" aria-labelledby="peek-title">
  <div class="wrap">
    <div class="section-head section-head--split">
      <div>
        <h2 id="peek-title">Zo ziet het er vanbinnen uit</h2>
        <p class="lead" style="margin-top:1rem">Echte foto's van onze units. Altijd schoon en hygiënisch afgeleverd.</p>
      </div>
      <a class="link-arrow" href="{{root}}onze-badkamers/index.html#binnenkant">Alles wat erin zit</a>
    </div>
    <div class="peek reveal-stagger">
      <figure>{picture('interieur-toilet-wastafel', 'Toilet en wastafel met spiegel', '(max-width: 860px) 72vw, 22rem', root='{root}')}<figcaption>Toilet &amp; wastafel</figcaption></figure>
      <figure>{picture('interieur-douche', 'Douchehoek met douchekop en zeephouder', '(max-width: 860px) 72vw, 17rem', root='{root}')}<figcaption>Douche</figcaption></figure>
      <figure>{picture('interieur-wastafel', 'Wastafel met spiegel, plankje en handdoek', '(max-width: 860px) 72vw, 17rem', root='{root}')}<figcaption>Spiegel &amp; stopcontact</figcaption></figure>
      <figure>{picture('interieur-deur', 'Kledinghaak en douchegordijn bij de deur', '(max-width: 860px) 72vw, 17rem', root='{root}')}<figcaption>Kledinghaak</figcaption></figure>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="how-title">
  <div class="wrap how">
    <div>
      <h2 id="how-title" style="font-size:var(--step-3)">Zo regelen we het</h2>
      <ol class="steps">
        <li><div><h3>Je vraagt je periode aan</h3><p>Via het formulier of telefonisch. Vertel ons hoeveel weken je verwacht te verbouwen.</p></div></li>
        <li><div><h3>Wij plaatsen en sluiten aan</h3><p>We zetten de badkamer op de juiste plek en sluiten water en stroom aan. Douchen met koud water hoeft niet.</p></div></li>
        <li><div><h3>Klaar? Wij halen hem op</h3><p>Is je nieuwe badkamer af, dan nemen we de unit weer mee. Uitlopen? Laat het ons weten.</p></div></li>
      </ol>
      <p class="footnote"><strong>Liever zelf ophalen?</strong> Dat kan. De badkamer mag achter iedere auto met een trekhaak.</p>
    </div>
    <div class="how__media">{picture('badkamer-straat', 'Mobiele badkamer met dissel, geparkeerd voor een woning', '(max-width: 860px) 92vw, 36rem', root='{root}')}</div>
  </div>
</section>

<section class="section tiles" aria-labelledby="faq-title">
  <div class="wrap faq-layout">
    <div class="section-head">
      <h2 id="faq-title">Wat mensen ons vaak vragen</h2>
      <p class="muted">Staat je vraag er niet bij? Bel <a href="tel:{PHONE_T}" class="num">{PHONE_D}</a>, dan denken we mee.</p>
      <a class="link-arrow" href="{{root}}veelgestelde-vragen/index.html">Alle vragen en prijzen</a>
    </div>
    {faq_html(FAQ_BADKAMER[:3] + FAQ_GENERAL[:1] + FAQ_CABINE[1:2], open_first=True)}
  </div>
</section>

<section class="section" aria-labelledby="about-title">
  <div class="wrap about">
    <div class="about__media">{picture('nonstop-jas', 'Medewerker in een jas met de logo’s van Mobiele Badkamer en Nonstop Rioolreiniging', '(max-width: 860px) 92vw, 32rem', root='{root}')}</div>
    <div>
      <h2 id="about-title">Een vakbedrijf dat weet hoe water stroomt</h2>
      <div class="prose">
        <p>Mobiele Badkamer is onderdeel van Nonstop Rioolreiniging. We zijn geen verbouwingsbedrijf, maar we zorgen er wel voor dat jij tijdens de verbouwing gewoon thuis kunt douchen.</p>
        <p>Bel of mail ons, spreek af hoeveel weken je de badkamer nodig hebt, en wij regelen de rest.</p>
      </div>
      <div class="btn-row">
        <a class="btn" href="{REVIEWS}">{ic('star')}Lees reviews op Google</a>
        <a class="btn" href="{NONSTOP}">Over Nonstop</a>
      </div>
    </div>
  </div>
</section>
{band()}
"""
write("", page("", "Mobiele badkamer huren tijdens je verbouwing | Mobiele Badkamer",
  "Tijdelijke badkamer op je oprit met douche, toilet, wastafel en verwarming. €137,50 per week excl. btw. Wij bezorgen, sluiten aan en halen op.",
  home, schema=[LOCAL_BUSINESS, faq_schema(FAQ_BADKAMER[:3] + FAQ_GENERAL[:1] + FAQ_CABINE[1:2])]))

# ======================================================================= ONZE BADKAMERS
def big(n):
    return max(x for x in (480, 960, 1600) if os.path.exists(f"{OUT}/assets/img/{n}-{x}.webp"))
GALLERY = [
 ("badkamer-oprit", "De mobiele badkamer bij een bosrand, met bedrijfsbus"),
 ("interieur-toilet", "Toiletruimte met raam"),
 ("badkamer-kraan", "Plaatsing met een kraan"),
 ("interieur-toilet-wastafel", "Toilet, wastafel, spiegel en kachel"),
 ("interieur-douchebak", "Douchebak naast het toilet"),
 ("badkamer-straat", "Geparkeerd aan de straat"),
 ("interieur-wastafel", "Wastafel met spiegel en plankje"),
 ("interieur-douche", "Douchehoek"),
 ("interieur-deur", "Deur met kledinghaak"),
 ("interieur-boiler", "Boiler van 2500 watt"),
 ("interieur-groepenkast", "Groepenkast van de unit"),
]
gallery = "\n".join(
  f'<button type="button" data-lightbox="{{root}}assets/img/{n}-{big(n)}.webp">{picture(n, a, "(max-width: 700px) 92vw, 24rem", root="{root}")}</button>'
  for n, a in GALLERY)

DIMS_SVG = """<svg viewBox="0 0 640 330" role="img" aria-labelledby="dims-t dims-d">
<title id="dims-t">Afmetingen mobiele badkamer, bovenaanzicht</title>
<desc id="dims-d">De unit is 305 centimeter lang en 199 centimeter breed. Met de dissel van 150 centimeter is de totale lengte ongeveer 455 centimeter.</desc>
<defs><pattern id="tg" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="oklch(0.90 0.018 250)" stroke-width="1"/></pattern>
<marker id="ar" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 10 5 0 10z" fill="oklch(0.42 0.035 256)"/></marker></defs>
<rect x="190" y="70" width="400" height="190" rx="8" fill="url(#tg)" stroke="oklch(0.50 0.15 253)" stroke-width="3"/>
<path d="M190 140 L40 165 L190 190" fill="none" stroke="oklch(0.24 0.055 258)" stroke-width="3" stroke-linejoin="round"/>
<circle cx="40" cy="165" r="7" fill="oklch(0.24 0.055 258)"/>
<rect x="300" y="52" width="70" height="18" rx="4" fill="oklch(0.24 0.055 258)"/><rect x="420" y="52" width="70" height="18" rx="4" fill="oklch(0.24 0.055 258)"/>
<rect x="300" y="260" width="70" height="18" rx="4" fill="oklch(0.24 0.055 258)"/><rect x="420" y="260" width="70" height="18" rx="4" fill="oklch(0.24 0.055 258)"/>
<text x="390" y="172" text-anchor="middle" font-size="22" font-weight="700" fill="oklch(0.40 0.13 256)">Badkamer</text>
<line x1="190" y1="300" x2="590" y2="300" stroke="oklch(0.42 0.035 256)" stroke-width="1.5" marker-start="url(#ar)" marker-end="url(#ar)"/>
<text x="390" y="322" text-anchor="middle" font-size="17" font-weight="700" fill="oklch(0.24 0.055 258)">305 cm</text>
<line x1="40" y1="300" x2="185" y2="300" stroke="oklch(0.42 0.035 256)" stroke-width="1.5" stroke-dasharray="4 4" marker-start="url(#ar)" marker-end="url(#ar)"/>
<text x="112" y="322" text-anchor="middle" font-size="17" fill="oklch(0.42 0.035 256)">dissel 150 cm</text>
<line x1="615" y1="70" x2="615" y2="260" stroke="oklch(0.42 0.035 256)" stroke-width="1.5" marker-start="url(#ar)" marker-end="url(#ar)"/>
<text x="628" y="170" font-size="17" font-weight="700" fill="oklch(0.24 0.055 258)" transform="rotate(90 628 165)" text-anchor="middle">199 cm</text>
<line x1="40" y1="24" x2="590" y2="24" stroke="oklch(0.55 0.205 27)" stroke-width="2" marker-start="url(#ar)" marker-end="url(#ar)"/>
<rect x="245" y="10" width="140" height="28" rx="14" fill="oklch(1 0 0)"/>
<text x="315" y="30" text-anchor="middle" font-size="17" font-weight="700" fill="oklch(0.47 0.18 27)">totaal ± 455 cm</text>
</svg>"""

badkamers = f"""
<section class="page-hero tiles">
  <div class="wrap page-hero__grid">
    <div>
      <nav class="crumbs" aria-label="Kruimelpad"><a href="{{root}}index.html">Home</a> / Mobiele badkamer</nav>
      <h1>De mobiele badkamer</h1>
      <p class="lead">Een complete badkamer op wielen voor op je oprit: warme douche, gewoon toilet, wastafel met spiegel en een kachel. Zo weet je precies waar je tijdens de verbouwing doucht.</p>
      <p class="price-line"><strong class="num">€137,50</strong><span>per week, excl. btw (€166,38 incl.) · minimaal 2 weken</span></p>
      <div class="btn-row">
        <a class="btn btn--primary btn--lg" href="{{root}}contact/index.html?product=badkamer">Beschikbaarheid aanvragen</a>
        <a class="btn btn--lg" href="tel:{PHONE_T}">{ic('phone')}Bel ons</a>
      </div>
    </div>
    <div class="page-hero__media">{picture('badkamer-oprit', 'De mobiele badkamer op wielen, met ramen en eigen deur', '(max-width: 860px) 92vw, 34rem', eager=True, root='{root}')}</div>
  </div>
</section>

<section class="section" id="binnenkant" aria-labelledby="inside-title">
  <div class="wrap inside">
    {hotspot_photo()}
    <div>
      <h2 id="inside-title" style="font-size:var(--step-3)">Alles wat je van een badkamer verwacht</h2>
      <p class="lead" style="margin-top:1rem">Elke unit wordt schoon en hygiënisch afgeleverd. De nummers horen bij de foto.</p>
      {amenities_list()}
    </div>
  </div>
</section>

<section class="section section--tight tiles" aria-labelledby="video-title">
  <div class="wrap">
    <div class="section-head"><h2 id="video-title">Loop even mee naar binnen</h2></div>
    <div class="video" data-vimeo="{VIMEO}" data-title="Rondleiding door de mobiele badkamer">
      <button type="button"><span class="play">{ic('play')}</span><span>Video afspelen</span></button>
      {picture('badkamer-oprit', '', '(max-width: 1200px) 92vw, 76rem', root='{root}')}
      <p class="consent">De video wordt pas geladen als je op afspelen klikt (Vimeo, zonder tracking).</p>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="dims-title">
  <div class="wrap dims">
    <figure class="dims__drawing" style="margin:0">{DIMS_SVG}</figure>
    <div>
      <h2 id="dims-title" style="font-size:var(--step-3)">Past hij op mijn oprit?</h2>
      <p class="lead" style="margin-top:1rem;margin-bottom:1.5rem">Reken op een vlakke plek van ongeveer 4,6 bij 2 meter, dicht bij een wateraansluiting en stroom.</p>
      <table class="spec">
        <caption class="visually-hidden">Technische specificaties mobiele badkamer</caption>
        <tbody>
          <tr><th scope="row">Lengte (zonder dissel)</th><td>305 cm</td></tr>
          <tr><th scope="row">Lengte dissel</th><td>150 cm</td></tr>
          <tr><th scope="row">Breedte</th><td>199 cm</td></tr>
          <tr><th scope="row">Hoogte (vanaf de grond)</th><td>280 cm</td></tr>
          <tr><th scope="row">Gewicht</th><td>1300 kg</td></tr>
          <tr><th scope="row">Boiler</th><td>2500 watt</td></tr>
          <tr><th scope="row">Vervoer</th><td>Achter elke auto met trekhaak</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="section section--tight" aria-labelledby="gallery-title">
  <div class="wrap">
    <div class="section-head"><h2 id="gallery-title">Meer foto's</h2><p class="muted">Klik op een foto om hem groot te bekijken.</p></div>
    <div class="gallery">{gallery}</div>
  </div>
</section>
<dialog class="lightbox" id="lightbox" aria-label="Foto vergroot">
  <figure style="margin:0"><img alt="" width="1600" height="1067"><figcaption></figcaption></figure>
  <div class="lightbox__nav"><button class="icon-btn" type="button" data-prev aria-label="Vorige foto">{ic('left')}</button><button class="icon-btn" type="button" data-next aria-label="Volgende foto">{ic('right')}</button></div>
  <div class="lightbox__bar"><button class="icon-btn" type="button" data-close aria-label="Sluiten" autofocus>{ic('close')}</button></div>
</dialog>

<section class="section tiles" aria-labelledby="bfaq-title">
  <div class="wrap faq-layout">
    <div class="section-head">
      <h2 id="bfaq-title">Vragen over de badkamer</h2>
      <p class="muted">Alleen een douche nodig, binnen? Kijk dan naar de <a href="{{root}}mobiele-douchecabines/index.html">mobiele douchecabine</a>.</p>
    </div>
    {faq_html(FAQ_BADKAMER, open_first=True)}
  </div>
</section>
{band()}
"""
write("onze-badkamers", page("onze-badkamers", "De mobiele badkamer: douche, toilet en wastafel op wielen | Mobiele Badkamer",
  "Bekijk onze tijdelijke badkamer: warme douche, toilet, wastafel met spiegel, kachel en stopcontact. 305 × 199 cm. €137,50 per week excl. btw.",
  badkamers, schema=[faq_schema(FAQ_BADKAMER)]))

# ======================================================================= DOUCHECABINES
cabine = f"""
<section class="page-hero tiles">
  <div class="wrap page-hero__grid">
    <div>
      <nav class="crumbs" aria-label="Kruimelpad"><a href="{{root}}index.html">Home</a> / Mobiele douchecabine</nav>
      <h1>Geen plek buiten? Zet de douche binnen neer.</h1>
      <p class="lead">De mobiele douchecabine past door elke deur en heeft een eigen boiler. Je hebt alleen een stopcontact en een koudwaterkraan nodig.</p>
      <p class="price-line"><strong class="num">€129</strong><span>eerste week, daarna €99 per week · incl. btw</span></p>
      <div class="btn-row">
        <a class="btn btn--primary btn--lg" href="{{root}}contact/index.html?product=douchecabine">Beschikbaarheid aanvragen</a>
        <a class="btn btn--lg" href="tel:{PHONE_T}">{ic('phone')}Bel ons</a>
      </div>
    </div>
    <div class="page-hero__media">{picture('cabine-open', 'De douchecabine van binnen: thermostaatkraan en douchekop', '(max-width: 860px) 92vw, 30rem', eager=True, root='{root}')}</div>
  </div>
</section>

<section class="section" aria-labelledby="cab-feat">
  <div class="wrap">
    <div class="section-head"><h2 id="cab-feat">Klein, maar een echte warme douche</h2></div>
    <div class="feature-rows reveal-stagger">
      <div class="feature-row"><p class="big num">78 <small>cm breed</small></p><div><h3>Past door elke deurpost</h3><p>Dankzij het compacte ontwerp en de wieltjes rijd je hem zonder gedoe naar de plek waar je hem wilt hebben.</p></div></div>
      <div class="feature-row"><p class="big num">200 <small>cm hoog</small></p><div><h3>Past onder elk plafond</h3><p>Zet hem in de bijkeuken, de garage of een slaapkamer op de begane grond.</p></div></div>
      <div class="feature-row"><p class="big">1 <small>stopcontact</small></p><div><h3>Eigen boiler, dus direct warm water</h3><p>Sluit hem aan op een stopcontact en een koudwaterkraan. De ingebouwde elektrische boiler doet de rest, je hoeft niet te klooien met de watertemperatuur.</p></div></div>
      <div class="feature-row"><p class="big">0 <small>gedoe met afvoer</small></p><div><h3>Ingebouwd pompje</h3><p>Het douchewater wordt weggepompt via de meegeleverde afvoerslang. Er blijft niets in de cabine staan.</p></div></div>
    </div>
  </div>
</section>

<section class="section section--tight tiles" aria-labelledby="cab-move">
  <div class="wrap">
    <div class="section-head section-head--split">
      <div><h2 id="cab-move">Zelf ophalen en plaatsen? Dat lukt prima.</h2>
      <p class="lead" style="margin-top:1rem">Je krijgt de aan- en afvoerslang mee. Liever dat wij hem neerzetten? Dat kan ook.</p></div>
    </div>
    <div class="sequence">
      <figure>{picture('cabine-transport-1', 'De douchecabine wordt op een steekwagen over de stoep gereden', '(max-width: 720px) 92vw, 24rem', root='{root}')}<figcaption>Op de steekwagen naar de voordeur</figcaption></figure>
      <figure>{picture('cabine-transport-3', 'De douchecabine wordt langs de gevel gereden', '(max-width: 720px) 92vw, 24rem', root='{root}')}<figcaption>Licht genoeg voor één persoon</figcaption></figure>
      <figure>{picture('cabine-transport-2', 'De douchecabine wordt door een deuropening gekanteld', '(max-width: 720px) 92vw, 24rem', root='{root}')}<figcaption>Kantelen en door de deur</figcaption></figure>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="cab-why">
  <div class="wrap">
    <div class="section-head"><h2 id="cab-why">Wanneer kies je voor de douchecabine?</h2></div>
    <ul class="uses">
      <li><h3>Je badkamer wordt verbouwd</h3><p>En er is geen ruimte op de oprit, of je hebt geen extra toilet nodig.</p></li>
      <li><h3>Er is een lekkage</h3><p>De aannemer kan pas over een paar weken. Tot die tijd kun je gewoon douchen.</p></li>
      <li><h3>Je bent tijdelijk minder mobiel</h3><p>Na een operatie of blessure even niet de trap op? Zet de douche op de begane grond.</p></li>
    </ul>
    <p class="footnote" style="margin-top:2.5rem;max-width:44rem"><strong>Toch ook een toilet en wastafel nodig?</strong> Bekijk dan de <a href="{{root}}onze-badkamers/index.html">mobiele badkamer</a> voor buiten.</p>
  </div>
</section>

<section class="section tiles" aria-labelledby="cfaq-title">
  <div class="wrap faq-layout">
    <div class="section-head"><h2 id="cfaq-title">Vragen over de douchecabine</h2></div>
    {faq_html(FAQ_CABINE, open_first=True)}
  </div>
</section>
{band()}
"""
write("mobiele-douchecabines", page("mobiele-douchecabines", "Mobiele douchecabine huren voor binnen | Mobiele Badkamer",
  "Tijdelijke douche voor binnen: 78 cm breed, eigen boiler, alleen stopcontact en kraan nodig. €129 eerste week, daarna €99 per week incl. btw.",
  cabine, schema=[faq_schema(FAQ_CABINE)], og_img="cabine-tuin-og.jpg"))

# ======================================================================= FAQ
faq_all = FAQ_GENERAL + FAQ_BADKAMER + FAQ_CABINE
faqpage = f"""
<section class="page-hero tiles">
  <div class="wrap">
    <nav class="crumbs" aria-label="Kruimelpad"><a href="{{root}}index.html">Home</a> / Vragen &amp; prijzen</nav>
    <h1>Vragen en prijzen</h1>
    <p class="lead">Alles over huren, kosten, aansluiten en afmetingen. Staat je vraag er niet bij? Bel <a href="tel:{PHONE_T}" class="num">{PHONE_D}</a>.</p>
  </div>
</section>

<section class="section section--tight" aria-labelledby="prices-title">
  <div class="wrap">
    <h2 id="prices-title" class="visually-hidden">Prijzen</h2>
    <div class="table-scroll">
    <table class="compare" style="font-size:1rem">
      <caption>Prijzen in één oogopslag</caption>
      <thead><tr><th scope="col"></th><th scope="col">Mobiele badkamer</th><th scope="col">Mobiele douchecabine</th></tr></thead>
      <tbody>
        <tr><th scope="row">Prijs</th><td class="num">€137,50 per week<br><span class="muted">excl. btw (€166,38 incl.)</span></td><td class="num">€129 eerste week<br>€99 per volgende week<br><span class="muted">incl. btw</span></td></tr>
        <tr><th scope="row">Minimale huur</th><td>14 dagen</td><td>1 week</td></tr>
        <tr><th scope="row">Waar</th><td>Buiten, op oprit of erf</td><td>Binnen</td></tr>
        <tr><th scope="row">Voorzieningen</th><td>Douche, toilet, wastafel, kachel, licht, stopcontact</td><td>Douche met boiler en afvoerpomp</td></tr>
        <tr><th scope="row">Afmetingen</th><td class="num">305 × 199 × 280 cm (+ dissel 150 cm)</td><td class="num">78 cm breed, 200 cm hoog</td></tr>
        <tr><th scope="row">Vervoer</th><td>Wij bezorgen, of zelf met trekhaak</td><td>Wij plaatsen, of zelf in een ruime auto of aanhanger</td></tr>
      </tbody>
    </table>
    </div>
  </div>
</section>

<section class="section section--tight" aria-labelledby="f1">
  <div class="wrap faq-layout">
    <div class="section-head"><h2 id="f1">Huren in het algemeen</h2></div>
    {faq_html(FAQ_GENERAL)}
  </div>
</section>
<section class="section section--tight tiles" aria-labelledby="f2" id="badkamer">
  <div class="wrap faq-layout">
    <div class="section-head"><h2 id="f2">Mobiele badkamer</h2><a class="link-arrow" href="{{root}}onze-badkamers/index.html">Bekijk de badkamer</a></div>
    {faq_html(FAQ_BADKAMER)}
  </div>
</section>
<section class="section section--tight" aria-labelledby="f3" id="douchecabine">
  <div class="wrap faq-layout">
    <div class="section-head"><h2 id="f3">Mobiele douchecabine</h2><a class="link-arrow" href="{{root}}mobiele-douchecabines/index.html">Bekijk de douchecabine</a></div>
    {faq_html(FAQ_CABINE)}
  </div>
</section>
{band()}
"""
write("veelgestelde-vragen", page("veelgestelde-vragen", "Veelgestelde vragen en prijzen | Mobiele Badkamer",
  "Wat kost een mobiele badkamer of douchecabine huren, wat zit erin en hoe wordt hij geplaatst? Alle antwoorden en prijzen op één pagina.",
  faqpage, schema=[faq_schema(faq_all)]))

# ======================================================================= CONTACT
contact = f"""
<section class="page-hero tiles" style="padding-bottom:clamp(1.5rem,3vw,2.5rem)">
  <div class="wrap">
    <nav class="crumbs" aria-label="Kruimelpad"><a href="{{root}}index.html">Home</a> / Contact</nav>
    <h1>Beschikbaarheid aanvragen</h1>
    <p class="lead">Vul je periode in en we laten je weten of er een unit vrij is. Je zit nergens aan vast.</p>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap contact-layout">
    <div class="panel">
      <form id="aanvraag" action="mailto:{MAIL}" method="post" enctype="text/plain">
        <div class="form-grid">
          <fieldset class="field full">
            <legend>Wat wil je huren?</legend>
            <div class="choice">
              <label><input type="radio" name="product" value="badkamer" checked><span class="t">Mobiele badkamer</span><span class="d">Buiten · douche, toilet, wastafel · €137,50/week excl. btw</span></label>
              <label><input type="radio" name="product" value="douchecabine"><span class="t">Mobiele douchecabine</span><span class="d">Binnen · alleen douche · €129 eerste week incl. btw</span></label>
            </div>
          </fieldset>

          <div class="field">
            <label for="vanaf">Vanaf</label>
            <input id="vanaf" name="vanaf" type="date" required data-required="Kies de eerste dag dat je de badkamer nodig hebt.">
            <p class="error" role="alert">{ic('alert')}<span></span></p>
          </div>
          <div class="field">
            <label for="tot">Tot en met</label>
            <input id="tot" name="tot" type="date" required data-required="Kies tot wanneer je hem ongeveer nodig hebt." aria-describedby="min-note">
            <p class="hint" id="min-note" data-min-note>Minimale huurperiode is 14 dagen.</p>
            <p class="error" role="alert">{ic('alert')}<span></span></p>
          </div>

          <div class="estimate full" id="estimate" aria-live="polite">
            <span class="estimate__label">Indicatie huurprijs</span>
            <span class="estimate__amount num">—</span>
            <span class="estimate__detail">Kies je periode, dan rekenen we het voor je uit.</span>
          </div>

          <div class="field">
            <label for="voornaam">Voornaam</label>
            <input id="voornaam" name="voornaam" autocomplete="given-name" required data-required="Vul je voornaam in.">
            <p class="error" role="alert">{ic('alert')}<span></span></p>
          </div>
          <div class="field">
            <label for="achternaam">Achternaam</label>
            <input id="achternaam" name="achternaam" autocomplete="family-name" required data-required="Vul je achternaam in.">
            <p class="error" role="alert">{ic('alert')}<span></span></p>
          </div>
          <div class="field">
            <label for="email">E-mailadres</label>
            <input id="email" name="email" type="email" autocomplete="email" inputmode="email" required data-required="Vul je e-mailadres in, dan sturen we je de bevestiging.">
            <p class="error" role="alert">{ic('alert')}<span></span></p>
          </div>
          <div class="field">
            <label for="telefoon">Telefoonnummer</label>
            <input id="telefoon" name="telefoon" type="tel" autocomplete="tel" inputmode="tel" required pattern="[0-9\\s+\\-\\(\\)]{{8,}}" data-required="Vul je telefoonnummer in, zodat we je kunnen bellen over de plaatsing." data-pattern="Gebruik alleen cijfers, spaties of een +, bijvoorbeeld 06 12345678.">
            <p class="error" role="alert">{ic('alert')}<span></span></p>
          </div>
          <div class="field">
            <label for="plaats">Plaats of postcode <span class="opt">(optioneel)</span></label>
            <input id="plaats" name="plaats" autocomplete="postal-code">
            <p class="hint">Zo kunnen we de bezorging inschatten.</p>
          </div>
          <div class="field">
            <label for="levering">Bezorging</label>
            <select id="levering" name="levering">
              <option value="bezorgen">Graag bezorgen en aansluiten</option>
              <option value="zelf">Ik haal zelf op (trekhaak / auto)</option>
            </select>
          </div>
          <div class="field full">
            <label for="opmerkingen">Vragen of opmerkingen <span class="opt">(optioneel)</span></label>
            <textarea id="opmerkingen" name="opmerkingen" placeholder="Bijvoorbeeld: waar de badkamer kan staan, of iets over de wateraansluiting."></textarea>
          </div>
          <div class="hp" aria-hidden="true"><label for="website">Website</label><input id="website" name="website" tabindex="-1" autocomplete="off"></div>
          <div class="full" style="display:flex;flex-wrap:wrap;align-items:center;gap:1rem">
            <button class="btn btn--primary btn--lg" type="submit">Aanvraag versturen</button>
            <p class="hint">We reageren op werkdagen meestal dezelfde dag.</p>
          </div>
          <p class="error is-shown full" id="form-error" tabindex="-1" hidden>{ic('alert')}<span>Versturen lukte niet. Probeer het opnieuw of bel ons op {PHONE_D}.</span></p>
        </div>
      </form>
      <div class="form-status form-status--ok" id="form-done" tabindex="-1" role="status">
        <h3>Bedankt, je aanvraag staat klaar</h3>
        <p>We nemen zo snel mogelijk contact met je op over de beschikbaarheid.</p>
        <p data-mail-note hidden style="margin-top:.75rem">Je e-mailprogramma is geopend met je aanvraag erin. Vergeet niet op <strong>verzenden</strong> te drukken. Werkt dat niet? Bel ons op <a href="tel:{PHONE_T}">{PHONE_D}</a>.</p>
      </div>
    </div>

    <aside class="contact-aside" aria-labelledby="direct-title">
      <div>
        <h2 id="direct-title">Liever direct contact?</h2>
        <p class="muted" style="margin-top:.4rem">Bel ons, dan hebben we het in een paar minuten geregeld.</p>
        <p style="margin-top:1rem"><a class="phone-big" href="tel:{PHONE_T}">{PHONE_D}</a></p>
      </div>
      <ul class="contact-list">
        <li><span class="ic">{ic('mail')}</span><div><div class="k">E-mail</div><a class="v" href="mailto:{MAIL}">{MAIL}</a></div></li>
        <li><span class="ic">{ic('clock')}</span><div><div class="k">Bereikbaar</div><div class="v">Ma t/m vr, <span class="num">08:00–17:00</span></div></div></li>
        <li><span class="ic">{ic('pin')}</span><div><div class="k">Adres</div><address class="v" style="font-style:normal">Lytse Mar 4<br>8523 NN Idskenhuizen</address></div></li>
      </ul>
      <p class="footnote">Mobiele Badkamer is onderdeel van <a href="{NONSTOP}">Nonstop Rioolreiniging</a>. <a href="{REVIEWS}">Bekijk onze reviews op Google</a>.</p>
    </aside>
  </div>
</section>
"""
write("contact", page("contact", "Beschikbaarheid aanvragen | Mobiele Badkamer",
  "Vraag een mobiele badkamer of douchecabine aan voor jouw periode, of bel 06 54 25 47 40. Bereikbaar op werkdagen van 08:00 tot 17:00.",
  contact, schema=[LOCAL_BUSINESS], body_class="is-contact"))

# ======================================================================= ARTICLE
article = f"""
<section class="page-hero tiles">
  <div class="wrap">
    <nav class="crumbs" aria-label="Kruimelpad"><a href="{{root}}index.html">Home</a> / Douchen tijdens de verbouwing</nav>
    <h1 style="max-width:18ch">Waar douche je tijdens de verbouwing van je badkamer?</h1>
    <p class="lead">De plannen zijn rond, de aannemer is geboekt. Alleen die ene vraag blijft: waar ga je de komende weken douchen?</p>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap article-layout">
    <article class="prose">
      <p>Een badkamerverbouwing duurt al snel een paar weken. In die tijd heb je geen douche, vaak geen wastafel en soms ook geen toilet. Dit zijn de opties, met hun voor- en nadelen.</p>

      <div class="table-scroll">
      <table class="compare">
        <caption>De opties naast elkaar</caption>
        <thead><tr><th scope="col">Optie</th><th scope="col">Prima als…</th><th scope="col">Nadeel</th></tr></thead>
        <tbody>
          <tr><th scope="row">Bij de buren of familie</th><td>Het om een paar dagen gaat</td><td>Je bent afhankelijk van andermans agenda en voelt je al snel bezwaard</td></tr>
          <tr><th scope="row">Mobiele douchecabine</th><td>Je binnen ruimte hebt en alleen een douche mist</td><td>Geen toilet of wastafel</td></tr>
          <tr><th scope="row">Mobiele badkamer</th><td>Je een oprit of erf hebt en alles in één wilt</td><td>Je hebt ongeveer 4,6 × 2 meter ruimte nodig</td></tr>
        </tbody>
      </table>
      </div>

      <h2>Douchen bij de buren: kan, maar niet weken achter elkaar</h2>
      <p>Ook als je goed met de buren kunt opschieten, zit je er niet op te wachten om elke ochtend met je handdoek aan te bellen. Je moet rekening houden met hun planning en het voelt al snel als een gunst.</p>

      <h2>Een eigen badkamer op je oprit</h2>
      <p>Met een mobiele badkamer heb je alles gewoon bij huis: een warme douche met douchegordijn, een gewoon toilet, een wastafel met spiegel en stopcontact, een kachel en kledinghaakjes. Handig als je huis maar één toilet heeft, of als je de badkamer en het tweede toilet tegelijk aanpakt.</p>
      <figure class="article-figure">{picture('interieur-toilet-wastafel', 'Binnen in de mobiele badkamer: toilet en wastafel met spiegel', '(max-width: 960px) 92vw, 42rem', root='{root}')}<figcaption>Toilet, wastafel, spiegel en kachel in één unit.</figcaption></figure>
      <p>Wij zetten de badkamer op de juiste plek, sluiten water en stroom aan en halen hem op zodra je nieuwe badkamer klaar is. Wil je hem liever zelf ophalen en terugbrengen? Dat kan met iedere auto met een trekhaak.</p>
      <p><a class="link-arrow" href="{{root}}onze-badkamers/index.html">Bekijk de mobiele badkamer</a></p>

      <h2>Geen ruimte buiten? Een douchecabine voor binnen</h2>
      <p>De mobiele douchecabine is 78 cm breed en past door elke deur. Je hebt alleen een stopcontact en een koudwaterkraan nodig; de boiler en afvoerpomp zitten erin.</p>
      <p><a class="link-arrow" href="{{root}}mobiele-douchecabines/index.html">Bekijk de douchecabine</a></p>

      <h2>Wat kost het?</h2>
      <p>De mobiele badkamer kost <strong>€137,50 per week excl. btw</strong>, met een minimale huur van 14 dagen. De douchecabine kost <strong>€129 voor de eerste week en €99 per volgende week, incl. btw</strong>. Alle details staan op de pagina <a href="{{root}}veelgestelde-vragen/index.html">vragen en prijzen</a>.</p>
    </article>
    <aside class="article-aside">
      <div class="panel">
        <h2>Plan je verbouwing?</h2>
        <p>Vraag nu je periode aan. Zo weet je zeker dat er een badkamer klaarstaat.</p>
        <a class="btn btn--primary" href="{{root}}contact/index.html">Beschikbaarheid aanvragen</a>
        <a class="btn" href="tel:{PHONE_T}" style="margin-top:.5rem">{ic('phone')}<span class="num">{PHONE_D}</span></a>
      </div>
    </aside>
  </div>
</section>
{band()}
"""
art_schema = {"@context": "https://schema.org", "@type": "Article", "headline": "Waar douche je tijdens de verbouwing van je badkamer?", "inLanguage": "nl", "publisher": {"@type": "Organization", "name": "Mobiele Badkamer"}, "image": SITE + "/assets/img/badkamer-oprit-og.jpg"}
write("douchen-tijdens-verbouwing-badkamer", page("douchen-tijdens-verbouwing-badkamer", "Douchen tijdens de verbouwing van je badkamer: je opties | Mobiele Badkamer",
  "Waar douche je als je badkamer wordt verbouwd? Buren, een douchecabine of een tijdelijke badkamer op je oprit: de opties en kosten op een rij.",
  article, schema=[art_schema]))

# ======================================================================= extras
urls = ["", "onze-badkamers/", "mobiele-douchecabines/", "veelgestelde-vragen/", "contact/", "douchen-tijdens-verbouwing-badkamer/"]
open(f"{OUT}/sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{SITE}/{u}</loc><lastmod>2026-11-01</lastmod></url>\n" for u in urls) + "</urlset>\n")
open(f"{OUT}/robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
print("built")
