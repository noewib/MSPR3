# Plan d'Inclusion, de Communication & de Collaboration d'Équipe
## Solution de Prédiction de la Consommation Électrique Nationale (EDF / RTE)

**Référentiel RNCP36582 – Blocs de compétences 3 & 4**  
**Promotion 2025-2026 – MSPR TPRE932 & TPRE942**

---

> **Équipe Projet – Attribution des rôles**
>
> | Membre | Rôle Bloc 3 | Rôle Bloc 4 |
> |---|---|---|
> | **Noé Wibaut** | Runbook, doc finale & slides | Project framing & planning *(coordinateur)* |
> | **Djamel Chebbah** | Deployment architecture | Agile management & tracking |
> | **Paul-Henri Dourneau** | Data & preprocessing | **Communication, inclusion & slides** *(référent de cette partie)* |
> | **Dorian Marty** | Maintainability & simulation | Technical specifications |
> | **Thuy-Trang Nguyen** | Models & training | Functional specifications |

---

## Sommaire

1. [Stratégie d'Accueil et d'Inclusion des Handicaps](#1-stratégie-daccueil-et-dinclusion-des-handicaps)
   - 1.1 Principes fondateurs de la démarche inclusive
   - 1.2 Prise en compte des différents types de handicap
   - 1.3 Adaptations dans l'équipe projet
   - 1.4 Articulation avec le référent handicap de l'entreprise

2. [Communication Interculturelle & Prévention des Conflits](#2-communication-interculturelle--prévention-des-conflits)
   - 2.1 Contexte : EDF et ses acteurs internationaux
   - 2.2 Modes de communication adaptés aux cultures, langues et fuseaux horaires
   - 2.3 Exemples de malentendus multiculturels et stratégies de prévention
   - 2.4 Solutions innovantes pour favoriser les interactions

3. [Processus de Communication Inclusif & Réunions à Distance](#3-processus-de-communication-inclusif--réunions-à-distance)
   - 3.1 Processus de communication : daily, weekly, rétros, comités
   - 3.2 Mise en place du fil de discussion (règles de fonctionnement)
   - 3.3 Kit de réunion à distance

---

# 1. Stratégie d'Accueil et d'Inclusion des Handicaps

> **Responsable de cette partie (Bloc 4) : Paul-Henri Dourneau** – Communication, inclusion & slides Bloc 4

---

## 1.1 Principes Fondateurs de la Démarche Inclusive

### 1.1.1 Cadre Légal et Éthique

La démarche inclusive du projet EDF/RTE s'inscrit dans un cadre légal et éthique structuré à trois niveaux :

| Niveau | Texte de référence | Exigence principale |
|---|---|---|
| **International** | Convention ONU relative aux droits des personnes handicapées (2006) | Participation pleine et effective à la vie professionnelle sur la base de l'égalité avec les autres |
| **Européen** | Directive 2000/78/CE · Charte des droits fondamentaux de l'UE (Art. 21 & 26) | Non-discrimination · Intégration des personnes handicapées |
| **Français** | Loi n°2005-102 (Loi Handicap) · Obligation d'emploi des travailleurs handicapés (OETH – 6 % de l'effectif) | Aménagement raisonnable du poste · Déclaration DOETH annuelle |
| **Normatif** | WCAG 2.1 niveau AA (Web Content Accessibility Guidelines) | Accessibilité numérique de tous les contenus web et outils collaboratifs |
| **EDF** | Accord GEIP (Gestion des Emplois et des Parcours Professionnels) EDF 2023-2026 | Mission Handicap EDF : accompagnement, maintien dans l'emploi, sensibilisation |

### 1.1.2 Le Modèle Social du Handicap vs Modèle Médical

La démarche inclusive du projet repose sur le **modèle social du handicap**, reconnu par la Convention ONU et adopté par EDF dans ses politiques RH :

```
MODÈLE MÉDICAL (à éviter)          MODÈLE SOCIAL (adopté)
────────────────────────────        ──────────────────────────────────
La personne EST handicapée.         La personne A un handicap.
Le problème est dans la             Le problème est dans l'inadaptation
personne.                           de l'environnement.
Solution : soigner / guérir.        Solution : adapter l'environnement.
Regard centré sur la déficience.    Regard centré sur les capabilités.
```

**Application concrète au projet :** Au lieu de demander à un collaborateur daltonien de « s'adapter » aux dashboards rouge/vert existants, l'équipe adapte les dashboards Grafana pour utiliser des palettes ColorBrewer bleu/orange accessibles à tous.

### 1.1.3 Les 5 Piliers de la Démarche Inclusive du Projet

```
        ┌─────────────────────────────────────────────────────┐
        │                                                     │
   ① ANTICIPER    ② ADAPTER     ③ FORMER    ④ OUTILLER   ⑤ SUIVRE
  (dès la         (l'environ-   (l'équipe   (solutions   (l'efficacité
  conception)     nement)       & les       numériques)  des mesures)
                               process)
        │                                                     │
        └───────────────── INCLUSION UNIVERSELLE ─────────────┘
```

---

## 1.2 Prise en Compte des Différents Types de Handicap

### 1.2.1 Vue d'Ensemble des Types de Handicap

Le projet EDF/RTE implique des outils numériques (interfaces web, dashboards, API docs, visioconférences, documents techniques) et des modes de collaboration variés (synchrone/asynchrone, présentiel/distanciel). La grille ci-dessous recense les adaptations nécessaires pour chaque grande catégorie de handicap :

| Catégorie | Types inclus | Prévalence estimée (France) | Impact potentiel dans le projet |
|---|---|:---:|---|
| **Handicap visuel** | Cécité totale, malvoyance, daltonisme (deutéranopie, protanopie, tritanopie) | 1,7 M (dont 2,6 M daltoniens) | Tableaux de bord Grafana · API Swagger · Documents techniques |
| **Handicap auditif** | Surdité totale, malentendance, acouphènes | 5,5 M | Visioconférences · Formations orales · Réunions internationales |
| **Handicap moteur** | Paralysie, mobilité réduite des membres supérieurs, fatigue chronique | 2,3 M | Navigation clavier · Outils de développement · Saisie longue |
| **Handicap cognitif** | TDAH, troubles dys (dyslexie, dyscalculie), troubles du spectre autistique (TSA), troubles anxieux | 3,5 M (dont ~8 % TSA/TDAH estimés en entreprise) | Documentation dense · Réunions longues · Ambiguïtés des consignes |
| **Handicap psychique** | Dépression, burn-out, troubles bipolaires | 3 M | Charge de travail · Pression des délais · Communication du stress |
| **Handicap invisible** | Maladies chroniques (épilepsie, diabète, maladies inflammatoires), cancer | 80 % des handicaps sont invisibles | Gestion des pauses · Aménagements flexibles |

---

### 1.2.2 Handicaps Visuels

#### A. Daltonisme (Deutéranopie, Protanopie, Tritanopie)

Le daltonisme touche environ **8 % des hommes** et 0,5 % des femmes en France. Dans une équipe de 5 personnes (dont potentiellement 1 homme daltonien), la prise en compte est indispensable.

**Impact identifié dans le projet :**
- Les dashboards Grafana utilisent par défaut des indicateurs rouge/vert pour les alertes de monitoring (drift, uptime…).
- Les graphiques de comparaison des performances des 4 modèles IA utilisent des couleurs distinctes.
- La documentation technique utilise des codes couleur pour distinguer les zones de criticité (MAPE).

**Adaptations implémentées :**

| Outil / Livrable | Problème identifié | Adaptation réalisée |
|---|---|---|
| **Dashboard Grafana** | Alertes rouge (critique) / vert (nominal) → invisibles pour les deutéranopes | Remplacement par palette **bleu/orange** (ColorBrewer) + symboles textuels `✔ ⚠ ✖` |
| **Graphiques de performance** | Courbes de couleur seules pour différencier les 4 modèles | Ajout de formes différentes (ronds, carrés, triangles, croix) + labels directs sur courbe |
| **Documentation** | Zones de criticité exprimées en rouge/orange/vert | Reformulation en texte explicite : **Zone Critique** · **Zone Vigilance** · **Zone Nominale** |
| **Code couleur API Swagger** | Boutons POST/GET en vert/orange → distinction difficile | Ajout de l'étiquette texte du verbe HTTP |

**Outils de vérification :**
- **Coblis** (Color Blindness Simulator) : simulation en ligne de tout visuel dans les différentes formes de daltonisme.
- **Colour Contrast Analyser** : vérification du ratio de contraste WCAG (minimum 4,5:1 pour le texte normal).
- **WAVE** (Web Accessibility Evaluation Tool) : audit automatique de l'accessibilité des interfaces web.

#### B. Malvoyance et Cécité

**Adaptations pour la malvoyance :**
- Taille de police minimale de **16px** dans tous les documents partagés.
- Utilisation de la police **OpenDyslexic** ou **Arial** (sans serif) dans les présentations.
- Contraste texte/fond minimum **4,5:1** (WCAG AA) ou **7:1** (WCAG AAA pour les cas sévères).
- Zoom de l'interface jusqu'à **200 %** sans perte de fonctionnalité.

**Adaptations pour la cécité totale :**
- Documentation technique au format **Markdown pur** (compatible lecteurs d'écran NVDA, JAWS, VoiceOver).
- Tous les graphiques accompagnés d'une **description textuelle alternative** (`alt text` ou paragraphe de données brutes).
- Tableaux de données structurés avec **en-têtes de colonne et de ligne explicites** (accessibles aux tableaux de bord Grafana en mode données brutes).

---

### 1.2.3 Handicaps Auditifs

**Impact identifié dans le projet :**
- Réunions synchrones en visioconférence (Sprint Reviews, COPRO, formations).
- Démos orales avec commentaire vocal (démonstrations API FastAPI).
- Contenu audio des formations sur l'utilisation de l'outil.

**Adaptations implémentées :**

| Contexte | Adaptation |
|---|---|
| **Visioconférences Teams/Zoom** | Activation systématique du **sous-titrage automatique en temps réel** (Teams Live Captions · Zoom CC) |
| **Réunions internationales** | **Enregistrement vidéo systématique** de toutes les réunions · Transcription automatique disponible en différé |
| **Démos et formations** | **Support visuel obligatoire** accompagnant toute présentation orale · Aucune information communiquée oralement uniquement |
| **Décisions importantes** | Toute décision verbale d'une réunion est **résumée par écrit** dans le compte-rendu partagé dans les 2h |
| **Alertes système** | Les alertes Grafana sont **visuelles ET textuelles** (pas d'alerte sonore exclusive) |
| **Slack / Teams** | Préférence aux **messages écrits** sur les réunions orales ad hoc pour les échanges non urgents |

**Outils recommandés :**
- **Microsoft Teams** : sous-titrage Live Captions (FR, EN, ZH, DE, IT, ES).
- **Otter.ai** : transcription automatique temps réel + résumé post-réunion (FR/EN).
- **Krisp** : réduction du bruit ambiant pour améliorer la clarté audio des intervenants.

---

### 1.2.4 Handicaps Moteurs

**Impact identifié dans le projet :**
- Utilisation intensive du clavier pour le développement (VS Code, terminal, Git).
- Navigation dans les interfaces Jira, Confluence, Grafana.
- Sessions de coding longues (feature engineering, CI/CD).

**Adaptations possibles :**

| Type de besoin | Adaptation | Outil / Solution |
|---|---|---|
| **Navigation clavier** | Toutes les interfaces doivent être navigables au clavier (Tab, flèches, Enter) | WCAG 2.1 – Critère 2.1.1 · Tests de navigation clavier |
| **Dictée vocale** | Alternative à la saisie clavier pour la rédaction de documentation | Windows 11 Dictée vocale · Dragon NaturallySpeaking |
| **Raccourcis et macros** | Réduction des gestes répétitifs | VS Code snippets personnalisés · Autohotkey macros |
| **Fatigue musculaire** | Pauses régulières formalisées (technique Pomodoro adaptée) | **Règle des 25/5 min** imposée dans les sessions de pair-programming |
| **Ergonomie du poste** | Matériel adapté fourni par EDF (Mission Handicap) | Clavier ergonomique · Souris verticale · Support écran |
| **Tâches fractionnées** | Découpage des tâches en sous-étapes ≤ 4h (WBS granulaire) | Jira sous-tâches · Tickets atomiques |

---

### 1.2.5 Handicaps Cognitifs (TDAH, TSA, Troubles Dys)

Le handicap cognitif représente l'une des catégories les plus impactantes dans un projet de développement logiciel en raison de la **surcharge cognitive** inhérente à la gestion simultanée du code, des spécifications, des réunions et de la documentation.

#### A. TDAH (Trouble du Déficit de l'Attention avec ou sans Hyperactivité)

**Manifestations possibles dans le projet :**
- Difficulté à maintenir l'attention lors de réunions longues ou peu structurées.
- Tendance à la procrastination sur les tâches peu stimulantes (documentation).
- Créativité et réactivité élevées dans les phases de problème à résoudre.

**Adaptations implémentées :**

| Contexte | Adaptation |
|---|---|
| **Réunions** | Durée limitée à **30 min maximum** · Ordre du jour envoyé 24h avant · Chronomètre affiché · Pauses de 5 min toutes les 25 min (Pomodoro) |
| **Tâches** | Décomposition en **micro-tâches de < 1h** · Affichage des sous-tâches dans Jira · Checkpoint quotidien dans le daily asynchrone |
| **Documentation** | Utilisation de **listes à puces courtes** plutôt que de blocs de texte · Titres hiérarchiques · Résumé en début de document |
| **Notifications** | **Mode Ne pas déranger** activé pendant les blocs de travail profond (Deep Work) · Réponse aux messages dans des plages définies |
| **Outil spécifique** | **Goblin.tools** (décomposition automatique de tâches complexes en sous-étapes simples) |

#### B. Troubles du Spectre de l'Autisme (TSA)

**Manifestations possibles dans le projet :**
- Préférence pour la communication écrite structurée vs orale non structurée.
- Sensibilité aux imprévus et aux changements de planning.
- Expertise technique souvent très approfondie dans un domaine spécifique.
- Difficulté possible avec les consignes ambiguës ou implicites.

**Adaptations implémentées :**

| Contexte | Adaptation |
|---|---|
| **Communication** | **Formulations directes et sans ambiguïté** · Pas de métaphores culturelles · Éviter le sarcasme |
| **Planning** | **Agenda des réunions partagé 48h à l'avance** · Pas de réunion surprise · Changements de planning notifiés avec > 24h de préavis |
| **Consignes** | Critères d'acceptation **explicites, mesurables et non interprétables** dans les User Stories (DoR) |
| **Environnement** | Réunions avec **fond neutre virtuel** disponible · Pas d'obligation de caméra allumée |
| **Feedback** | Feedback **factuel et constructif** (basé sur les faits, pas sur les intentions) · Jamais de critique personnelle |

#### C. Troubles Dys (Dyslexie, Dyscalculie, Dyspraxie)

**Adaptations implémentées :**

| Type | Adaptation |
|---|---|
| **Dyslexie** | Police **OpenDyslexic** disponible dans les outils partagés · Espacement augmenté (1,5 interligne) · Pas de texte justifié (préférer l'alignement gauche) · Documents en **mode sombre** disponibles |
| **Dyscalculie** | Métriques toujours accompagnées de leur **interprétation textuelle** (ex: "4,68 % = en dessous du seuil critique de 5 %, c'est bon") · Graphiques visuels préférés aux tableaux de chiffres |
| **Dyspraxie** | Interfaces **simplifiées** avec grands boutons cliquables · Raccourcis clavier documentés · Navigation clavier complète |

---

### 1.2.6 Handicaps Psychiques et Situations de Burn-out

**Adaptations pour le bien-être mental de l'équipe :**

| Mesure | Description |
|---|---|
| **Charge de travail monitored** | Le Scrum Master (Djamel) surveille la charge hebdomadaire de chaque membre. Aucune US ne peut être ajoutée en cours de sprint sans accord de toute l'équipe. |
| **Droit à la déconnexion** | Aucun message ni notification attendus en dehors des heures de travail (défaut : 9h-18h CET). Le mode asynchrone protège ce droit. |
| **Signal de détresse** | Un emoji 🆘 dans le daily asynchrone signale une situation de surcharge → le SM organise un appel individuel dans les 2h. |
| **Rétrospective Safe Space** | La rétrospective est un espace bienveillant : aucun jugement, aucune attribution personnelle des problèmes. Règle d'or de la Rétrospective Prime Directive. |
| **Célébration des succès** | Chaque livraison de sprint → message de félicitation collectif sur `#general`. Les contributions individuelles sont nommées. |

---

## 1.3 Adaptations dans l'Équipe Projet

### 1.3.1 Matrice des Adaptations par Livrable du Projet

| Livrable / Outil | Adaptation visuelle | Adaptation auditive | Adaptation cognitive | Adaptation motrice |
|---|---|---|---|---|
| **Dashboards Grafana** | Palette ColorBrewer · Alt text · Mode données brutes | Alertes visuelles + textuelles | Légende claire · 3 niveaux max | Navigation clavier complète |
| **API Swagger UI** | Contraste ≥ 4,5:1 · Étiquettes texte verbes | N/A | Exemples de requêtes visibles | Tab navigation |
| **Documentation Markdown** | Alt text images · Contraste élevé | Transcription des contenus audio | Listes courtes · Résumés · Titres H1-H3 | Police OpenDyslexic disponible |
| **Présentations slides** | Police ≥ 28pt · ColorBrewer · No PDF scanned | Sous-titres enregistrés | 1 idée par slide · Résumé final | Format PDF navigable |
| **Visioconférences** | Fond neutre · Partage d'écran lisible | Live Captions Teams · Enregistrement | Ordre du jour structuré · Durée limitée | Pas d'obligation de caméra |
| **Jira / Backlog** | Couleurs secondaires uniquement | Export écrit des priorités | Tâches ≤ 4h · Checklist DoD visible | Interface web navigable au clavier |
| **Code source** | — | — | Commentaires explicatifs · Fonctions courtes | Snippets VS Code · Autocomplete |

### 1.3.2 Aménagements du Temps de Travail

| Situation | Aménagement proposé | Décision par |
|---|---|---|
| **Difficulté de concentration prolongée** | Sessions de travail en Pomodoro (25 min travail / 5 min pause) · Deep Work blocks de 2h max | Membre + SM |
| **Fatigue chronique** | Répartition des tâches sur des créneaux flexibles · Pas de réunion avant 10h ou après 17h | Membre + PO |
| **Stress de performance avant soutenance** | Répétitions en groupe · Questions/réponses simulées · Pair-programming pour les parties complexes | SM + PO |
| **Surcharge cognitive temporaire** | Déplacement d'une US non critique vers le sprint suivant (décision SM + PO) | SM + PO |
| **Besoin de temps supplémentaire sur une tâche** | Allongement de l'estimation lors du Sprint Planning · Pas de jugement | Équipe |

### 1.3.3 Adaptations des Formats de Documentation

```
FORMAT STANDARD          FORMAT INCLUSIF ADAPTÉ
───────────────          ──────────────────────────────────────────────────
Bloc de texte dense   →  Paragraphes courts (< 5 lignes) + listes à puces
Tableaux complexes    →  Tableaux simplifiés + résumé textuel
Couleurs seules       →  Couleurs + icônes + étiquettes texte
Jargon technique      →  Glossaire en annexe + explication inline
PDF non structuré     →  Markdown structuré avec H1/H2/H3 hiérarchiques
Slides chargées       →  Règle "1 idée par slide" + résumé final
Instructions vagues   →  Critères d'acceptation mesurables et explicites
```

---

## 1.4 Articulation avec le Référent Handicap de l'Entreprise

### 1.4.1 La Mission Handicap EDF

EDF dispose d'une **Mission Handicap** dédiée, incarnation de son engagement depuis la signature du premier Accord relatif à l'emploi des personnes handicapées en 2002. Cette mission couvre 4 axes principaux :

| Axe | Actions |
|---|---|
| **Recrutement & intégration** | Partenariats avec AGEFIPH, Cap Emploi, ESAT · Stages et alternances dédiés |
| **Maintien dans l'emploi** | Aménagements de poste · Reconversions professionnelles · Reclassements |
| **Sensibilisation & formation** | SEEPH (Semaine Européenne pour l'Emploi des Personnes Handicapées) · Formations managers |
| **Sous-traitance et achats** | Recours aux ESAT et EA dans les marchés publics EDF |

### 1.4.2 Processus d'Articulation Projet ↔ Mission Handicap

```
COLLABORATEUR           SCRUM MASTER          MISSION HANDICAP         RH EDF
(Besoin identifié)      (Djamel Chebbah)      (Référent entreprise)
      │                       │                       │                   │
      ▼                       │                       │                   │
Signal dans le          ◄─────┘                       │                   │
Daily standup           Entretien                     │                   │
(emoji 🆘 ou           individuel                     │                   │
message direct)         confidentiel                   │                   │
      │                  (< 48h)                       │                   │
      │                       │                       │                   │
      │                       ▼                       │                   │
      │               Identification               ◄──┘                   │
      │               du besoin                   Contact                 │
      │               d'aménagement               Mission Handicap        │
      │                       │                       │                   │
      │                       │                       ▼                   │
      │                       │               Évaluation                 │
      │                       │               du besoin +                │
      │                       │               plan d'action              │
      │                       │               personnalisé               │
      │                       │                       │                   │
      │                       ▼                       ▼                   │
      └───────────────► Mise en œuvre         Documentation              │
                        des aménagements      RQTH / MDPH ──────────────►│
                        dans le projet        si nécessaire    Validation RH
```

### 1.4.3 Coordonnées et Ressources

| Ressource | Rôle | Contact type |
|---|---|---|
| **Mission Handicap EDF** | Conseil, aménagement, financement | missionhandicap@edf.fr |
| **Référent Handicap RH site** | Accompagnement administratif (RQTH, MDPH) | DRH du site concerné |
| **Médecin du Travail** | Préconisations médicales d'aménagement | Via service de santé au travail EDF |
| **AGEFIPH** | Financement des aménagements de poste | www.agefiph.fr |
| **Cap Emploi** | Recrutement et maintien dans l'emploi des RQTH | Cap Emploi local |

### 1.4.4 Confidentialité et Non-Discrimination

**Principes non négociables :**
1. **Confidentialité absolue** : la nature du handicap d'un collaborateur n'est jamais divulguée sans son accord explicite. Seuls les aménagements nécessaires sont communiqués à l'équipe, pas le diagnostic.
2. **Déclaration volontaire** : aucun membre de l'équipe n'est obligé de déclarer son handicap. Les aménagements sont proposés à tous sans justification médicale obligatoire.
3. **Non-discrimination active** : toute remarque discriminatoire (intentionnelle ou non) est traitée immédiatement par le SM lors de la rétrospective ou en bilatéral.
4. **Principe d'aménagement raisonnable** : EDF est légalement tenu de mettre en œuvre tout aménagement raisonnable permettant à la personne d'exercer son activité, sauf contrainte disproportionnée.

---

# 2. Communication Interculturelle & Prévention des Conflits

> **Responsable de cette partie (Bloc 4) : Paul-Henri Dourneau** – Communication, inclusion & slides

---

## 2.1 Contexte : EDF et ses Acteurs Internationaux

### 2.1.1 La R&D Mondiale d'EDF : 9 Centres sur 4 Continents

EDF Group dispose de l'une des R&D les plus importantes du secteur énergétique mondial, répartie sur **9 centres** situés en France, en Chine, au Royaume-Uni, aux États-Unis, en Allemagne, en Italie, en Belgique, en Pologne et en Inde. Le projet de prédiction de consommation électrique est conçu pour être **déployable dans tous ces contextes**, ce qui impose une gouvernance interculturelle rigoureuse.

```
                    ┌──────────────────────────────────────────┐
                    │          CENTRES R&D EDF MONDIAUX        │
                    └──────────────────────────────────────────┘
                                        │
          ┌─────────────┬───────────────┼───────────────┬─────────────┐
          │             │               │               │             │
    🇫🇷 France      🇬🇧 Royaume-Uni  🇨🇳 Chine      🇺🇸 États-Unis  🇩🇪 Allemagne
   Clamart/Saclay   Leatherhead      Wuhan           Menlo Park      Aachen
   CET UTC+1/+2    GMT UTC+0/+1    CST UTC+8       EST UTC-5/-4    CET UTC+1/+2
                    │               │               │             │
               🇮🇹 Italie      🇧🇪 Belgique    🇵🇱 Pologne    🇮🇳 Inde
                  Milan          Bruxelles       Varsovie      Mumbai
               CET UTC+1/+2   CET UTC+1/+2   CET UTC+1/+2  IST UTC+5:30
```

**Défi horaire maximal :** Entre la France (CET, UTC+1) et la Chine (CST, UTC+8), il existe un **décalage de 7 heures**. Une réunion à 15h Paris = 22h Pékin. Entre la France et New York (EST, UTC-5), le décalage est de **6 heures** : 15h Paris = 9h New York.

### 2.1.2 Diversité Culturelle et Dimensions de Hofstede

Le modèle de **Geert Hofstede** (6 dimensions culturelles) permet d'anticiper les sources potentielles de friction dans les équipes internationales EDF. Le tableau ci-dessous compare les profils culturels des principaux pays impliqués :

| Dimension Hofstede | France 🇫🇷 | Chine 🇨🇳 | Royaume-Uni 🇬🇧 | États-Unis 🇺🇸 | Allemagne 🇩🇪 | Impact sur le projet |
|---|:---:|:---:|:---:|:---:|:---:|---|
| **Distance hiérarchique** | Haute (68) | Très haute (80) | Faible (35) | Faible (40) | Faible (35) | FR/CN : attendent validation hiérarchique · US/DE/UK : autonomie décisionnelle |
| **Individualisme** | Haute (71) | Faible (20) | Très haute (89) | Très haute (91) | Haute (67) | CN : décisions collectives · US/UK : initiative individuelle valorisée |
| **Masculinité (Compétition)** | Faible (43) | Haute (66) | Haute (66) | Haute (62) | Très haute (66) | DE/CN : valorisent performance et résultats · FR : valorise équilibre vie pro/perso |
| **Évitement de l'incertitude** | Haute (86) | Faible (30) | Faible (35) | Faible (46) | Très haute (65) | FR/DE : besoin de processus définis · CN/US/UK : à l'aise avec l'ambiguïté |
| **Orientation long terme** | Faible (63) | Très haute (87) | Faible (51) | Faible (26) | Haute (83) | CN/DE : investissement dans la durée · US/UK : résultats rapides attendus |

---

## 2.2 Modes de Communication Adaptés aux Cultures, Langues et Fuseaux Horaires

### 2.2.1 La Règle d'Or : « Asynchrone par Défaut »

Le principe fondateur de la gouvernance interculturelle du projet est l'**Async-First** (asynchrone d'abord) :

```
PARADIGME SYNCHRONE (ancien)     PARADIGME ASYNC-FIRST (adopté)
──────────────────────────────    ────────────────────────────────────────
"Réunissons-nous pour décider."   "Décidons par écrit, réunissons-nous
                                   pour valider et créer du lien."

Réunion = moyen de travail        Réunion = outil de célébration,
principal                         débloquage et renforcement d'équipe

Communication instantanée         Communication documentée
attendue                          et horodatée

Dépend du fuseau horaire          Indépendant du fuseau horaire
```

**Les 3 catégories de communication et leurs règles :**

| Catégorie | Canal | Délai de réponse attendu | Exemples |
|---|---|:---:|---|
| **Urgent (P1)** | Téléphone / Appel direct Teams | < 30 min | Incident production critique · Blocage total |
| **Rapide (P2)** | Slack/Teams – mention @prénom | < 4 heures | Question technique · Validation d'un PR · Bloqueur |
| **Normal (P3)** | Slack/Teams – canal thématique | < 24 heures | Discussion technique · Feedback documentation · Idée |
| **Non urgent (P4)** | Email / Confluence | < 48 heures | Rapport hebdo · Partage de ressource · Question ouverte |

### 2.2.2 Politique Linguistique du Projet

| Contexte | Langue | Justification |
|---|---|---|
| **Documentation technique** (code, API, README, Runbook) | 🇬🇧 **Anglais technique** | Standard international · Lisible par les 9 centres R&D · Compatible outils (GitHub, Jira) |
| **Réunions avec participants non-francophones** | 🇬🇧 **Anglais** | Langue commune de travail à EDF Group |
| **Réunions internes à l'équipe française** | 🇫🇷 **Français** | Efficacité et fluidité · Résumé en anglais ensuite |
| **Slack/Teams (canaux techniques)** | 🇬🇧 **Anglais** | Cohérence avec la documentation |
| **Slack/Teams (canal #general / bien-être)** | 🇫🇷 / 🇬🇧 **Bilingue** | Inclusivité sociale |
| **Messages d'alerte système (Grafana, CI/CD)** | 🇬🇧 **Anglais** | Standard MLOps international |

**Règles de rédaction pour l'anglais technique :**
- Phrases **courtes** (< 20 mots) et structure Sujet-Verbe-Objet.
- Pas d'idiomes ou d'expressions culturellement spécifiques (ex: "let's table this" = sens opposé UK/USA).
- Utilisation du **Plain English** : préférer "use" à "utilize", "start" à "commence".
- Disponibilité de **LanguageTool** pour la vérification orthographique et grammaticale (extension VS Code et Slack).

### 2.2.3 Gestion des Fuseaux Horaires

#### Fenêtres de Communication Universelles

```
FUSEAU    │  8h  9h  10h 11h 12h 13h 14h 15h 16h 17h 18h 19h 20h 21h 22h
──────────┼───────────────────────────────────────────────────────────────
🇨🇳 Pékin │                                    ████████████
          │                               ─────── Raisonnable ─────────
🇩🇪🇫🇷 EU  │              ████████████████████████████████████████
          │                          ══════════ CORE HOURS ══════════
🇬🇧 London│             ████████████████████████████████████
🇮🇳 Mumbai│                  ████████████████████████████████████████
🇺🇸 NY    │  █████████                    ████████████████
          │ ─ Tôt ─────────────────────────────────────────────
          │
          └─────── ZONE COMMUNE ──────────────► 14h00-16h00 (CET) ✅
```

**Règles de planification des réunions :**
1. **Fenêtre prioritaire :** 14h00 – 16h00 CET pour tout comité avec participants non-européens.
2. **Rotation équitable :** Si la fenêtre idéale est impossible, alterner les horaires inconfortables entre les équipes (pas toujours les mêmes personnes qui se lèvent tôt ou restent tard).
3. **Maximum 2 réunions synchrones internationales par semaine** par membre.
4. **Calendrier partagé** : tous les membres maintiennent leur calendrier à jour (Google Calendar / Outlook) avec indication des disponibilités.

**Outil recommandé : World Time Buddy** – Visualisation des fuseaux horaires pour la planification des réunions multilocalisées.

---

## 2.3 Exemples de Malentendus Multiculturels et Stratégies de Prévention

### 2.3.1 Les 8 Malentendus les Plus Fréquents en Contexte EDF

#### Malentendu 1 – Le « Oui » qui ne signifie pas « Je suis d'accord »

| Attribut | Détail |
|---|---|
| **Cultures concernées** | Chine 🇨🇳, Japon, Inde 🇮🇳 (cultures à haute contexte) |
| **Situation typique** | Un collègue pékinois répond « Yes, I understand » lors d'une revue de sprint. L'équipe française interprète cela comme une validation du plan. Lors de la livraison, la tâche n'a pas été réalisée comme prévu. |
| **Cause culturelle** | Dans les cultures asiatiques, « yes » signifie souvent « J'ai entendu ce que tu dis » et non « Je suis d'accord et je vais le faire ». Le refus ou le désaccord direct est considéré comme impoli. |
| **Stratégie de prévention** | ① Reformulation systématique : *"Could you confirm in your own words what you'll do by Friday?"* · ② Utilisation d'un **compte-rendu écrit** partagé après chaque décision · ③ Critères d'acceptation écrits dans Jira (pas de validation orale exclusive) |

---

#### Malentendu 2 – La Critique Directe Perçue comme Attaque Personnelle

| Attribut | Détail |
|---|---|
| **Cultures concernées** | Chine 🇨🇳, France 🇫🇷 (dans certains contextes hiérarchiques) |
| **Situation typique** | Un ingénieur allemand (DE) commente lors d'une code review : *"This code is wrong. Rewrite it."* Le collaborateur chinois (CN) se sent humilié publiquement devant l'équipe et se ferme à toute communication future. |
| **Cause culturelle** | Les cultures germaniques et américaines valorisent le feedback **direct et factuel** (Low-context). Les cultures asiatiques et françaises hiérarchiques le perçoivent parfois comme une attaque **personnelle** (High-context). |
| **Stratégie de prévention** | ① **Sandwich de feedback** : Positif → Amélioration → Positif · ② Feedback **en privé** pour les points sensibles (jamais en réunion publique) · ③ Formation de l'équipe au **modèle DESC** (Décrire · Exprimer · Spécifier · Conséquences) · ④ Charte de code review bienveillante |

---

#### Malentendu 3 – La Ponctualité et le Rapport au Temps

| Attribut | Détail |
|---|---|
| **Cultures concernées** | France 🇫🇷 / Chine 🇨🇳 (cultures « polychroniques ») vs Allemagne 🇩🇪 / Royaume-Uni 🇬🇧 (cultures « monochroniques ») |
| **Situation typique** | La réunion est programmée à 14h00. Les participants français rejoignent à 14h05 après les salutations habituelles. L'ingénieur allemand a déjà commencé sans attendre, générant de la frustration. |
| **Cause culturelle** | Les cultures monochroniques (DE, UK, Scandinavie) considèrent le retard comme un manque de respect. Les cultures polychroniques (FR, IT, ES, CN) admettent 5-10 min de souplesse pour les interactions sociales. |
| **Stratégie de prévention** | ① **Norme explicite** : *"La réunion commence et se termine à l'heure dans notre équipe – 14h00 = 14h00"* · ② L'animateur démarre et clôture à l'heure sans attendre · ③ **Buffer de 5 min** pour les questions informelles avant le début officiel (Teams ouvert 5 min en avance) |

---

#### Malentendu 4 – Hiérarchie et Prise de Parole

| Attribut | Détail |
|---|---|
| **Cultures concernées** | Chine 🇨🇳, Inde 🇮🇳, France 🇫🇷 (cultures à forte distance hiérarchique) |
| **Situation typique** | Lors d'un Sprint Planning, le PO (Noé) demande l'avis de tous les membres. Les collègues chinois ne proposent aucun commentaire tant que le manager n'a pas exprimé sa propre opinion. L'équipe conclut à tort que tout le monde est d'accord. |
| **Cause culturelle** | Dans les cultures à forte distance hiérarchique, critiquer ou contredire une proposition du supérieur est perçu comme de l'insolence. Le silence = déférence, pas accord. |
| **Stratégie de prévention** | ① **Tour de table obligatoire** lors des cérémonies Scrum : chaque membre s'exprime · ② Utilisation de **votes anonymes** (Mentimeter, Miro dots) pour les décisions sensibles · ③ Questions ouvertes directes à chaque membre : *"Thuy-Trang, what do you think about this approach?"* · ④ **Écriture avant partage** : chaque membre note son avis sur Miro avant la discussion orale |

---

#### Malentendu 5 – La Gestion du Désaccord Technique

| Attribut | Détail |
|---|---|
| **Cultures concernées** | France 🇫🇷 (culture du débat) vs Chine 🇨🇳 / Japon (culture du consensus) |
| **Situation typique** | Un ingénieur français plaide vigoureusement pour l'utilisation de Kubernetes plutôt que Docker Compose lors d'un COTECH. Son collègue chinois reste silencieux. La décision est prise. Deux semaines plus tard, le collègue chinois soulève que Docker Compose aurait été plus adapté. |
| **Cause culturelle** | La culture française valorise le débat contradictoire comme mode normal de validation des idées. La culture chinoise préfère chercher le consensus en amont et ne pas s'opposer frontalement en réunion. |
| **Stratégie de prévention** | ① **Délai de réflexion** : les décisions architecturales sont documentées dans un ticket Jira et laissées ouvertes 24h pour commentaires asynchrones · ② **Désaccord nommé comme vertu** : *"Nous voulons entendre les désaccords – ils nous rendent meilleurs"* · ③ Règle des **2 opinions minimales** avant toute décision technique majeure |

---

#### Malentendu 6 – Le Sens de l'Humour et de l'Ironie

| Attribut | Détail |
|---|---|
| **Cultures concernées** | Royaume-Uni 🇬🇧 (ironie, understatement) vs Chine 🇨🇳 / Allemagne 🇩🇪 |
| **Situation typique** | Un collègue britannique commente un code avec un PR trop complexe : *"Well, this is certainly... creative."* Le collègue allemand prend le commentaire au premier degré comme un compliment. |
| **Cause culturelle** | L'humour britannique (understatement, ironie) est opaque pour les cultures qui communiquent directement. |
| **Stratégie de prévention** | ① **Éviter l'ironie** dans toute communication écrite professionnelle · ② Si humour = l'indiquer explicitement avec 😄 · ③ Charte de communication : *"No sarcasm in written communications"* |

---

#### Malentendu 7 – La Perception de la Performance et des Délais

| Attribut | Détail |
|---|---|
| **Cultures concernées** | États-Unis 🇺🇸 / Allemagne 🇩🇪 (orientation court terme, résultats) vs France 🇫🇷 (qualité sur vitesse) |
| **Situation typique** | L'équipe américaine pousse pour livrer l'API au Jalon J3 « même si ce n'est pas parfait ». L'équipe française résiste, voulant valider tous les tests de charge avant la mise en production. |
| **Cause culturelle** | Le pragmatisme américain (« Done is better than perfect ») s'oppose au perfectionnisme français (goût pour la rigueur et la complétude). |
| **Stratégie de prévention** | ① **DoD explicite** : la Definition of Done précise objectivement ce que signifie "terminé" · ② Distinction explicite entre **MVP (livrable minimal validé)** et **version finale** dans le backlog · ③ Critères Go/No-Go documentés pour chaque jalon |

---

#### Malentendu 8 – L'Invitation à Discuter Perçue comme une Critique

| Attribut | Détail |
|---|---|
| **Cultures concernées** | France 🇫🇷 (débat = richesse) vs Royaume-Uni 🇬🇧 (politesse indirecte) |
| **Situation typique** | Un manager français demande à son collègue britannique de « challenger » son architecture. Le collègue britannique répond poliment *"It's a very interesting approach"* sans donner de critique substantielle, par politesse. Le manager français pensait avoir reçu une validation alors que le collègue avait des réserves. |
| **Stratégie de prévention** | ① Formuler les demandes de feedback **précisément** : *"What are the 3 risks you see in this architecture?"* plutôt que *"What do you think?"* · ② Formulaire de feedback structuré en asynchrone (Confluence/Jira) |

---

### 2.3.2 Protocole de Prévention des Conflits

```
SIGNAL D'ALERTE               NIVEAU          RÉPONSE
────────────────────          ─────────────   ─────────────────────────────
Tension dans un message       L1 – Latent     SM lit entre les lignes →
écrit (formulation brusque,                   message privé bienveillant
absence de réponse)                           dans les 4h

Conflit exprimé lors          L2 – Émergent   SM organise un appel
d'une réunion (voix,                          de médiation bilatéral
ton, interruption)                            dans les 24h

Blocage de travail            L3 – Ouvert     PO + SM → réunion de
(refus de collaborer,                         résolution · si nécessaire
non-livraison répétée)                        escalade RH / Manager

Conflit interpersonnel        L4 – Crise      Escalade RH EDF · Mission
grave ou discrimination                       Handicap si lié au handicap ·
                                              Protocole légal si nécessaire
```

**La Rétrospective Prime Directive (Norman Kerth) :**
> *« Indépendamment de ce que nous découvrons, nous comprenons et croyons sincèrement que chacun a fait du mieux possible, compte tenu de ce qu'il savait alors, de ses compétences et capacités, des ressources disponibles et de la situation du moment. »*

Cette directive est lue à voix haute au début de **chaque rétrospective** pour établir un espace de sécurité psychologique.

---

## 2.4 Solutions Innovantes pour Favoriser les Interactions

### 2.4.1 Rituels d'Équipe

| Rituel | Fréquence | Format | Objectif |
|---|---|---|---|
| **🌍 Cultural Moment** | Hebdomadaire (lundi) | 5 min en réunion ou post Slack | Un membre partage une curiosité culturelle ou professionnelle de son pays · Renforcé le lien humain |
| **🎉 Sprint Kudos** | Fin de chaque sprint | Post Slack `#kudos` | Remerciements publics entre membres · Format : *"@[Prénom] Kudos pour [contribution spécifique] !"* |
| **☕ Virtual Coffee** | Bi-hebdomadaire (optionnel) | 20 min Zoom informel | Conversation non professionnelle · 2 membres tirés au sort · Rotation mensuelle |
| **🎯 Tech Spotlight** | Mensuel | 15 min en COTECH | Un membre présente une technologie, un outil ou un article qu'il a découvert · Partage de connaissances |
| **🔄 Pair-programming** | Par sprint (1-2 sessions) | 1h en partage d'écran | 2 membres de profils complémentaires codent ensemble · Transfert de compétences + lien d'équipe |

### 2.4.2 Binômes Mixtes (Cross-Cultural Pairs)

Le principe des **binômes mixtes** (buddy system) consiste à apparier des membres de cultures ou de spécialités différentes pour renforcer la cohésion et prévenir les silos.

| Binôme | Profils | Objectif du binôme |
|---|---|---|
| **Thuy-Trang × Paul-Henri** | IA/Data + Data Engineering | Cohérence entre les modèles et le pipeline de données · Revue croisée des features |
| **Djamel × Dorian** | MLOps/Deploy + Monitoring/Maintenance | Continuité entre le déploiement et la maintenabilité · Handover sans perte |
| **Noé × Djamel** | Coordination + Agilité | Alignement PO-SM · Priorisation du backlog cohérente |
| **Thuy-Trang × Dorian** | Modèles + Tests de performance | Validation croisée des métriques et des tests de charge |

**Format du binôme :**
- Réunion de 30 min par sprint (synchrone ou asynchrone).
- Compte-rendu partagé dans Jira sous le ticket de la US concernée.
- Rotation des binômes tous les 2 sprints pour maximiser le transfert de connaissances.

### 2.4.3 Outils Collaboratifs Innovants

| Outil | Usage dans le projet | Valeur ajoutée inclusive |
|---|---|---|
| **Miro** | Brainstorming · Rétrospectives · Story Mapping | Interface visuelle accessible · Sticky notes = adaptées aux neurodivergents · Pas de prise de parole imposée |
| **Mentimeter** | Votes anonymes · Quiz interactifs · Sondages rapides | Anonymat = libère la parole des cultures hiérarchiques · Pas de pression de groupe |
| **Goblin.tools** | Décomposition de tâches complexes en sous-étapes | Spécialement conçu pour TDAH et TSA · Réduit la surcharge cognitive |
| **Otter.ai** | Transcription automatique des réunions | Sous-titrage pour malentendants · Archive pour fuseaux décalés |
| **Krisp** | Suppression du bruit lors des appels | Améliore la clarté pour les malentendants · Réduit la fatigue auditive |
| **World Time Buddy** | Planification de réunions multilocalisées | Visualisation instantanée des fuseaux · Évite les erreurs de planification |
| **LanguageTool** | Vérification grammaticale FR/EN | Aide les non-natifs et les dys · Réduction des malentendus écrits |
| **Loom** | Vidéos asynchrones courtes (< 5 min) | Remplacement des réunions par des démos visuelles · Revisionnable · Sous-titres automatiques |

---

# 3. Processus de Communication Inclusif & Réunions à Distance

> **Responsable de cette partie (Bloc 4) : Paul-Henri Dourneau** – Communication, inclusion & slides

---

## 3.1 Processus de Communication : Daily, Weekly, Rétros, Comités

### 3.1.1 Vue d'Ensemble du Calendrier de Communication

```
LUNDI          MARDI          MERCREDI       JEUDI          VENDREDI
──────────────────────────────────────────────────────────────────────
☕ Virtual     📝 Daily        🔧 COTECH      📝 Daily       📊 Weekly
Coffee (opt.)  Async          Bi-hebdo       Async          Report +
               (Slack)        (14h-14h30)    (Slack)        Kudos
               9h-10h                        9h-10h         (Slack)
                              ──────────────────────────────
               📝 Daily                      📝 Daily       [Fin sprint]
               Async                         Async          Sprint Review
               (Slack)                       (Slack)        + Rétro
               9h-10h                        9h-10h         (14h-15h30)
──────────────────────────────────────────────────────────────────────
  Cadence HEBDOMADAIRE   │   Cadence PAR SPRINT   │   Cadence PAR JALON
  Cultural Moment (5')   │   Sprint Planning       │   COPRO (1h)
  Retrospective suivante │   Sprint Review (30')   │   COSTRAT (1h)
  planifiée               │   Rétrospective (30')  │   Go/No-Go Sponsor
```

### 3.1.2 Le Daily Asynchrone (Format Détaillé)

**Canal :** `#daily-standup` (Slack/Teams)  
**Fréquence :** Quotidienne · **Délai :** Avant 10h00 CET  
**Durée de rédaction estimée :** 3 à 5 minutes  

**Template officiel (bilingue FR/EN) :**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 Daily – [Prénom] – [Date] [Heure de votre fuseau]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ TERMINÉ / DONE:
→ [Lien Jira EDF-XXX] Description courte

🔄 EN COURS / IN PROGRESS:
→ [Lien Jira EDF-XXX] Description courte · Avancement : XX %

🚨 BLOQUEUR / BLOCKER (laisser vide si aucun):
→ Description du blocage
   🆘 Besoin de : @[Personne] avant [heure]

📊 HUMEUR / MOOD (optionnel):
→ 😊 Motivé(e) / 😐 Neutre / 😔 Fatigué(e) / 🆘 En difficulté
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Règles de fonctionnement du Daily Asynchrone :**
1. **Pas de jugement** : le daily n'est pas un reporting de performance, c'est un outil de coordination.
2. **Réponse aux bloqueurs dans les 4h** : si quelqu'un signale un bloqueur, un autre membre (ou le SM) doit répondre dans les 4h.
3. **Emoji 🆘 = priorité absolue** : le SM organise un appel individuel dans les 2h.
4. **Indicateur mood optionnel** : personne n'est obligé de partager son état émotionnel, mais cela permet au SM de détecter les signaux faibles de surcharge.
5. **Pas de résumé de travail passé > 3 lignes** : le daily est prospectif, pas un rapport d'activité.

### 3.1.3 Le Weekly Report

**Canal :** Email + message récapitulatif sur `#weekly-report` (Slack/Teams)  
**Fréquence :** Chaque vendredi, avant 17h00 CET  
**Rédacteur :** Scrum Master (Djamel Chebbah)  

**Contenu du Weekly Report :**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 WEEKLY REPORT – Projet EDF/RTE Predictor – Semaine XX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 AVANCEMENT SPRINT
Sprint [N] – J+X/J+7
SP livrés : XX / XX cibles
Burn-down : [✅ Sur cible / ⚠️ Légèrement en retard / 🔴 À risque]

✅ SUCCÈS DE LA SEMAINE
→ [Accomplissement 1]
→ [Accomplissement 2]

🚨 POINTS D'ATTENTION
→ [Bloqueur ou risque identifié]
   Action : [Mesure corrective]

📅 AGENDA SEMAINE PROCHAINE
→ [Cérémonie / Réunion prévue]
→ [US prioritaires à livrer]

💡 INDICATEUR TEAM
Énergie d'équipe : 😊😊😊😐😊 (moyenne : Bonne)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 3.1.4 La Rétrospective (Format Détaillé)

**Format :** Synchrone · **Durée :** 30 min · **Outil :** Miro (tableau collaboratif)  
**Participants :** Équipe uniquement (PO + SM + Devs) · Sans sponsor ni référent métier  
**Fréquence :** En fin de chaque sprint  

**Déroulement en 5 étapes :**

| Étape | Durée | Activité | Animateur |
|:---:|:---:|---|---|
| **1. Check-in** | 3 min | Question brise-glace légère (ex: *"En un mot, comment tu décris ce sprint ?"*) · Post-its Miro | SM |
| **2. Rappel Prime Directive** | 1 min | Lecture de la directive de Norman Kerth · Établissement du safe space | SM |
| **3. Collecte (Starfish)** | 10 min | Chaque membre écrit en silence ses post-its sur les 5 axes : Start · Stop · More · Less · Keep | Chacun |
| **4. Discussion** | 12 min | SM regroupe les post-its similaires · Vote par points (3 dots par personne) sur les actions prioritaires | SM + Équipe |
| **5. Plan d'action** | 4 min | Les 2-3 actions prioritaires sont formalisées dans Jira (US ou tâche technique) avec responsable et délai | SM + Équipe |

**Règles d'or de la Rétrospective :**
- **Règle de Vegas** : ce qui se dit en rétro reste en rétro (pas de citation sans accord).
- **Pas de nom dans les problèmes** : on parle de situations, pas de personnes.
- **Action = ticket Jira** : une action sans ticket Jira n'existe pas.
- **Suivi** : les actions du sprint N sont revues au début de la rétro du sprint N+1.

---

## 3.2 Mise en Place du Fil de Discussion (Règles de Fonctionnement)

### 3.2.1 Architecture des Canaux Slack/Teams

```
🏢 EDF-RTE-PREDICTOR (Workspace)
│
├── 📢 INFORMATIONS GÉNÉRALES
│   ├── #general              → Annonces importantes pour toute l'équipe
│   ├── #announcements        → Informations officielles (jalons, réunions)
│   └── #kudos                → Félicitations et remerciements publics
│
├── 🔧 TECHNIQUE
│   ├── #data-pipeline        → Discussion API ODRE, feature engineering, data quality
│   ├── #model-training       → IA, métriques, hyperparamètres, MLflow
│   ├── #mlops-k8s            → Docker, Kubernetes, CI/CD, déploiement GCP
│   ├── #monitoring-alerts    → Alertes Prometheus, Grafana, drift KS
│   └── #code-review          → Demandes de review PR, retours techniques
│
├── 📋 PROJET & AGILE
│   ├── #daily-standup        → Daily asynchrone quotidien
│   ├── #weekly-report        → Rapport hebdomadaire (vendredi)
│   ├── #sprint-backlog       → Discussions sur les US en cours
│   └── #kpi-board            → Publication des KPIs et métriques projet
│
├── 🌍 INTERNATIONAL & INCLUSION
│   ├── #cultural-moments     → Partages culturels hebdomadaires
│   ├── #virtual-coffee       → Organisation et liens des cafés virtuels
│   └── #accessibility        → Retours sur les outils et adaptations inclusives
│
└── 🚨 URGENCES
    └── #incidents            → Incidents production · P1/P2 uniquement
```

### 3.2.2 Règles de Fonctionnement des Canaux

#### Règles Universelles (tous les canaux)

| Règle | Description | Sanction |
|---|---|---|
| **Pas de @channel inutile** | La mention @channel notifie tous les membres. N'utiliser que pour les urgences P1. | SM rappelle la règle en bilatéral |
| **Fil de discussion (Thread)** | Toute réponse à un message se fait en thread (répondre dans le fil), pas dans le canal principal. | Réduction du bruit · SM réorganise si nécessaire |
| **Pas de "OK" seul** | Les messages d'une seule lettre encombrent le canal. Préférer une réaction emoji 👍 ou ✅. | Convention d'équipe |
| **Langue du canal** | Respecter la langue définie par canal (EN technique / FR social) | Rappel bienveillant par n'importe quel membre |
| **Délai de réponse** | Respecter les délais : P1 < 30min · P2 < 4h · P3 < 24h · P4 < 48h | Relance après délai passé |
| **Droit à la déconnexion** | Aucun message professionnel n'attend de réponse en dehors des heures de travail définies (9h-18h CET) | Règle formalisée dans le contrat d'équipe |

#### Règles Spécifiques par Canal

| Canal | Règle spécifique |
|---|---|
| `#daily-standup` | Template obligatoire · Pas de discussion dans le canal · Les bloqueurs déclenchent un thread séparé |
| `#incidents` | Format : `🚨 INCIDENT [P1/P2] – [Système] – [Description courte]` · Post initial puis updates toutes les 30 min |
| `#kudos` | Format : `🎉 Kudos @[Prénom] pour [contribution précise]` · Pas de réponse obligatoire (un 🙏 suffit) |
| `#code-review` | Lien PR obligatoire + contexte en 2 lignes · Délai de review : < 24h |
| `#cultural-moments` | Un membre par semaine (rotation) · 3-5 lignes max · Tolérance zéro pour les commentaires condescendants |

### 3.2.3 Contrat d'Équipe (Team Agreement)

Le contrat d'équipe est un document vivant, co-construit lors du Sprint 0 et révisable à chaque rétrospective.

```
╔════════════════════════════════════════════════════════════════╗
║              CONTRAT D'ÉQUIPE – PROJET EDF/RTE                 ║
║                     Version 1.2 – Juin 2026                    ║
╠════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  NOS VALEURS                                                    ║
║  ✦ Bienveillance · Transparence · Responsabilité · Courage     ║
║                                                                 ║
║  NOS ENGAGEMENTS                                                ║
║  1. Respecter les délais de réponse convenus (P1/P2/P3/P4)     ║
║  2. Utiliser le template du daily sans exception                ║
║  3. Signaler les bloqueurs dès qu'ils se présentent            ║
║  4. Ne pas fusionner de code sans code review approuvée         ║
║  5. Appliquer la DoD intégralement pour toute US               ║
║  6. Respecter les plages de déconnexion de chacun              ║
║  7. Lire la Prime Directive avant chaque rétrospective          ║
║                                                                 ║
║  NOS ENGAGEMENTS D'INCLUSION                                    ║
║  8. Aucun commentaire discriminatoire (direct ou indirect)      ║
║  9. Reformuler en anglais simple (pas de jargon, pas d'ironie) ║
║  10. Sous-titrage activé à chaque réunion internationale        ║
║  11. Compte-rendu écrit après toute décision                   ║
║  12. Signaler les besoins d'adaptation sans crainte             ║
║                                                                 ║
║  NOS RITUELS                                                    ║
║  13. Cultural Moment tous les lundis (rotation)                 ║
║  14. Sprint Kudos en fin de sprint                              ║
║  15. Virtual Coffee bi-hebdomadaire (optionnel)                 ║
║                                                                 ║
║  Signataires : Noé W. · Djamel C. · Paul-Henri D.              ║
║               Dorian M. · Thuy-Trang N.                        ╠
╚════════════════════════════════════════════════════════════════╝
```

---

## 3.3 Kit de Réunion à Distance

### 3.3.1 Structure Type d'une Réunion à Distance

Chaque réunion du projet, quelle que soit sa nature, suit une **structure en 5 temps** :

```
┌────────────────────────────────────────────────────────────────────┐
│           STRUCTURE TYPE D'UNE RÉUNION À DISTANCE                 │
│                                                                    │
│  ─────────────────────────────────────────────────────────────    │
│  ① PRÉ-RÉUNION                              [J-48h à J-24h]      │
│  ─────────────────────────────────────────────────────────────    │
│  • Ordre du jour partagé sur Confluence/Teams (format précis)     │
│  • Documents de travail mis à jour et accessibles                 │
│  • Rappel envoyé 1h avant via Teams/Slack                        │
│  • Sous-titrage activé par l'animateur avant ouverture           │
│  • Teams ouvert 5 min avant pour le social pre-meeting           │
│                                                                    │
│  ─────────────────────────────────────────────────────────────    │
│  ② OUVERTURE (5 % du temps)                 [2-3 min]            │
│  ─────────────────────────────────────────────────────────────    │
│  • Accueil de tous les participants (prénom + lieu si international│
│  • Rappel de l'objectif de la réunion et du livrable attendu     │
│  • Rappel des règles : caméra optionnelle · micro off par défaut  │
│  • Vérification du sous-titrage et de l'enregistrement            │
│  • Désignation d'un Scribe (compte-rendu en temps réel)          │
│                                                                    │
│  ─────────────────────────────────────────────────────────────    │
│  ③ CORPS DE RÉUNION (85 % du temps)                              │
│  ─────────────────────────────────────────────────────────────    │
│  • Traitement des points de l'ordre du jour (minuté)             │
│  • Tour de table pour les points décisionnels                    │
│  • Votes anonymes si nécessaire (Mentimeter)                     │
│  • Parking lot pour les sujets hors scope (pas de dérive)        │
│  • Pause de 5 min si durée > 45 min                              │
│                                                                    │
│  ─────────────────────────────────────────────────────────────    │
│  ④ CLÔTURE (5 % du temps)                  [2-3 min]            │
│  ─────────────────────────────────────────────────────────────    │
│  • Résumé des décisions prises (lecture par le Scribe)           │
│  • Actions identifiées : Quoi ? Qui ? Pour quand ?               │
│  • Prochain point planifié                                        │
│  • Satisfaction de réunion : 👍 / 😐 / 👎 (réaction rapide)     │
│                                                                    │
│  ─────────────────────────────────────────────────────────────    │
│  ⑤ POST-RÉUNION                             [< 2h après]         │
│  ─────────────────────────────────────────────────────────────    │
│  • Compte-rendu partagé sur Confluence + canal Slack (#general)  │
│  • Actions ajoutées dans Jira (avec assigné + deadline)          │
│  • Enregistrement vidéo disponible (lien dans le CR)             │
│  • Transcription automatique disponible (Otter.ai)               │
└────────────────────────────────────────────────────────────────────┘
```

### 3.3.2 Templates d'Ordre du Jour par Type de Réunion

#### Template Sprint Planning (1h00)

```
SPRINT PLANNING – Sprint [N]
Date : [JJ/MM/AAAA] · 14h00-15h00 CET
Animateur : Djamel Chebbah (SM)
Participants : Toute l'équipe

OBJECTIF : Définir le Sprint Backlog et l'objectif du Sprint [N]

[0:00-0:05]  Ouverture · Vérification des présences · Rappel des règles
[0:05-0:15]  Bilan Sprint N-1 : Vélocité · Points de vigilance
[0:15-0:35]  PARTIE 1 – LE QUOI : PO présente les US prioritaires
             → Clarification des critères d'acceptation
             → Sélection collective des US pour le sprint
[0:35-0:50]  PARTIE 2 – LE COMMENT : Découpage en sous-tâches + estimation
             → Planning Poker (Mentimeter / cartes physiques)
             → Définition de l'objectif du sprint
[0:50-0:55]  Validation de la capacité sprint (SP vs vélocité historique)
[0:55-1:00]  Actions post-planning · Clôture

LIVRABLE : Sprint Backlog créé dans Jira · Objectif sprint validé
```

#### Template Sprint Review (30-45 min)

```
SPRINT REVIEW – Sprint [N]
Date : [JJ/MM/AAAA] · 14h00-14h45 CET
Animateur : Djamel Chebbah (SM)
Participants : Équipe + PO + Référents Métier (Marc, Léa) + Sponsor (optionnel)

OBJECTIF : Démontrer les incréments livrés et recueillir le feedback

[0:00-0:05]  Accueil · Présentation du sprint (objectif, SP engagés, SP livrés)
[0:05-0:25]  DÉMONSTRATIONS EN LIVE (pas de slides statiques)
             → Chaque membre démo son incrément (5 min max chacun)
             → Questions des référents métier après chaque démo
[0:25-0:35]  Feedback Product Owner : US validées vs rejctées
[0:35-0:40]  Discussion : qu'est-ce qui change dans le Backlog ?
[0:40-0:45]  Prochain sprint : aperçu des US prioritaires · Clôture

LIVRABLE : US validées (DoD) · Backlog mis à jour · Compte-rendu partagé
```

#### Template Rétrospective (30 min)

```
RÉTROSPECTIVE – Sprint [N]
Date : [JJ/MM/AAAA] · 14h30-15h00 CET (après la Sprint Review)
Animateur : Djamel Chebbah (SM)
Participants : Équipe uniquement (sans sponsor/métier)
Outil : Miro (tableau Starfish prêt)

OBJECTIF : Améliorer continuellement nos pratiques de travail

[0:00-0:03]  Check-in : Chacun répond en un mot à "Comment décris-tu ce sprint ?"
[0:03-0:04]  Lecture de la Prime Directive de Norman Kerth
[0:04-0:14]  Collecte silencieuse (Miro) : chacun écrit ses post-its
             → START : Commencer à faire
             → STOP : Arrêter de faire
             → MORE : Faire davantage
             → LESS : Faire moins
             → KEEP : Continuer
[0:14-0:26]  Discussion et dot-vote (3 points par personne)
[0:26-0:30]  Plan d'action : 2-3 actions → tickets Jira + responsables

LIVRABLE : 2-3 actions formalisées dans Jira · Compte-rendu (résumé uniquement)
```

#### Template COPRO (Comité de Projet – 1h00)

```
COPRO – Semaine [N]
Date : Lundi · 14h00-15h00 CET
Animateur : Djamel Chebbah (SM)
Participants : Équipe + PO + Référents Métier + Sponsor

[0:00-0:05]  Ouverture · Rappel des règles · Vérification sous-titrage
[0:05-0:15]  Tableau de bord KPIs (Burn-down, MAPE, uptime, budget)
[0:15-0:30]  Points d'avancement par lot : Data · IA · MLOps · Docs
[0:30-0:40]  Risques et bloqueurs : statut + plan de mitigation
[0:40-0:50]  Décisions à prendre (Go/No-Go, arbitrages, ressources)
[0:50-0:55]  Points divers + Parking lot
[0:55-1:00]  Résumé décisions · Actions Jira · Prochain COPRO · Clôture

LIVRABLE : Compte-rendu Teams + Jira · Tableau KPIs mis à jour
```

---

### 3.3.3 Bonnes Pratiques pour Garder la Dynamique de Groupe

#### Avant la réunion

| Pratique | Description |
|---|---|
| **Ordre du jour envoyé à l'avance** | 24h à 48h avant · Format structuré avec minutage · Documents pré-lus |
| **Préparation active** | Un "devoir de réunion" peut être demandé : *"Venez avec 1 idée d'amélioration pour le monitoring"* |
| **Test technique** | L'animateur teste la salle virtuelle 10 min avant (son, vidéo, sous-titrage, partage d'écran) |
| **Liste des participants** | Confirmée la veille · Jamais plus de **8 participants** (au-delà → scinder en groupes) |

#### Pendant la réunion

| Pratique | Description |
|---|---|
| **Timekeeper** | Un membre (différent de l'animateur) chronomètre chaque point et alerte à -2 min | 
| **Parking Lot** | Tableau virtuel Miro pour noter les sujets hors scope → traités en fin de réunion ou en asynchrone |
| **Tour de table structuré** | Pour les points décisionnels : chaque membre s'exprime brièvement avant la discussion ouverte |
| **Popcorn** | Alternative au tour de table : chaque personne qui finit de parler désigne la suivante → évite les monopoles de parole |
| **Silence actif** | Après une question complexe, 60 secondes de réflexion silencieuse + écriture sur Miro avant la discussion |
| **Check-out émotionnel** | En fin de réunion : *"En un emoji, comment tu te sens ?"* → jauge rapide de l'énergie d'équipe |
| **Règle de la caméra** | Caméra **optionnelle** (pas d'obligation pour inclusion des handicaps) · Fond neutre virtuel disponible |
| **Enregistrement annoncé** | L'enregistrement est annoncé en début de réunion · Accord de tous requis |

#### Après la réunion

| Pratique | Description |
|---|---|
| **Compte-rendu en 2h** | Scribe publie le CR sur Confluence + résumé sur Slack dans les 2h · Format : Décisions + Actions + Parking lot |
| **Feedback sur la réunion** | Sondage rapide (3 questions, 30 secondes) : *"La réunion était-elle utile ? Bien organisée ? Avez-vous pu vous exprimer ?"* |
| **Suivi des actions** | Actions du CR importées dans Jira le jour même · Vérification lors du daily suivant |

---

### 3.3.4 Outils Interactifs Utilisés dans les Réunions

| Outil | Usage | Moment d'utilisation | Lien avec l'inclusion |
|---|---|---|---|
| **Mentimeter** | Votes anonymes · Word clouds · Quiz | Sprint Planning (Planning Poker) · COPRO (sondages) | Anonymat libère la parole des cultures hiérarchiques |
| **Miro** | Rétrospectives · Brainstorming · Architecture · User Story Mapping | Rétros · Sprint Planning · COTECH | Espace visuel · Inclusif pour les profils visuels et les non-natifs |
| **Teams Live Captions** | Sous-titrage en temps réel (FR, EN, ZH, DE, IT…) | Toutes les réunions internationales | Inclusion des malentendants et des non-natifs |
| **Otter.ai / Teams Transcript** | Transcription et résumé automatique post-réunion | Toutes les réunions > 15 min | Archive asynchrone · Fuseaux horaires différents |
| **Jamboard / Miro (Post-its)** | Collecte silencieuse d'idées | Rétrospectives · Brainstorming | Égalité de parole · Évite l'effet "premier qui parle" |
| **Loom** | Démos vidéo asynchrones (< 5 min) | En remplacement de présentations synchrones | Revisionnable · Sous-titres auto · Respecte les fuseaux |
| **Breakout Rooms** (Teams/Zoom) | Travail en sous-groupes de 2-3 personnes | Sprint Planning (estimation) · Rétrospectives | Espace plus confortable pour les personnes timides ou introvertis |
| **Sli.do / Slido** | Questions anonymes pendant une présentation | COSTRAT · Formations | Anonymat pour les cultures hiérarchiques |

---

### 3.3.5 Protocole de Réunion Accessible – Checklist Animateur

Avant chaque réunion à distance, l'animateur valide la checklist suivante :

```
CHECKLIST ANIMATEUR – RÉUNION ACCESSIBLE À DISTANCE
══════════════════════════════════════════════════════════════
PRÉ-RÉUNION (J-24h)
□ Ordre du jour envoyé avec minutage précis
□ Documents pré-lus partagés (lien + format accessible)
□ Invitation avec lien direct Teams/Zoom (pas de numéro de réunion seul)
□ Fuseau horaire précisé dans l'invitation (ex: 14h00 CET / 13h00 GMT / 20h00 CST)

TECHNIQUE (J-0, 10 min avant)
□ Test micro + son + partage d'écran
□ Sous-titrage Live Captions activé
□ Enregistrement configuré (avec accord participants)
□ Fond virtuel neutre activé (disponible pour tous)
□ Scribe désigné et prêt

INCLUSION (pendant)
□ Accueil nominatif de chaque participant
□ Caméra optionnelle rappelée
□ Mode "lever la main" (Teams) activé pour demander la parole
□ Polling/vote anonyme configuré (Mentimeter) pour les décisions
□ Parking lot créé sur Miro
□ Pause de 5 min planifiée si > 45 min

POST-RÉUNION (< 2h)
□ Compte-rendu publié sur Confluence + résumé Slack
□ Actions importées dans Jira (responsable + deadline)
□ Lien enregistrement partagé dans le canal dédié
══════════════════════════════════════════════════════════════
```

---

## Conclusion

Ce plan d'inclusion, de communication et de collaboration d'équipe formalise l'engagement de l'équipe EDF/RTE Predictor en faveur d'un environnement de travail **universel, accessible et respectueux** de la diversité humaine dans toutes ses dimensions.

### Synthèse des Engagements

| Dimension | Engagement principal | Outil / Mesure clé |
|---|---|---|
| **Inclusion visuelle** | Palette ColorBrewer · Contraste WCAG 4,5:1 | Coblis · Colour Contrast Analyser |
| **Inclusion auditive** | Sous-titrage systématique · Transcription automatique | Teams Live Captions · Otter.ai |
| **Inclusion cognitive** | Tâches ≤ 4h · Documentation simplifiée | Goblin.tools · Template Miro |
| **Inclusion motrice** | Navigation clavier · Dictée vocale disponible | WCAG 2.1 – Critère 2.1.1 |
| **Communication interculturelle** | Async-First · Anglais simple · Fenêtre 14h-16h CET | Règle culturelle d'équipe |
| **Prévention des conflits** | Protocole L1-L4 · Prime Directive Rétrospective | Rétrospective Starfish · SM référent |
| **Dynamique de groupe** | Rituels hebdomadaires · Binômes mixtes · Kudos | Cultural Moment · Virtual Coffee |
| **Réunions à distance** | Structure en 5 temps · Checklist animateur | Mentimeter · Miro · Loom |

### Responsabilités Finales

| Membre | Contribution principale à ce document |
|---|---|
| **Paul-Henri Dourneau** | Rédaction principale · Inclusion · Communication interculturelle · Kit réunion |
| **Noé Wibaut** | Processus communication · Rituels d'équipe · Coordination générale |
| **Djamel Chebbah** | Canaux Slack/Teams · Contrat d'équipe · Protocole incidents |
| **Dorian Marty** | Outils interactifs · Accessibilité technique (Grafana, Prometheus) |
| **Thuy-Trang Nguyen** | Personas · Cas d'usage interculturels · Maquettes inclusives |

---

*Document rédigé dans le cadre de la MSPR TPRE932 & TPRE942 – Référentiel RNCP36582 – Promotion 2025-2026.*  
*Date de rédaction : Juin 2026*
