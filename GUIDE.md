# Masterclass ClientX 13 octobre - mise en place dans ClientX

Deux pages en code personnalisé, à intégrer dans le sous-compte **ClientX.ma** (`sMBdtpAowNv22pz2kxma`) (décision du 1er octobre ; la première version visait ClientX.us), plus le pixel. Le texte reprend le brief section par section (5.1 à 5.9).

```
src/            sources (inscription.html, confirmation.html)
config.json     ID formulaire, URLs images, pixel, lien Zoom, intervenants, logos
build.py        python3 build.py -> dist/ (à coller dans ClientX) + preview/ (aperçu local)
assets/         avatars Axel, Max, Jade (depuis Drive ClientX v2 > Avatares), à uploader
```

Aperçu local : `open preview/inscription.html` et `open preview/confirmation.html`.
L'aperçu affiche l'ANCIEN formulaire « Webinar ai » : ne rien soumettre depuis l'aperçu, cela créerait un vrai contact.

## 1. Images (2 min)

Médias ClientX > uploader `assets/axel.jpg`, `assets/max.jpg`, `assets/jade.jpg` > copier les 3 URLs dans `config.json` > `assets`.
Les logos ClientX et Webeuz sont déjà hébergés dans le sous-compte, et les logos clients sur clientx.uk : rien à faire pour eux.

## 2. Formulaire (10 min)

Sites > Formulaires > dupliquer **Webinar ai** (`UtIYQk5gwWxRT0ZUUqXl`) et nommer la copie **Masterclass 13oct**.

- Supprimer le titre « Inscrivez-vous au Webinaire » et le texte sur l'IA vocale : la carte de la page a déjà son propre titre.
- Bouton : **Je réserve ma place**.
- **UTM, à corriger impérativement.** L'ancien formulaire n'a que 3 champs cachés : `utm_source`, `utm_medium` et `utm_term`. Testé le 30/09 : `utm_medium` ne se remplit pas (mauvaise clé de requête), et `utm_campaign` et `utm_content` n'existent pas. Sans `utm_content`, impossible de compter les inscrits par créa.
  -> 5 champs cachés, chacun avec une **clé de requête** identique à son nom : `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`.
- Style, pour s'intégrer au fond sombre de la carte :
  - fond du formulaire transparent, sans bordure ni ombre, police Inter
  - champs : fond `#151a17`, bordure 1 px `#2a312c`, texte `#f4f6f5`, placeholder `#79817c`, arrondi 10 px
  - bouton : fond `#37ca37`, texte `#03170a`, gras, arrondi 12 px, pleine largeur
- Après envoi : **rediriger vers l'URL** de l'étape 2 (confirmation).
- Copier l'ID du nouveau formulaire dans `config.json` > `form_id`, puis lancer `python3 build.py`.

## 3. Funnel (10 min)

Nouveau funnel **Masterclass 13 octobre**. Un funnel neuf plutôt qu'un clone : on évite ainsi d'hériter des anciens pixels (Meta 133519173977115, AW-785053299, TikTok, LinkedIn).

| Étape | Chemin proposé | Contenu |
|---|---|---|
| 1. Inscription | `/masterclass-13-octobre` | `dist/01-inscription.html` |
| 2. Confirmation | `/masterclass-13-octobre-merci` | `dist/02-confirmation.html` |

Pour chaque page :
- une page vierge, fond de page `#000`
- une seule section **pleine largeur**, avec padding 0 sur la section, la ligne et la colonne
- un seul élément **Code personnalisé** (Custom JS/HTML), dans lequel on colle tout le fichier

Paramètres du funnel :
- **Code de suivi > Head** : coller `dist/00-tracking-head.html`. C'est le pixel `25447269248228502`, à confirmer.
- SEO de l'étape 1 : titre « Masterclass gratuite : Recrutez votre équipe d'agents IA · 13 octobre ».

Le PageView part sur les 2 étapes. Le **Lead** part uniquement sur la confirmation, une fois par session : un rechargement ne le déclenche pas deux fois.

## 4. Automatisations

- Workflow A : déclencheur « Formulaire envoyé : Masterclass 13oct » -> ajouter le tag `webinar-13oct`.
- Le formulaire natif Meta pose le même tag via le webhook existant.
- Workflow B : déclencheur « Tag ajouté : `webinar-13oct` » -> WhatsApp d'Axel et email de confirmation, puis les rappels du lundi 12 à 11h et du mardi 13 à 9h et 10h (brief section 6).
- Un seul point d'entrée : le tag. Les deux sources, page et formulaire Meta, suivent donc le même parcours.

## 5. Quand le lien Zoom existe

Renseigner `zoom_url` dans `config.json`, puis lancer `python3 build.py`. Recoller ensuite `dist/02-confirmation.html` : le lien Zoom est alors inclus dans « Ajouter à mon agenda » (Google, Outlook, .ics).

## 6. Intervenants

`config.json` > `speakers`. Par défaut : Mehdi Mourabit et Joris Blot, « Fondateur ClientX », repris du template et **à confirmer** avec Mehdi Mourabit.
- Sans photo, la page affiche les initiales.
- `"photo": "<url>"` ajoute une photo.
- `"speakers": []` retire la section.

Les photos du template vibe n'ont pas été reprises : elles semblent générées par IA.

## 7. Test de bout en bout (avant vendredi midi)

- [ ] Ouvrir l'étape 1 avec `?utm_source=meta&utm_medium=paid&utm_campaign=masterclass_13oct&utm_content=test_lp` et s'inscrire.
- [ ] Vérifier le contact dans ClientX : tag `webinar-13oct` et les **5** UTM remplies.
- [ ] Vérifier la redirection vers la confirmation, puis l'événement Lead dans le gestionnaire d'événements Meta (outil de test).
- [ ] Vérifier le WhatsApp d'Axel, l'email et le lien Zoom.
- [ ] Faire une inscription test par le formulaire natif Meta : même tag, même parcours.
- [ ] Tester sur mobile : la barre « Je réserve ma place » en bas d'écran apparaît après le haut de page et disparaît sur le formulaire.
