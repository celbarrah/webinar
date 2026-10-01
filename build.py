#!/usr/bin/env python3
"""Genere la LP Masterclass ClientX 13 octobre.

    python3 build.py            -> site/ (Vercel, page finale) + dist/ et preview/ (secours ClientX)
    python3 build.py --og       -> regenere aussi site/assets/og.jpg (Playwright + Chrome)

site/     -> index.html, merci.html, api/register.js, assets/ : a deployer avec
             cd site && npx vercel --prod --yes --scope meladraouy-4670s-projects
dist/     -> blocs "Code personnalise" si la page est un jour montee dans ClientX (iframe formulaire)
preview/  -> apercu local de la version ClientX (ancien formulaire, affichage seulement)
"""
import html
import json
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import urlencode, quote

ROOT = Path(__file__).parent
CFG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))

TITLE = "Masterclass ClientX : Recrutez votre équipe d'agents IA"
# Mardi 13 octobre 2026, 11h-12h Africa/Casablanca (UTC+1) = 10h-11h UTC
START_UTC, END_UTC = "20261013T100000Z", "20261013T110000Z"
START_ISO, END_ISO = "2026-10-13T10:00:00Z", "2026-10-13T11:00:00Z"
AGENTS = ("axel", "max", "jade")

IFRAME_BLOCK = ('<div class="fslot" id="cxm-form" data-form-id="{id}" data-form-domain="{dom}" data-form-height="{h}">'
                '<span class="fload">Chargement du formulaire…</span></div>')

NATIVE_FORM = """<form class="rf" id="cxm-reg" novalidate>
            <div class="g2">
              <label>Prénom<input name="first_name" autocomplete="given-name" required maxlength="80"><span class="err" data-err="first_name"></span></label>
              <label>Nom<input name="last_name" autocomplete="family-name" required maxlength="80"><span class="err" data-err="last_name"></span></label>
            </div>
            <label>Email professionnel<input type="email" name="email" autocomplete="email" inputmode="email" required maxlength="150" placeholder="vous@entreprise.ma"><span class="err" data-err="email"></span></label>
            <label>Téléphone WhatsApp<input type="tel" name="phone" autocomplete="tel" inputmode="tel" required maxlength="25" placeholder="06 12 34 56 78"><span class="err" data-err="phone"></span></label>
            <div class="g2">
              <label>Entreprise<input name="company" autocomplete="organization" required maxlength="150"><span class="err" data-err="company"></span></label>
              <label>Fonction<input name="job_title" autocomplete="organization-title" required maxlength="150" placeholder="Gérant, directeur commercial…"><span class="err" data-err="job_title"></span></label>
            </div>
            <div class="hp" aria-hidden="true"><label>Site web<input name="website" tabindex="-1" autocomplete="off"></label></div>
            <p class="ferr" role="alert" hidden></p>
            <button type="submit" class="btn">Je réserve ma place<svg class="ic"><use href="#cx-arrow"/></svg></button>
          </form>"""


def speakers_html(speakers, base=""):
    """base : prefixe des photos en chemin local (assets/speakers/...), ex. '../' pour preview/."""
    if not speakers:
        return ""
    cards = []
    for s in speakers:
        name, role = html.escape(s["name"]), html.escape(s["role"])
        if s.get("photo"):
            src = s["photo"] if s["photo"].startswith(("http://", "https://", "/")) else base + s["photo"]
            av = f'<img class="spk-av" src="{html.escape(src)}" alt="{name}" width="72" height="72" loading="lazy">'
        else:
            initials = "".join(p[0] for p in s["name"].split()[:2]).upper()
            av = f'<span class="spk-av" aria-hidden="true">{initials}</span>'
        cards.append(f'<div class="spk">{av}<div><b>{name}</b><span>{role}</span></div></div>')
    return (
        '<!-- 5.5 INTERVENANTS -->\n  <section class="sec" id="intervenants"><div class="w">'
        '<div class="sec-hd c rv"><p class="eyebrow">Intervenants</p><h2>Vos intervenants</h2></div>'
        f'<div class="spk-g rv">{"".join(cards)}</div></div></section>'
    )


def speakers_hero_html(speakers, base=""):
    """v2 : intervenants en cartes compactes dans le haut de page."""
    if not speakers:
        return ""
    items = []
    for s in speakers:
        name, role = html.escape(s["name"]), html.escape(s["role"])
        if s.get("photo"):
            src = s["photo"] if s["photo"].startswith(("http://", "https://", "/")) else base + s["photo"]
            av = f'<img class="spk-av" src="{html.escape(src)}" alt="{name}" width="54" height="54">'
        else:
            initials = "".join(p[0] for p in s["name"].split()[:2]).upper()
            av = f'<span class="spk-av" aria-hidden="true">{initials}</span>'
        items.append(f'<li class="hspk-i">{av}<div><b>{name}</b><span>{role}</span></div></li>')
    return f'<div class="hspk"><p class="hspk-t">Vos intervenants</p><ul class="hspk-g">{"".join(items)}</ul></div>'


def logos_html():
    base = CFG["logo_base"]
    one = [f'<img src="{base.format(f)}" alt="{html.escape(alt)}" width="96" height="40" loading="lazy">'
           for f, alt in CFG["logos"]]
    dup = [re.sub(r'alt="[^"]*"', 'alt="" aria-hidden="true"', i) for i in one]  # 2e passage pour la boucle
    return "".join(one)  # v2 : grille fixe, plus de 2e passage pour la boucle du defilement


def ics_escape(s):
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def calendar_tokens():
    zoom = CFG.get("zoom_url", "").strip()
    details = "Masterclass gratuite en direct. Le lien Zoom vous a été envoyé par WhatsApp et par email."
    if zoom:
        details += f"\nLien : {zoom}"
    location = zoom or "En ligne sur Zoom (lien envoyé par WhatsApp et email)"
    gcal = "https://calendar.google.com/calendar/render?" + urlencode(
        {"action": "TEMPLATE", "text": TITLE, "dates": f"{START_UTC}/{END_UTC}", "details": details,
         "location": location, "ctz": "Africa/Casablanca"}, quote_via=quote)
    outlook = "https://outlook.office.com/calendar/0/deeplink/compose?" + urlencode(
        {"path": "/calendar/action/compose", "rru": "addevent", "subject": TITLE, "startdt": START_ISO,
         "enddt": END_ISO, "body": details, "location": location}, quote_via=quote)
    return {
        "GCAL_URL": html.escape(gcal),
        "OUTLOOK_URL": html.escape(outlook),
        "JS_ICS_SUMMARY": json.dumps("SUMMARY:" + ics_escape(TITLE), ensure_ascii=False),
        "JS_ICS_DESCRIPTION": json.dumps("DESCRIPTION:" + ics_escape(details), ensure_ascii=False),
        "JS_ICS_LOCATION": json.dumps("LOCATION:" + ics_escape(location), ensure_ascii=False),
    }


def share_tokens():
    """v3 : liens Invitez un associe de la page de confirmation, avec UTM parrainage par canal."""
    base = CFG["site_url"].rstrip("/") + "/"

    def url(medium):
        return base + "?" + urlencode({"utm_source": "parrainage", "utm_medium": medium,
                                       "utm_campaign": "masterclass_13oct"})
    msg = ("Je participe à la Masterclass gratuite de ClientX « Recrutez votre équipe d'agents IA », "
           "mardi 13 octobre à 11h, en ligne. Inscription gratuite : ")
    wa = "https://wa.me/?" + urlencode({"text": msg + url("whatsapp")}, quote_via=quote)
    mail = "mailto:?" + urlencode({"subject": "Masterclass gratuite : Recrutez votre équipe d'agents IA · 13 octobre",
                                   "body": "Bonjour,\n\n" + msg + url("email") + "\n\nBien à vous"}, quote_via=quote)
    return {"SHARE_WA": html.escape(wa), "SHARE_MAIL": html.escape(mail), "SHARE_URL": html.escape(url("lien"))}


def render(src, tokens):
    out = (ROOT / "src" / src).read_text(encoding="utf-8")
    for k, v in tokens.items():
        out = out.replace("{{" + k + "}}", str(v))
    left = sorted(set(re.findall(r"\{\{[A-Z_]+\}\}", out)))
    if left:
        sys.exit(f"Tokens non remplaces dans {src}: {left}")
    return out


def pixel_snippet(pixel):
    return f"""<!-- Pixel Meta ClientX Agents IA ({pixel}) : PageView partout, Lead sur la confirmation -->
<script>
!function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)}};if(!f._fbq)f._fbq=n;
n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,
document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '{pixel}');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id={pixel}&ev=PageView&noscript=1"/></noscript>
"""


def doc(title, body, head_extra=""):
    return f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="theme-color" content="#000000">
{head_extra}<style>html,body{{margin:0;padding:0;background:#000}}</style></head>
<body>
{body}
</body></html>
"""


def site_head(url, index=True):
    desc = ("Mardi 13 octobre à 11h, en ligne sur Zoom. Découvrez en direct comment trois agents IA répondent "
            "à vos prospects, automatisent vos tâches répétitives et gèrent vos avis Google, et repartez avec "
            "votre agent IA. Gratuit, places limitées.")
    og_t = "Masterclass gratuite : Recrutez votre équipe d'agents IA"
    og_d = "Mardi 13 octobre, 11h, en ligne sur Zoom. Axel, Max et Jade en direct. Repartez avec votre agent IA."
    base = CFG["site_url"].rstrip("/")
    tags = [
        f'<meta name="description" content="{html.escape(desc)}">',
        f'<link rel="icon" href="{CFG["favicon"]}">',
        '<meta property="og:type" content="website"><meta property="og:locale" content="fr_FR"><meta property="og:site_name" content="ClientX">',
        f'<meta property="og:title" content="{html.escape(og_t)}">',
        f'<meta property="og:description" content="{html.escape(og_d)}">',
        f'<meta property="og:image" content="{base}/assets/og.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">',
        f'<meta property="og:url" content="{base}{url}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<link rel="canonical" href="{base}{url}">',
    ]
    if not index:
        tags.append('<meta name="robots" content="noindex">')
    return "\n".join(tags) + "\n" + pixel_snippet(CFG["pixel_id"])


def build_og(site):
    """site/assets/og.jpg : capture 1200x630 de src/og.html."""
    from playwright.sync_api import sync_playwright
    tmp = ROOT / "src" / "_og.html"
    tmp.write_text(render("og.html", {"LOGO_FOOTER": CFG["assets"]["logo_footer"],
                                      **{"IMG_" + k.upper(): f"../assets/{k}.jpg" for k in AGENTS}}), encoding="utf-8")
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": 1200, "height": 630})
        pg.goto(tmp.resolve().as_uri(), wait_until="networkidle")
        pg.wait_for_timeout(800)
        pg.screenshot(path=str(site / "assets" / "og.jpg"), type="jpeg", quality=86)
        b.close()
    tmp.unlink()


def build(with_og=False):
    a = CFG["assets"]
    warnings = []
    common = {"LOGO_HEADER": a["logo_header"], "LOGO_FOOTER": a["logo_footer"], **calendar_tokens(), **share_tokens()}
    shared = {"LOGOS": logos_html(), "SPEAKERS": speakers_html(CFG.get("speakers", [])),
              "SPEAKERS_HERO": speakers_hero_html(CFG.get("speakers", [])),
              "CONFIRM_PATH": CFG["confirm_path"]}
    local_imgs = {"IMG_" + k.upper(): f"assets/{k}.jpg" for k in AGENTS}

    # --- site/ : page finale Vercel (formulaire natif -> /api/register -> ClientX)
    site = ROOT / "site"
    (site / "assets").mkdir(parents=True, exist_ok=True)
    (site / "api").mkdir(exist_ok=True)
    for k in AGENTS:
        shutil.copy(ROOT / "assets" / f"{k}.jpg", site / "assets" / f"{k}.jpg")
    shutil.copy(ROOT / "src" / "api" / "register.js", site / "api" / "register.js")
    spk_dir = ROOT / "assets" / "speakers"  # photos des intervenants, servies avec la page
    if spk_dir.is_dir():
        (site / "assets" / "speakers").mkdir(parents=True, exist_ok=True)
        for p in spk_dir.iterdir():
            if p.is_file():
                shutil.copy(p, site / "assets" / "speakers" / p.name)
    (site / "index.html").write_text(doc(
        "Masterclass gratuite : Recrutez votre équipe d'agents IA · ClientX",
        render("inscription.html", {**common, **shared, **local_imgs, "FORM_BLOCK": NATIVE_FORM}),
        site_head("/")), encoding="utf-8")
    (site / "merci.html").write_text(doc(
        "Votre place est réservée · Masterclass ClientX",
        render("confirmation.html", {**common, **{k: "/" + v for k, v in local_imgs.items()}}),
        site_head(CFG["confirm_path"], index=False)), encoding="utf-8")
    (site / "package.json").write_text(json.dumps(
        {"name": CFG["vercel_project"], "private": True, "type": "module", "engines": {"node": ">=20"}}, indent=2) + "\n")
    (site / "vercel.json").write_text(json.dumps({
        "cleanUrls": True,
        "trailingSlash": False,
        "headers": [
            {"source": "/merci", "headers": [{"key": "X-Robots-Tag", "value": "noindex"}]},
            {"source": "/assets/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=604800"}]},
        ],
    }, indent=2) + "\n")
    if with_og or not (site / "assets" / "og.jpg").exists():
        build_og(site)

    # --- dist/ : secours ClientX (iframe formulaire natif ClientX)
    dist_imgs = {}
    for k in AGENTS:
        dist_imgs["IMG_" + k.upper()] = a.get(k) or f"A_REMPLACER_URL_{k.upper()}"
    form_id = CFG.get("form_id") or "A_REMPLACER_ID_FORMULAIRE"
    iframe = lambda fid: IFRAME_BLOCK.format(id=fid, dom=CFG["form_domain"], h=CFG["form_height"])
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    (dist / "00-tracking-head.html").write_text(pixel_snippet(CFG["pixel_id"]), encoding="utf-8")
    (dist / "01-inscription.html").write_text(
        render("inscription.html", {**common, **shared, **dist_imgs, "FORM_BLOCK": iframe(form_id)}), encoding="utf-8")
    (dist / "02-confirmation.html").write_text(render("confirmation.html", {**common, **dist_imgs}), encoding="utf-8")

    prev = ROOT / "preview"
    prev.mkdir(exist_ok=True)
    prev_imgs = {k: "../" + v for k, v in local_imgs.items()}
    (prev / "inscription.html").write_text(doc("Apercu ClientX - inscription", render(
        "inscription.html", {**common, **shared, "SPEAKERS": speakers_html(CFG.get("speakers", []), "../"),
                             "SPEAKERS_HERO": speakers_hero_html(CFG.get("speakers", []), "../"),
                             **prev_imgs, "FORM_BLOCK": iframe(CFG["preview_form_id"])})), encoding="utf-8")
    (prev / "confirmation.html").write_text(doc("Apercu ClientX - confirmation", render(
        "confirmation.html", {**common, **prev_imgs})), encoding="utf-8")

    for f in sorted(p for p in site.rglob("*") if p.is_file() and ".vercel" not in p.parts):
        print(f"  {f.relative_to(ROOT)}  {f.stat().st_size / 1024:.1f} Ko")
    if any(s.get("photo") and not s["photo"].startswith(("http://", "https://")) for s in CFG.get("speakers", [])):
        warnings.append("photos intervenants en chemin local : OK pour site/ (Vercel) ; pour dist/ (ClientX), "
                        "les uploader dans Medias ClientX et mettre leur URL dans config.json > speakers > photo")
    if not CFG.get("zoom_url"):
        warnings.append("zoom_url vide : 'Ajouter a mon agenda' indique 'En ligne sur Zoom' (rebuild + redeploy quand le lien existe)")
    for w in warnings:
        print("  ! " + w)


if __name__ == "__main__":
    build(with_og="--og" in sys.argv)
