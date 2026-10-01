// POST /api/register - inscription Masterclass 13 octobre -> webhook
// Sends form data with UTM parameters to webhook

const UTM_KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const WEBHOOK_URL = 'https://radouane.automatespot.com/webhook-test/d4480c0d-d77d-43af-90a8-c6dfb477f87b';

const clip = (v, n = 150) => String(v ?? '').trim().slice(0, n);

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

  try {
    // Send to webhook
    const payload = {
      firstName: lead.first_name,
      lastName: lead.last_name,
      email: lead.email,
      phone: lead.phone,
      company: lead.company,
      jobTitle: lead.job_title,
      ...utm, // Include all UTM parameters
      timestamp: new Date().toISOString(),
      source: 'LP Masterclass 13 octobre',
    };

    const response = await fetch(WEBHOOK_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`Webhook returned ${response.status}`);
    }

    console.log('LEAD_OK', JSON.stringify({ ...lead, utm }));
    return res.status(200).json({ ok: true });
  } catch (e) {
    console.error('WEBHOOK_ERROR', e.message, JSON.stringify({ lead, utm }));
    return res.status(502).json({ ok: false, message: 'Une erreur est survenue. Réessayez dans un instant.' });
  }
}
