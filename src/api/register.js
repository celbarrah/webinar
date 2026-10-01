// POST /api/register - inscription Masterclass 13 octobre -> contact ClientX (API LeadConnector v2)
// Env : CLIENTX_TOKEN (jeton d'integration privee du sous-compte ClientX.ma, locationId sMBdtpAowNv22pz2kxma), CLIENTX_LOCATION_ID,
//       CLIENTX_TAG (defaut webinar-13oct), CLIENTX_FIELDS (optionnel, JSON {"utm_source":"<id>",...,"job_title":"<id>"})
const API = 'https://services.leadconnectorhq.com';
const UTM_KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
let fieldCache = null;

const clip = (v, n = 150) => String(v ?? '').trim().slice(0, n);

async function api(path, init = {}) {
  const r = await fetch(API + path, {
    ...init,
    headers: {
      Authorization: `Bearer ${process.env.CLIENTX_TOKEN}`,
      Version: '2021-07-28',
      Accept: 'application/json',
      'Content-Type': 'application/json',
      'User-Agent': 'Mozilla/5.0 (compatible; ClientX-Masterclass-LP/1.0)',
    },
  });
  const text = await r.text();
  let body;
  try { body = JSON.parse(text); } catch { body = { raw: text.slice(0, 300) }; }
  if (!r.ok) {
    const err = new Error(`ClientX ${r.status} ${path}`);
    err.body = body;
    throw err;
  }
  return body;
}

// IDs des champs personnalises (UTM + Fonction), resolus une fois par instance
async function fieldIds(locationId) {
  if (fieldCache) return fieldCache;
  if (process.env.CLIENTX_FIELDS) return (fieldCache = JSON.parse(process.env.CLIENTX_FIELDS));
  const { customFields = [] } = await api(`/locations/${locationId}/customFields?model=contact`);
  const ids = {};
  for (const f of customFields) {
    const key = String(f.fieldKey || '').replace(/^contact\./, '').toLowerCase();
    const name = String(f.name || '').trim().toLowerCase();
    for (const k of UTM_KEYS) if (key === k || name === k) ids[k] ||= f.id;
    if (key === 'fonction' || name === 'fonction') ids.job_title ||= f.id;
  }
  return (fieldCache = ids);
}

// Numero -> E.164, Maroc par defaut (06..., 6..., 212..., 00212..., +212 0...)
export function normPhone(raw) {
  let p = String(raw || '').trim().replace(/[\s.\-()]/g, '');
  if (p.startsWith('00')) p = '+' + p.slice(2);
  if (!p.startsWith('+')) {
    p = p.replace(/\D/g, '');
    if (p.startsWith('212')) p = '+' + p;
    else if (p.startsWith('0')) p = '+212' + p.slice(1);
    else if (/^[5-7]\d{8}$/.test(p)) p = '+212' + p;
    else p = '+' + p;
  }
  p = ('+' + p.slice(1).replace(/\D/g, '')).replace(/^\+2120/, '+212');
  const digits = p.length - 1;
  if (digits < 9 || digits > 15) return null;
  if (p.startsWith('+212') && digits !== 12) return null;
  return p;
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ ok: false });
  }
  let b = req.body || {};
  if (typeof b === 'string') { try { b = JSON.parse(b); } catch { b = {}; } }

  // Anti-robot : champ piege rempli ou envoi trop rapide -> on repond OK sans rien creer
  if (b.website || (Number(b.elapsed) > 0 && Number(b.elapsed) < 1500)) return res.status(200).json({ ok: true });

  const lead = {
    first_name: clip(b.first_name, 80),
    last_name: clip(b.last_name, 80),
    email: clip(b.email, 150).toLowerCase(),
    phone: normPhone(b.phone),
    company: clip(b.company),
    job_title: clip(b.job_title),
  };
  const utm = {};
  for (const k of UTM_KEYS) if (b[k]) utm[k] = clip(b[k], 200);

  if (!EMAIL_RE.test(lead.email)) lead.email = '';
  const missing = Object.keys(lead).filter((k) => !lead[k]);
  if (missing.length) {
    const message = missing.includes('phone') ? 'Vérifiez votre numéro WhatsApp (ex. 06 12 34 56 78 ou +33 6 12 34 56 78).'
      : missing.includes('email') ? 'Vérifiez votre adresse email.' : 'Merci de remplir tous les champs.';
    return res.status(400).json({ ok: false, message, fields: missing });
  }

  const token = process.env.CLIENTX_TOKEN;
  const locationId = process.env.CLIENTX_LOCATION_ID;
  const tag = process.env.CLIENTX_TAG || 'webinar-13oct';
  if (!token || !locationId) {
    console.error('LEAD_NOT_SAVED config manquante', JSON.stringify({ lead, utm }));
    return res.status(503).json({ ok: false, message: "Les inscriptions ouvrent dans quelques instants. Merci de réessayer un peu plus tard." });
  }

  try {
    const ids = await fieldIds(locationId);
    const customFields = [];
    for (const k of UTM_KEYS) if (utm[k] && ids[k]) customFields.push({ id: ids[k], field_value: utm[k] });
    if (ids.job_title) customFields.push({ id: ids.job_title, field_value: lead.job_title });

    const up = await api('/contacts/upsert', {
      method: 'POST',
      body: JSON.stringify({
        locationId,
        firstName: lead.first_name,
        lastName: lead.last_name,
        name: `${lead.first_name} ${lead.last_name}`,
        email: lead.email,
        phone: lead.phone,
        companyName: lead.company,
        source: 'LP Masterclass 13 octobre',
        customFields,
      }),
    });
    const id = up?.contact?.id;
    if (!id) throw Object.assign(new Error('contact id absent'), { body: up });

    // Tag ajoute a part : l'upsert remplace les tags existants, l'endpoint /tags les complete
    await api(`/contacts/${id}/tags`, { method: 'POST', body: JSON.stringify({ tags: [tag] }) });
    console.log('LEAD_OK', id, JSON.stringify(utm));
    return res.status(200).json({ ok: true });
  } catch (e) {
    console.error('LEAD_NOT_SAVED', e.message, JSON.stringify(e.body || {}).slice(0, 500), JSON.stringify({ lead, utm }));
    return res.status(502).json({ ok: false, message: 'Une erreur est survenue. Réessayez dans un instant.' });
  }
}
