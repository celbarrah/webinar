# Modifications du 1er octobre 2026 (v5)

Faites par Claude, assistant IA de Radouane Driouich, à partir des retours de Radouane. Sauvegardes : fichiers `*.avant-v5`.

**Page d'inscription (`src/inscription.html`)**
1. Logo de l'en-tête agrandi : 42 px de haut (32 px sur mobile).
2. Accroche ajoutée sous le titre : « Et repartez avec votre agent IA. » ; reprise dans le titre du bas de page et dans les descriptions de partage (`build.py`).
3. Durée retirée partout (« En une heure », « Une heure pour… », question FAQ « Combien de temps dure-t-elle ? »). « 11h (heure du Maroc) » devient « 11h ».
4. Infos date / heure / Zoom / places : en texte simple avec icône, plus en pastilles (on aurait dit des boutons). Idem pour les canaux sous chaque agent, séparés par des points.
5. « Leader au Maroc & Afrique » retiré du bandeau des logos : il reste « Ils nous font confiance ».
6. Max présenté comme « Agent IA d'automatisation » ; la relance des impayés devient l'exemple montré en direct. Axel et Jade : « Agent IA · … ». Carte « Pour qui » et image de partage (`src/og.html`) alignées.
7. Boutons en double retirés : celui sous les agents (avec la ligne « Gratuit · Mardi 13 octobre à 11h · En ligne sur Zoom ») et celui de « Après votre inscription ». Restent : en-tête, formulaire, bas de page, barre mobile.
8. Section Programme reformulée en « Ce que vous allez avoir » : cas d'usage réels en direct, votre agent IA, accès à la communauté réservée aux participants, questions-réponses. La ligne « Environ une heure · Mardi 13 octobre, 11h · Replay envoyé aux inscrits » est retirée.

9. Boutons : un texte différent pour chacun (plus de « Je réserve ma place » répété). En-tête « Je m'inscris » (mobile « S'inscrire »), titre du formulaire « Inscription gratuite · Places limitées », bouton du formulaire « Je réserve ma place » (même texte que le bouton des pubs), bas de page « Je participe à la Masterclass », barre mobile « Rejoindre ». L'ancien bouton du haut de page, masqué sur tous les écrans, est supprimé du code.

**Intervenants (`config.json`)** : Mehdi Mourabit « Co-fondateur de ClientX et CEO de Webeuz », Joris Blot « Co-fondateur de ClientX ».

**Page de confirmation (`src/confirmation.html`)** : logo agrandi, infos en texte simple, « 11h » sans fuseau, « Invitez un associé » devient « Partagez l'invitation » / « Une personne de votre entourage professionnel serait intéressée ? ».

---

# Modifications du 30 septembre 2026

Faites par Claude, assistant IA de Radouane Driouich, à la demande de Radouane, sur la base de la version reçue le 30/09 à 17h35.

**Version de revue en ligne** : https://masterclass-clientx-apercu.vercel.app
Publiée sur le compte Vercel de Radouane, sans les clés ClientX : le formulaire répond « Les inscriptions ouvrent dans quelques instants » et n'enregistre rien. Page en noindex. À ne pas utiliser pour les pubs.

---

## Page d'inscription (`src/inscription.html`)

1. **Formulaire dans le haut de page, à droite du texte.** L'identifiant `inscription` est maintenant sur la carte du formulaire : tous les boutons « Je réserve ma place » y mènent. La carte « Votre équipe IA, aujourd'hui » du haut de page est retirée (elle répétait la section « Ce que vous verrez en direct »).
2. **Mobile** : le formulaire arrive juste après les infos de date (`.hero-copy` en `display: contents` + `order`), les intervenants et le compte à rebours en dessous. Le bouton « Je réserve ma place » du haut de page est masqué, le formulaire étant juste en dessous. Sur iPhone, le formulaire commence dans le premier écran.
3. **Logos** : grille fixe centrée au lieu de la bande défilante, dont le masque en dégradé coupait les logos. Coralia et Renault Trucks sont retirés de `config.json` : leurs fichiers ont un fond plein et s'affichaient en bloc gris avec le filtre blanc. À remettre avec une version blanche détourée.
4. **Intervenants dans le haut de page** : Mehdi Mourabit (Fondateur de ClientX et CEO de Webeuz), Joris Blot (Cofondateur de ClientX), Radouane Driouich (Directeur des opérations média, Webeuz), avec photos dans `assets/speakers/`. Nouveau token `{{SPEAKERS_HERO}}`. La section « Vos intervenants » du bas est retirée pour ne pas faire doublon. Sources des photos : webeuz.com, clientx.uk, page Webeuz Academy.
5. **Bas de page** : la section d'inscription devient « Après votre inscription » (3 étapes, classe `.aft`) avec un bouton qui remonte au formulaire. Attention, la classe `.steps` est réservée à la section Programme.
6. Titre du haut de page ramené à 64 px maximum.
7. FAQ « Faut-il des connaissances techniques ? » reformulée : « Non, aucune. La démonstration est pensée pour les dirigeants et les équipes commerciales : tout est montré sur des cas concrets, sans jargon technique. »
8. Bouton « Réserver » de l'en-tête : 42 px de haut sur mobile.

## Page de confirmation (`src/confirmation.html`)

1. **Trois boutons agenda visibles** au lieu du menu déroulant : Google Agenda, Outlook (Microsoft 365), Apple et autres (.ics avec rappel 30 minutes avant).
2. **Bloc « Invitez un associé »** : WhatsApp, Email, Copier le lien. Liens suivis en `utm_source=parrainage`, `utm_medium=whatsapp` / `email` / `lien`, `utm_campaign=masterclass_13oct`. L'adresse de base est `site_url` dans `config.json`.

## `build.py`

- `speakers_html` et `speakers_hero_html` : les photos en chemin local sont préfixées `../` pour `preview/`.
- Copie de `assets/speakers/` vers `site/assets/speakers/` au build.
- `logos_html` : plus de doublon (grille fixe).
- `share_tokens` ajouté aux tokens communs (liens de la page de confirmation).
- Alerte au build : pour `dist/` (version ClientX de secours), les photos des intervenants doivent être chargées dans les médias ClientX et leur URL mise dans `config.json` > `speakers` > `photo`.

## Publier sur votre projet Vercel (celui qui a les clés ClientX)

```
python build.py
cd site
npx vercel --prod --yes --scope meladraouy-4670s-projects
```

Puis le test de bout en bout de `GUIDE.md`, section 7.

## Toujours ouvert

- `zoom_url` vide (compte Zoom Pro à activer).
- « 11h (heure du Maroc) » : tranché le 01/10, « 11h » seul (v5).
- Les sauvegardes intermédiaires (`*.avant-intervenants`, `*.avant-v2`, `*.avant-v3`, `*.avant-v4`) restent sur le poste de Radouane et ne sont pas dans ce zip.
