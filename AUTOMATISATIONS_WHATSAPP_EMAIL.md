# Masterclass ClientX du 13 octobre : intégration ClientX.ma et automatisations WhatsApp et email

Document préparé par Claude, assistant IA de Radouane Driouich, à la demande de Radouane, le 1er octobre 2026.

## 1. En bref

- **Événement** : Masterclass gratuite « Recrutez votre équipe d'agents IA », mardi 13 octobre 2026 à 11h, en ligne sur Zoom. Cible : dirigeants, gérants et directeurs commerciaux de TPE et PME au Maroc.
- **Sous-compte** : **ClientX.ma** (identifiant `sMBdtpAowNv22pz2kxma`). À ne pas confondre avec ClientX Media.ma ni ClientX.us.
- **Point d'entrée des automatisations** : le tag `webinar-13oct`, posé par la landing page et par le formulaire natif Meta.
- **Canaux** : WhatsApp (les messages sont signés Axel, l'agent IA de ClientX) et email, en doublon à chaque étape.
- **Lien Zoom** : Radouane le communique dès que le compte Zoom Pro est pris. Il est prévu comme valeur personnalisée : il suffira de la remplir une fois pour que tous les messages soient à jour.

## 2. À créer dans ClientX.ma

### 2.1 Pour brancher la landing page

1. **Jeton d'intégration privée** (Paramètres > Intégrations privées) avec les droits : contacts en lecture et écriture, champs personnalisés en lecture.
2. **Variables d'environnement** de l'hébergement (Vercel, ou équivalent) :
   - `CLIENTX_TOKEN` = le jeton ci-dessus
   - `CLIENTX_LOCATION_ID` = `sMBdtpAowNv22pz2kxma`
   - `CLIENTX_TAG` = `webinar-13oct`
3. **Champs personnalisés du contact** (texte), retrouvés automatiquement par leur nom : `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`, `Fonction`.
4. Après mise en ligne : une inscription test avec `?utm_source=test&utm_medium=test&utm_campaign=masterclass_13oct` doit créer le contact avec le tag, les 5 UTM et la fonction.

Le détail technique (code, construction, publication) est dans `GUIDE.md`, `LP_ET_CONTEXTE_CLIENTX.md` et `CHANGEMENTS.md`.

### 2.2 Pour les automatisations

**Valeurs personnalisées** (Paramètres > Valeurs personnalisées) :

| Valeur | Contenu | Qui la fournit |
|---|---|---|
| `lien_zoom_masterclass` | lien de connexion Zoom | Radouane, dès la prise du compte Zoom Pro |
| `lien_replay_masterclass` | lien du replay | après le live |
| `lien_rdv_agent_ia` | calendrier de réservation ClientX pour mettre en place l'agent IA du participant | à créer (voir points ouverts) |
| `lien_communaute` | accès à la communauté réservée aux participants | à confirmer |

**Tags** : `webinar-13oct` (inscrit), `webinar-present`, `webinar-absent`, `webinar-rdv` (créneau réservé).

**Modèles WhatsApp** : à soumettre à Meta au moins 24 à 48 heures avant le premier envoi. Catégorie « Utilitaire » pour la confirmation et les rappels, « Marketing » pour les messages d'après live. Dans les modèles, les variables deviennent `{{1}}`, `{{2}}`, etc., à relier au prénom et aux valeurs personnalisées.

**Fuseau des workflows** : Africa/Casablanca.

## 3. Workflow 1 : inscription et rappels

Déclencheur : tag `webinar-13oct` ajouté. Chaque étape envoie le WhatsApp puis l'email.

| Étape | Quand |
|---|---|
| 1. Confirmation | immédiatement |
| 2. La veille | lundi 12 octobre, 11h |
| 3. Le jour même | mardi 13 octobre, 9h |
| 4. 30 minutes avant | mardi 13 octobre, 10h30 |
| 5. C'est parti (WhatsApp seul) | mardi 13 octobre, 11h |

Pour une inscription faite après une date de rappel, l'étape passée est sautée (condition « si la date est déjà passée, continuer »).

## 4. Workflow 2 : après le live

Déclencheur : tags `webinar-present` ou `webinar-absent`, posés après le live à partir de la liste des participants Zoom.

| Étape | Pour qui | Quand |
|---|---|---|
| 6. Merci et replay | présents | mardi 13 octobre, 15h |
| 7. Replay | absents | mercredi 14 octobre, 10h |
| 8. Relance par Max | inscrits sans le tag `webinar-rdv` | mardi 20 octobre, 10h |

## 5. Les messages

Champs de fusion ClientX : `{{contact.first_name}}` pour le prénom, `{{custom_values.lien_zoom_masterclass}}` etc. pour les liens. Expéditeur des emails : ClientX.

### Étape 1 : confirmation (immédiatement)

**WhatsApp**

> Bonjour {{contact.first_name}}, c'est Axel, l'agent IA de ClientX. Votre place pour la Masterclass « Recrutez votre équipe d'agents IA » est confirmée : mardi 13 octobre à 11h, en ligne sur Zoom.
> Votre lien : {{custom_values.lien_zoom_masterclass}}
> Une question d'ici là ? Répondez simplement à ce message.

**Email**

Objet : Votre place est confirmée : Masterclass du mardi 13 octobre, 11h

> Bonjour {{contact.first_name}},
>
> Votre place pour la Masterclass « Recrutez votre équipe d'agents IA » est confirmée.
>
> Mardi 13 octobre, 11h, en ligne sur Zoom
> Votre lien de connexion : {{custom_values.lien_zoom_masterclass}}
>
> Au programme, des cas d'usage réels montrés en direct avec trois agents IA : Axel, qui répond à vos prospects et prend les rendez-vous ; Max, qui automatise vos tâches répétitives, comme la relance des impayés ; et Jade, qui gère vos avis Google.
>
> À la fin de la Masterclass, vous repartez avec votre agent IA et vous rejoignez la communauté réservée aux participants.
>
> Ajoutez la date à votre agenda pour ne pas la manquer. Une question ? Répondez à cet email.
>
> À mardi,
> L'équipe ClientX

### Étape 2 : la veille (lundi 12 octobre, 11h)

**WhatsApp**

> Bonjour {{contact.first_name}}, c'est demain ! Masterclass « Recrutez votre équipe d'agents IA », mardi 13 octobre à 11h, sur Zoom.
> Votre lien : {{custom_values.lien_zoom_masterclass}}
> Préparez vos questions : un temps d'échange est prévu en direct.

**Email**

Objet : C'est demain à 11h : votre Masterclass ClientX

> Bonjour {{contact.first_name}},
>
> Rendez-vous demain, mardi 13 octobre à 11h, pour la Masterclass « Recrutez votre équipe d'agents IA ».
>
> Votre lien de connexion : {{custom_values.lien_zoom_masterclass}}
>
> Vous verrez en direct Axel, Max et Jade au travail, et vous pourrez poser vos questions aux intervenants. Notez les situations de votre entreprise que vous aimeriez confier à un agent IA : nous y répondrons pendant l'échange.
>
> À demain,
> L'équipe ClientX

### Étape 3 : le jour même (mardi 13 octobre, 9h)

**WhatsApp**

> Bonjour {{contact.first_name}}, la Masterclass commence aujourd'hui à 11h.
> Votre lien : {{custom_values.lien_zoom_masterclass}}
> À tout à l'heure !

**Email**

Objet : Aujourd'hui à 11h : Recrutez votre équipe d'agents IA

> Bonjour {{contact.first_name}},
>
> C'est aujourd'hui : la Masterclass commence à 11h.
>
> Votre lien de connexion : {{custom_values.lien_zoom_masterclass}}
>
> À tout à l'heure,
> L'équipe ClientX

### Étape 4 : 30 minutes avant (mardi 13 octobre, 10h30)

**WhatsApp**

> Dans 30 minutes, on commence ! Rejoignez la Masterclass ici : {{custom_values.lien_zoom_masterclass}}

**Email**

Objet : On commence dans 30 minutes

> Bonjour {{contact.first_name}},
>
> La Masterclass « Recrutez votre équipe d'agents IA » commence dans 30 minutes.
>
> Rejoignez-nous ici : {{custom_values.lien_zoom_masterclass}}
>
> L'équipe ClientX

### Étape 5 : c'est parti (mardi 13 octobre, 11h, WhatsApp seul)

> C'est parti, {{contact.first_name}} : la Masterclass commence. Rejoignez-nous : {{custom_values.lien_zoom_masterclass}}

### Étape 6 : merci et replay, présents (mardi 13 octobre, 15h)

**WhatsApp**

> Merci d'avoir participé à la Masterclass, {{contact.first_name}} !
> Le replay : {{custom_values.lien_replay_masterclass}}
> Pour mettre en place votre agent IA, réservez votre créneau avec notre équipe : {{custom_values.lien_rdv_agent_ia}}
> Et la communauté réservée aux participants, c'est ici : {{custom_values.lien_communaute}}

**Email**

Objet : Merci pour votre participation : replay et prochaine étape

> Bonjour {{contact.first_name}},
>
> Merci d'avoir participé à la Masterclass « Recrutez votre équipe d'agents IA ».
>
> Le replay est disponible ici : {{custom_values.lien_replay_masterclass}}
>
> Prochaine étape : mettre en place votre agent IA. Réservez votre créneau avec notre équipe : {{custom_values.lien_rdv_agent_ia}}
>
> Vous avez aussi accès à la communauté réservée aux participants : {{custom_values.lien_communaute}}
>
> À très vite,
> L'équipe ClientX

### Étape 7 : replay, absents (mercredi 14 octobre, 10h)

**WhatsApp**

> Bonjour {{contact.first_name}}, vous n'avez pas pu assister à la Masterclass hier ? Le replay est disponible ici : {{custom_values.lien_replay_masterclass}}
> Pour mettre en place votre agent IA avec notre équipe : {{custom_values.lien_rdv_agent_ia}}

**Email**

Objet : Le replay de la Masterclass est disponible

> Bonjour {{contact.first_name}},
>
> Vous n'avez pas pu assister à la Masterclass « Recrutez votre équipe d'agents IA » ? Le replay est disponible ici : {{custom_values.lien_replay_masterclass}}
>
> Vous y verrez Axel, Max et Jade répondre à des prospects, automatiser des relances et gérer des avis Google, sur des cas réels.
>
> Pour mettre en place votre agent IA, réservez votre créneau avec notre équipe : {{custom_values.lien_rdv_agent_ia}}
>
> L'équipe ClientX

### Étape 8 : relance par Max (mardi 20 octobre, 10h, inscrits sans créneau réservé)

**WhatsApp**

> Bonjour {{contact.first_name}}, c'est Max, l'agent IA de relance de ClientX : votre créneau pour mettre en place votre agent IA est toujours disponible. Réservez ici : {{custom_values.lien_rdv_agent_ia}}

**Email**

Objet : Votre agent IA vous attend

> Bonjour {{contact.first_name}},
>
> C'est Max, l'agent IA qui automatise les relances chez ClientX. Comme vous l'avez vu pendant la Masterclass, je ne laisse rien passer : votre créneau pour mettre en place votre agent IA est toujours disponible.
>
> Réservez ici : {{custom_values.lien_rdv_agent_ia}}
>
> Max, pour l'équipe ClientX

## 6. Points ouverts

- **Lien Zoom** : Radouane le transmet dès la prise du compte Zoom Pro (à mettre dans `lien_zoom_masterclass`, et dans `config.json` > `zoom_url` de la landing page, puis republication).
- **« Votre agent IA »** : la forme exacte de ce que reçoit chaque participant (agent configuré, essai, séance de mise en place) reste à confirmer par Mehdi Mourabit. Les messages des étapes 6 à 8 renvoient pour l'instant vers un créneau de mise en place (`lien_rdv_agent_ia`).
- **Communauté** : lien d'accès à confirmer (`lien_communaute`).
- **Présents et absents** : méthode pour poser les tags après le live (export des participants Zoom puis import, ou intégration Zoom).
- **Expéditeur des emails** et numéro WhatsApp d'envoi du sous-compte ClientX.ma : à vérifier avant les tests.

## 7. Test avant lancement

- [ ] Inscription test par la landing page avec son propre numéro : contact créé dans ClientX.ma, tag `webinar-13oct`, UTM et fonction remplies
- [ ] WhatsApp et email de confirmation reçus, prénom et lien corrects
- [ ] Inscription test par le formulaire natif Meta : même tag, même parcours
- [ ] Rappels : vérifier sur un contact test que les dates et heures (Africa/Casablanca) sont bonnes
- [ ] Après le live : tags présents et absents posés, étapes 6 et 7 envoyées au bon groupe
