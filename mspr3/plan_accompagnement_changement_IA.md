# Plan d'Accompagnement du Changement & de Bonne Utilisation de l'IA
## Solution de Prédiction de Consommation Électrique Nationale — EDF / RTE
### MSPR TPRE932 & TPRE942 — CDPIA 2025-2026

---

> [!IMPORTANT]
> Ce document constitue le **Livrable 3** du projet MSPR. Il s'adresse à la fois aux équipes techniques (Data Science, MLOps) et aux équipes métier (dispatchers RTE, planificateurs EDF, management). Son objectif est de garantir que l'outil IA est utilisé correctement, de façon responsable, et que son intégration dans les pratiques de travail est réussie sur le long terme.

---

## Table des Matières

1. [Analyse d'Impact du Déploiement IA](#1-analyse-dimpact-du-déploiement-ia)
   - 1.1 Cartographie des parties prenantes
   - 1.2 Impact sur les métiers et les processus
   - 1.3 Risques humains et organisationnels
   - 1.4 Matrice d'impact global
2. [Stratégie d'Accompagnement du Changement](#2-stratégie-daccompagnement-du-changement)
   - 2.1 Vision & objectifs du changement
   - 2.2 Plan en 4 phases
   - 2.3 Plan de communication
   - 2.4 Plan de formation
3. [Kit de Bonne Utilisation de l'IA](#3-kit-de-bonne-utilisation-de-lia)
   - 3.1 Guide "Comment utiliser les prédictions ?"
   - 3.2 Fiche de référence rapide (Aide-mémoire)
   - 3.3 Check-list d'utilisation responsable
4. [Outils Lean & Amélioration Continue](#4-outils-lean--amélioration-continue)
   - 4.1 Formulaire de feedback utilisateur
   - 4.2 Template A3 d'amélioration continue
   - 4.3 Tableau Kanban des retours d'usage
   - 4.4 Procédure de traitement des incidents d'usage
5. [Indicateurs de Maturité d'Adoption (KPIs Humains)](#5-indicateurs-de-maturité-dadoption-kpis-humains)
6. [Références Croisées](#6-références-croisées)

---

## 1. Analyse d'Impact du Déploiement IA

### 1.1 Cartographie des Parties Prenantes

```
                    ┌─────────────────────────────────────────┐
                    │        SOLUTION IA RTE/EDF               │
                    │  Prédiction Consommation Électrique       │
                    └────────────────┬────────────────────────┘
                                     │
          ┌──────────────────────────┼──────────────────────────┐
          │                          │                          │
          ▼                          ▼                          ▼
┌─────────────────┐      ┌─────────────────────┐    ┌─────────────────────┐
│ UTILISATEURS    │      │ ÉQUIPES SUPPORTS     │    │ DÉCIDEURS           │
│ DIRECTS         │      │                     │    │                     │
│                 │      │ • Data Scientists    │    │ • Direction RTE     │
│ • Dispatchers   │      │ • Ingénieurs MLOps  │    │ • Direction EDF     │
│   RTE           │      │ • Équipe Ops/Infra  │    │ • Responsables SI   │
│ • Planificateurs│      │ • Support N1/N2/N3  │    │ • RSSI              │
│   production    │      │                     │    │ • DPO (RGPD)        │
│ • Analystes     │      │                     │    │                     │
│   énergie       │      │                     │    │                     │
└─────────────────┘      └─────────────────────┘    └─────────────────────┘
   Impact ÉLEVÉ              Impact MOYEN               Impact INDIRECT
   Résistance probable       Formation requise          Validation requise
```

#### Profils des Parties Prenantes Clés

| Partie prenante | Rôle actuel | Interaction avec l'IA | Niveau d'impact | Attitude prévisible |
|:---|:---|:---|:---:|:---:|
| **Dispatcher RTE** | Supervision en temps réel du réseau | Consulte les prédictions pour anticiper | ⬛⬛⬛⬛ Très élevé | Mitigée (crainte remplacement) |
| **Planificateur production** | Programme les tranches de production H+24/H+168 | Intègre les prédictions dans le planning | ⬛⬛⬛⬛ Très élevé | Positive (gain de temps) |
| **Data Scientist R&D** | Développe et améliore les modèles | Pilote le ré-entraînement et la qualité | ⬛⬛⬛ Élevé | Très positive (c'est leur outil) |
| **Ingénieur MLOps** | Opère l'infrastructure IA | Surveillance et maintenance | ⬛⬛⬛ Élevé | Positive (nouveau rôle valorisant) |
| **Manager équipe réseau** | Supervise les dispatchers | Valide l'adoption et les processus | ⬛⬛ Moyen | Prudente (responsabilité) |
| **Direction RTE/EDF** | Stratégie et investissements | Suivi des KPIs de valeur créée | ⬛ Faible | Positive (ROI attendu) |
| **DPO / Juridique** | Conformité RGPD et IA Act | Audit de conformité | ⬛⬛ Moyen | Neutre à méfiante |
| **Partenaires externes** | Météo France, ODRE | Fournisseurs de données | ⬛ Faible | Neutre |

---

### 1.2 Impact sur les Métiers et les Processus

#### A. Impact sur le Processus de Planification (H+24 / H+168)

**AVANT le déploiement IA :**
```
Dispatcher/Planificateur
    │
    ├── Consultation des données historiques manuellement (tableurs Excel)
    ├── Application de règles métier empiriques ("en janvier, +15% si < 0°C")
    ├── Consultation de la météo (site Météo France)
    ├── Appel téléphonique avec pairs pour validation croisée
    └── Saisie manuelle de la prévision dans le SCADA
    
Temps moyen : 45–90 minutes pour une prévision H+24
Précision typique : ±8–12% (expert humain seul)
```

**APRÈS le déploiement IA :**
```
Dispatcher/Planificateur
    │
    ├── Consultation de l'API /predict (< 1 seconde)
    │   → Prédiction : 58 432 MW ± ~3 142 MW (RMSE)
    ├── Vérification de cohérence avec le contexte (événements connus)
    ├── Ajustement humain si nécessaire (grève, sommet sportif, etc.)
    └── Saisie dans le SCADA avec traçabilité "assisté par IA"

Temps moyen : 5–15 minutes pour une prévision H+24
Précision IA seule : MAPE 4,68% (±5% dans 69% des cas)
Précision IA + expert : estimée à ±3–5% (meilleure pratique)
```

**Transformation du travail :**

| Tâche | Avant IA | Après IA | Évolution |
|:---|:---:|:---:|:---:|
| Collecte des données | 20–30 min | 0 min (automatisée) | ✅ Libération de temps |
| Calcul de la prévision | 15–30 min | < 1 s | ✅ Accélération x1000 |
| Validation de la prévision | 10–20 min | 5–10 min | ✅ Recentrage sur la valeur |
| Justification/traçabilité | Empirique | Documentée (model_used) | ✅ Auditabilité |
| Gestion des cas extrêmes | Expertise pure | Expertise + signal IA | ⚠️ Nécessite formation |

#### B. Impact sur le Processus de Supervision Temps Réel

L'IA introduit un **troisième niveau d'alerte** dans la supervision :

```
Niveau 1 (EXISTANT) : Mesures physiques des capteurs réseau (tension, fréquence)
Niveau 2 (EXISTANT) : Prévisions météorologiques Météo France
Niveau 3 (NOUVEAU)  : Prédiction IA de consommation (API /predict)
                      → Alerte si écart mesuré/prédit > 5% sur 30 minutes
```

#### C. Impact Organisationnel

| Dimension | Changement | Impact |
|:---|:---|:---:|
| **Compétences requises** | Nouvelles compétences : lecture des métriques IA, compréhension des limites | Moyen |
| **Hiérarchie décisionnelle** | La décision finale reste humaine, mais s'appuie sur un nouveau signal | Faible |
| **Processus documentaires** | Les rapports doivent mentionner si l'IA a été consultée | Moyen |
| **Responsabilité** | Qui est responsable si une prédiction IA mal utilisée cause une erreur ? | Élevé |
| **Culture de données** | Passage d'une culture empirique à une culture data-driven | Élevé |

---

### 1.3 Risques Humains et Organisationnels

#### Risque 1 — Sur-confiance dans les prédictions (Automation Bias)

```
Description : L'utilisateur fait trop confiance à la prédiction IA sans exercer
              son jugement critique. En cas d'erreur du modèle, la décision
              finale sera mauvaise car non questionnée.

Exemple concret : La prédiction indique 45 000 MW un lundi matin de janvier
                  alors que la consommation réelle sera probablement > 70 000 MW
                  (pic hivernal + retour des usines après les fêtes).
                  Le dispatcher qui suit aveuglément l'IA ne planifiera pas
                  suffisamment de capacité de production.

Probabilité  : Élevée (biais cognitif naturel)
Impact       : Critique (déséquilibre réseau électrique)
Mitigation   : Formation, check-list obligatoire, affichage systématique de
               l'intervalle d'incertitude du modèle
```

#### Risque 2 — Sous-confiance et Rejet (Technophobie)

```
Description : Certains utilisateurs, souvent les plus expérimentés, refusent
              d'utiliser l'outil par conviction que "mon expérience vaut mieux
              que l'IA" ou par crainte de déqualification.

Exemple concret : Un dispatcher avec 20 ans d'expérience continue de faire ses
                  prévisions comme avant, n'utilise jamais /predict, et ne remonte
                  pas les cas où l'IA aurait eu tort (feedback loop brisée).

Probabilité  : Moyenne
Impact       : Modéré (perte de valeur, données de feedback incomplètes)
Mitigation   : Implication des experts dans la conception, démonstration du
               complémentarité IA/humain (pas substitution)
```

#### Risque 3 — Déresponsabilisation ("C'est l'IA qui a dit")

```
Description : Face à une erreur de planification, un opérateur se décharge
              de sa responsabilité en arguant que "l'IA avait prédit X".

Impact légal et opérationnel : élevé dans un secteur aussi critique que
l'électricité nationale.

Mitigation   : Clause dans les procédures : "La prédiction IA est un outil
               d'aide à la décision. La responsabilité de la décision finale
               appartient toujours à l'opérateur humain."
               Traçabilité : chaque décision doit indiquer si elle est
               "confirmée IA", "corrigée IA" ou "hors scope IA".
```

#### Risque 4 — Dépendance Excessive (Single Point of Failure Cognitif)

```
Description : Si l'outil IA est indisponible (panne, maintenance), les
              opérateurs ayant perdu l'habitude de faire des prévisions
              manuelles se retrouvent en difficulté.

Mitigation   : Maintenir les compétences manuelles via des exercices périodiques
               "sans IA" (au moins trimestriels).
               Disposer de procédures dégradées documentées dans le Runbook.
```

#### Risque 5 — Biais dans les Prédictions

```
Description : Le modèle entraîné sur des données historiques peut reproduire
              ou amplifier des biais présents dans ces données.
              Ex : sous-estimation systématique de la consommation des régions
              climatiquement atypiques.

Mitigation   : Analyse SHAP des importances de features, revue mensuelle
               des erreurs par sous-population (région, type de jour, saison).
```

---

### 1.4 Matrice d'Impact Global

```
IMPACT
  │
  │  ÉLEVÉ    Dispatchers RTE ───────────── Planificateurs production
  │           (former + accompagner)         (former + accompagner)
  │
  │  MOYEN    Managers ────────── Data Scientists ────── MLOps/Ops
  │           (informer)         (pas de résistance)    (pas de résistance)
  │
  │  FAIBLE   Direction ─────────────────── DPO / Juridique
  │           (reporting KPI)               (audit conformité)
  │
  └──────────────────────────────────────────────────────────────
             FAVORABLE      NEUTRE       RÉSISTANT
                          ATTITUDE PRÉVISIBLE
```

---

## 2. Stratégie d'Accompagnement du Changement

### 2.1 Vision & Objectifs du Changement

**Vision :** *"L'IA de prédiction de consommation électrique est un copilote qui amplifie l'expertise des opérateurs RTE/EDF, leur permettant de se concentrer sur les décisions à haute valeur ajoutée tout en maintenant la sécurité et la fiabilité du réseau national."*

**Principes directeurs :**
1. **L'humain reste le décideur** — L'IA est un outil d'aide, jamais un substitut
2. **La transparence avant tout** — Les limites du modèle sont communiquées ouvertement
3. **Apprendre ensemble** — Les retours des utilisateurs alimentent l'amélioration du modèle
4. **Progressivité** — Pas de basculement brutal, montée en puissance par étapes

**Objectifs mesurables à 12 mois :**

| Objectif | Indicateur | Cible |
|:---|:---|:---:|
| Adoption de l'outil | % d'opérateurs consultant l'API ≥ 1x/jour | ≥ 80% |
| Satisfaction utilisateurs | Score NPS (Net Promoter Score) trimestriel | ≥ 40/100 |
| Qualité des prédictions | MAPE moyen sur données réelles | < 5% |
| Remontée de feedback | Nombre de fiches feedback soumises/mois | ≥ 10 |
| Autonomie | % d'opérateurs capables d'interpréter l'intervalle de confiance | ≥ 90% |
| Conformité | % de décisions tracées "avec/sans IA" | 100% |

---

### 2.2 Plan en 4 Phases

#### Phase 1 — Préparation (Mois 1-2)

**Objectif :** Créer les conditions du succès avant tout déploiement.

```
ACTIVITÉS CLÉS :
│
├── Audit de l'existant
│   • Cartographier les processus actuels de prévision (interviews terrain)
│   • Identifier les "champions du changement" parmi les opérateurs
│   • Évaluer le niveau de maturité digitale de chaque équipe
│
├── Définir la gouvernance IA
│   • Nommer un Responsable Usage IA (côté métier)
│   • Définir les règles d'utilisation responsable (voir §3.3)
│   • Valider le cadre juridique avec le DPO et le service juridique
│
├── Concevoir les formations (voir §2.4)
│   • Co-construire avec les futurs utilisateurs (pas imposer)
│   • Créer les supports : guide, fiche mémo, vidéos courtes
│
└── Préparer l'environnement technique
    • Déployer l'environnement de test (bac à sable)
    • Tester les accès réseau aux endpoints /predict et /health
    • Configurer les alertes Prometheus/Grafana opérationnelles
```

**Livrable de la phase :** Plan de formation validé + Charte d'utilisation IA signée

---

#### Phase 2 — Pilote (Mois 3-4)

**Objectif :** Tester en conditions réelles sur un groupe restreint de volontaires.

```
PÉRIMÈTRE DU PILOTE :
• 3 à 5 dispatchers volontaires (idéalement 1 junior, 2 seniors, 1 réticent)
• 1 équipe de planification H+24
• Période : 2 mois (1 cycle saisonnier printemps-été)

ACTIVITÉS :
│
├── Formation initiale (2h) pour les pilotes
├── Utilisation quotidienne de l'API avec journal de bord
├── Réunion hebdomadaire de suivi (30 min) avec le Responsable Usage IA
├── Collecte des feedbacks via le formulaire (voir §4.1)
└── Mesure des KPIs hebdomadaires
```

**Critères de passage en Phase 3 :**
- ✅ Score satisfaction pilotes ≥ 35/100
- ✅ Aucun incident critique d'usage (sur-confiance ayant causé une erreur)
- ✅ MAPE du modèle confirmé < 6% sur les données réelles de la période
- ✅ ≥ 80% des pilotes utilisent l'outil quotidiennement après 4 semaines

**Livrable de la phase :** Rapport de pilote + Retours d'expérience documentés

---

#### Phase 3 — Généralisation (Mois 5-8)

**Objectif :** Étendre à tous les utilisateurs concernés en s'appuyant sur les leçons du pilote.

```
DÉPLOIEMENT PAR VAGUES :
│
├── Vague 1 (mois 5) : Tous les dispatchers RTE (formation + suivi)
├── Vague 2 (mois 6) : Équipes de planification H+24/H+168
└── Vague 3 (mois 7-8) : Analystes énergie et équipes support

ACTIVITÉS :
│
├── Formations en groupes de 8–12 personnes (1 session/semaine)
│   (Les "champions" du pilote co-animent les sessions)
├── Mise en place du tableau Kanban de suivi des remontées (voir §4.3)
├── Revues mensuelles de qualité IA (métriques + feedback agrégé)
└── Communication régulière : newsletter IA interne (bimensuelle)
```

**Livrable de la phase :** Rapport de généralisation + KPIs adoption à M+8

---

#### Phase 4 — Ancrage (Mois 9-12 et au-delà)

**Objectif :** Institutionnaliser l'usage de l'IA dans les pratiques de travail.

```
ACTIVITÉS D'ANCRAGE :
│
├── Intégrer l'IA dans les procédures officielles de travail
│   (procédures d'exploitation RTE, guides de supervision)
│
├── Créer un "Comité IA Usage" trimestriel
│   (mixte : opérateurs + data scientists + management)
│   → Revue des métriques qualité + traitement des A3 (voir §4.2)
│
├── Exercices "mode dégradé" semestriels
│   (Simulation de panne de l'API → Maintien des compétences manuelles)
│
├── Cycle d'amélioration continue (voir §4)
│   → Les remontées traitées alimentent le backlog de développement
│
└── Rapport annuel d'impact IA
    → Valeur créée, incidents évités, progrès de précision du modèle
```

**Livrable de la phase :** Rapport d'impact annuel + Feuille de route IA 2027

---

### 2.3 Plan de Communication

| Public | Message clé | Canal | Fréquence | Responsable |
|:---|:---|:---:|:---:|:---:|
| Tous les opérateurs | "L'IA vous aide, ne vous remplace pas" | Réunion d'équipe | Au lancement | Manager |
| Pilotes | "Vos retours construisent un meilleur outil" | Slack/Teams dédié | Hebdo | Responsable Usage IA |
| Management | "Indicateurs d'adoption et de valeur créée" | Dashboard Grafana + email | Mensuel | Chef de projet |
| Direction | "ROI et conformité réglementaire" | Comité de direction | Trimestriel | Chef de projet |
| Équipes support | "Nouvelles procédures d'escalade" | Formation + RUNBOOK | Au déploiement | MLOps |

**Messages à éviter absolument :**
- ❌ "L'IA est infaillible" → Créé de la sur-confiance
- ❌ "L'IA va automatiser votre travail" → Créé de la résistance
- ❌ "L'IA a toujours raison" → Juridiquement faux et dangereux
- ❌ "Les anciens experts ne servent plus à rien" → Toxique pour l'adoption

---

### 2.4 Plan de Formation

#### Parcours de Formation par Profil

```
┌──────────────────────────────────────────────────────────────────────┐
│                    CATALOGUE DE FORMATIONS IA                         │
├────────────────┬─────────────────┬───────────────┬───────────────────┤
│ PUBLIC         │ MODULE          │ DURÉE         │ FORMAT            │
├────────────────┼─────────────────┼───────────────┼───────────────────┤
│ TOUS           │ Module 0 :      │ 30 min        │ Vidéo + Quiz      │
│ (obligatoire)  │ "IA : Qu'est-ce │               │ (auto-formation)  │
│                │  que c'est ?"   │               │                   │
├────────────────┼─────────────────┼───────────────┼───────────────────┤
│ Dispatchers    │ Module 1 :      │ 2h            │ Atelier pratique  │
│ Planificateurs │ "Lire et        │               │ (groupe 8–12)     │
│                │  interpréter    │               │                   │
│                │  une prédiction"│               │                   │
├────────────────┼─────────────────┼───────────────┼───────────────────┤
│ Dispatchers    │ Module 2 :      │ 1h            │ Atelier pratique  │
│ Planificateurs │ "Quand faire    │               │                   │
│                │  confiance à    │               │                   │
│                │  l'IA ? Quand   │               │                   │
│                │  s'en méfier ?" │               │                   │
├────────────────┼─────────────────┼───────────────┼───────────────────┤
│ Managers       │ Module 3 :      │ 1h30          │ Séminaire         │
│                │ "Piloter une    │               │ management        │
│                │  équipe avec IA"│               │                   │
├────────────────┼─────────────────┼───────────────┼───────────────────┤
│ Data Scientists│ Module 4 :      │ 4h            │ Workshop technique │
│ MLOps          │ "Maintenance    │               │                   │
│                │  et ré-entraîne-│               │                   │
│                │  ment du modèle"│               │                   │
├────────────────┼─────────────────┼───────────────┼───────────────────┤
│ TOUS           │ Module 5 :      │ 1h            │ Retour terrain    │
│ (à M+6)        │ "Bilan 6 mois   │               │ + Q&R             │
│                │  et amélioration│               │                   │
└────────────────┴─────────────────┴───────────────┴───────────────────┘
```

#### Contenu du Module 1 — "Lire et Interpréter une Prédiction" (détail)

**Objectifs pédagogiques :**
1. Comprendre ce que prédit le modèle (MW, pas kWh, pas une région)
2. Lire les métriques clés (MAPE 4,68%, RMSE 3 142 MW, Accuracy ±5% 69,48%)
3. Identifier les situations où le modèle est moins fiable
4. Suivre la procédure de consultation et de validation

**Séquence de l'atelier (2h) :**
```
[0:00 – 0:20]  Présentation : "Pourquoi cet outil ? Que fait-il exactement ?"
[0:20 – 0:50]  Démonstration live de l'API /predict avec des cas réels
[0:50 – 1:10]  Exercice 1 : Interpréter 5 prédictions (cas nominaux)
[1:10 – 1:40]  Exercice 2 : Identifier les 3 cas où vous ne devez PAS
               suivre la prédiction sans vérification
[1:40 – 2:00]  Questions / Retours / Distribution de la fiche mémo
```

---

## 3. Kit de Bonne Utilisation de l'IA

### 3.1 Guide "Comment Utiliser les Prédictions ?"

---

#### 🔵 QU'EST-CE QUE L'IA PRÉDIT ?

L'outil prédit la **consommation électrique nationale française** à un instant donné, exprimée en **mégawatts (MW)**.

```
Exemple de réponse de l'API :
{
  "prediction_mw": 58 432,        ← Consommation prédite : 58 432 MW
  "status": "success",
  "model_used": "KNeighborsRegressor",
  "latency_sec": 0.004
}
```

**Ce que cette valeur signifie :**
- La consommation prédite est de **58 432 MW**
- La précision typique du modèle est de **±3 142 MW** (RMSE) dans 68% des cas
- Exprimé en pourcentage : erreur moyenne de **±4,68%** (MAPE)
- Donc la vraie consommation sera probablement entre **55 290 MW et 61 574 MW**

---

#### 🟢 LES 5 QUESTIONS AVANT D'AGIR SUR UNE PRÉDICTION

Avant d'utiliser une prédiction IA pour une décision opérationnelle, posez-vous ces 5 questions :

```
Question 1 : LE CONTEXTE EST-IL NORMAL ?
  → Y a-t-il un événement exceptionnel aujourd'hui ?
    (grève nationale, match de football en soirée, épisode météo extrême,
     jour férié non calendaire, panne industrielle régionale ?)
  Si OUI → La prédiction est peut-être inadaptée → Appliquer votre expertise

Question 2 : LA VALEUR EST-ELLE PLAUSIBLE ?
  → La prédiction est-elle dans les bornes physiques historiques ?
    Hiver : 55 000 – 102 000 MW
    Été   : 30 000 – 70 000 MW
    Nuit  : 25 000 – 60 000 MW
  Si NON → Alerte : signaler sur le formulaire de feedback (§4.1)

Question 3 : LES DONNÉES D'ENTRÉE SONT-ELLES CORRECTES ?
  → La température fournie correspond-elle à la réalité d'aujourd'hui ?
  → Les lags (t-24h, t-48h) sont-ils issus de données fiables ?
  "Garbage in, garbage out" : une mauvaise entrée donne une mauvaise sortie.

Question 4 : LE MODÈLE EST-IL À JOUR ?
  → Vérifier dans Grafana : la dernière mise à jour du modèle date de quand ?
  → Y a-t-il une alerte de dérive active ?
  Si le modèle n'a pas été ré-entraîné depuis > 4 semaines en été → Prudence

Question 5 : MA DÉCISION EST-ELLE RÉVERSIBLE ?
  → Si la prédiction est fausse, les conséquences sont-elles graves ?
  → Plus la décision est irréversible et impactante, plus la validation
    humaine doit être rigoureuse.
```

---

#### 🟡 SITUATIONS OÙ FAIRE CONFIANCE À L'IA

Le modèle est **particulièrement fiable** dans ces conditions :

| Situation | Pourquoi | Niveau de confiance |
|:---|:---|:---:|
| Journée de semaine ordinaire | Données similaires en entraînement | 🟢 Élevé |
| Températures entre 5°C et 25°C | Zone de bonne calibration du modèle | 🟢 Élevé |
| Données de lag disponibles et récentes | Les features les plus prédictives sont présentes | 🟢 Élevé |
| Période printemps-automne | Saisons bien représentées dans les données | 🟢 Élevé |
| Prédiction à H+1 ou H+4 | Court terme = moins d'incertitude | 🟢 Élevé |

---

#### 🔴 SITUATIONS OÙ NE PAS SUIVRE L'IA SEULE

Le modèle est **moins fiable** dans ces situations — votre expertise est essentielle :

| Situation | Raison | Action recommandée |
|:---|:---|:---|
| **Événement exceptionnel** | Grève nationale, sommet G7, match Coupe du Monde | Ajustement manuel obligatoire |
| **Canicule extrême (>38°C)** | Hors de la plage d'entraînement (données synthétiques) | Réduire la prédiction de 5–10% (clim intensive) |
| **Grand froid polaire (<-10°C)** | Rare dans les données d'entraînement | Augmenter la prédiction de 5–15% |
| **Panne industrielle régionale** | Le modèle ne connaît pas les pannes | Ajustement manuel selon impact estimé |
| **Nouveau comportement de consommation** | Déploiement massif de pompes à chaleur, VE | Alerter le Data Scientist (dérive structurelle) |
| **Jour de transition de saison** | Comportement mixte chauffage/climatisation | Validation croisée avec historique J-7 |
| **Alerte de dérive active** | Le modèle a détecté sa propre dérive | Attendre le ré-entraînement, prudence maximale |

---

#### 📊 INTERPRÉTER LES MÉTRIQUES DU MODÈLE

Quand vous consultez le tableau de bord de supervision (Grafana), voici comment lire les indicateurs :

```
┌────────────────────────────────────────────────────────────────┐
│  TABLEAU DE BORD QUALITÉ IA (Grafana)                          │
├─────────────────┬──────────────┬─────────────────┬────────────┤
│ INDICATEUR      │ VALEUR CIBLE │ ZONE D'ALERTE   │ CRITIQUE   │
├─────────────────┼──────────────┼─────────────────┼────────────┤
│ MAPE            │ < 5%         │ 5% – 8%         │ > 8%       │
│ (erreur relat.) │ ✅ Nominal   │ ⚠️ Surveiller   │ 🔴 Agir   │
├─────────────────┼──────────────┼─────────────────┼────────────┤
│ Latence API     │ < 100 ms     │ 100 ms – 500 ms │ > 500 ms   │
│                 │ ✅ Nominal   │ ⚠️ Surveiller   │ 🔴 Agir   │
├─────────────────┼──────────────┼─────────────────┼────────────┤
│ Drift Score     │ KS < 0.3     │ 0.3 – 0.6       │ > 0.6      │
│ (dérive)        │ ✅ Stable    │ ⚠️ Ré-entraîner │ 🔴 Urgent │
├─────────────────┼──────────────┼─────────────────┼────────────┤
│ Santé API       │ ✅ ok        │ —               │ ❌ unhealthy│
└─────────────────┴──────────────┴─────────────────┴────────────┘
```

**Que faire si un indicateur est en zone critique ?**
1. Ne pas ignorer l'alerte
2. Contacter l'équipe MLOps via le canal dédié (Slack `#mlops-alerts`)
3. Augmenter votre vigilance sur les prédictions jusqu'à retour à la normale
4. Documenter vos observations dans le formulaire de feedback

---

### 3.2 Fiche de Référence Rapide (Aide-Mémoire)

```
╔══════════════════════════════════════════════════════════════╗
║          AIDE-MÉMOIRE — IA PRÉDICTION CONSOMMATION          ║
║                      RTE / EDF                               ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  CE QUE L'IA FAIT           │  CE QUE L'IA NE FAIT PAS      ║
║  ─────────────────────      │  ─────────────────────────     ║
║  ✅ Prédit la conso.         │  ❌ Décider à votre place      ║
║     nationale en MW          │  ❌ Connaître les pannes       ║
║  ✅ Intègre temp. + heure    │  ❌ Gérer les événements        ║
║     + historique             │     exceptionnels              ║
║  ✅ Répond en < 1 seconde    │  ❌ Être infaillible            ║
║                              │  ❌ Prédire à H+168 (semaine)  ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  VÉRIFICATION RAPIDE (30 secondes)                          ║
║  ─────────────────────────────────                          ║
║  □ 1. La valeur est physiquement plausible ? (25K–102K MW)  ║
║  □ 2. Pas d'événement exceptionnel aujourd'hui ?            ║
║  □ 3. La température fournie est correcte ?                  ║
║  □ 4. Pas d'alerte de dérive active dans Grafana ?          ║
║  □ 5. API en état "ok" (/health) ?                           ║
║       → Si tout ✅ : confiance normale                       ║
║       → Si un ❌  : vérification approfondie requise         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  EN CAS DE DOUTE               EN CAS D'ANOMALIE            ║
║  ─────────────────             ──────────────────           ║
║  → Croiser avec votre          → Formulaire feedback         ║
║    expérience et les           → Slack #mlops-alerts         ║
║    données J-7                 → Appel MLOps astreinte       ║
║  → Consulter un collègue       → Ne pas utiliser la          ║
║  → Documenter votre            prédiction jusqu'à            ║
║    décision finale             confirmation                  ║
╚══════════════════════════════════════════════════════════════╝
```

*À afficher dans la salle de supervision et à conserver dans le classeur opérateur.*

---

### 3.3 Check-list d'Utilisation Responsable de l'IA

Cette check-list doit être respectée par tout utilisateur de l'outil IA. Elle est organisée en **6 dimensions** de l'utilisation responsable.

---

#### Dimension 1 — Fiabilité & Qualité

```
□ Je vérifie que l'API est disponible avant de consulter une prédiction
  (GET /health → {"status": "ok"})

□ Je m'assure que les données d'entrée que je fournis sont exactes
  (température du jour, lags réels et non estimés si possible)

□ Je note la valeur du MAPE actuel du modèle (dashboard Grafana)
  avant d'utiliser une prédiction pour une décision critique

□ Si le MAPE est > 6% ou si une alerte de dérive est active,
  je traite la prédiction comme indicative seulement

□ Je croise systématiquement la prédiction avec une source secondaire
  (historique J-1, J-7, modèle météo) pour les décisions à fort impact
```

#### Dimension 2 — Éthique & Responsabilité

```
□ Je comprends que la décision finale m'appartient, pas à l'IA

□ Je ne me dédouane jamais d'une mauvaise décision en disant
  "c'est l'IA qui m'a dit de le faire"

□ Je documente si ma décision opérationnelle a été :
  ✅ Confirmée par l'IA  |  ✏️ Corrigée vs l'IA  |  ⬜ Sans consultation IA

□ Je signale toute prédiction qui me semble manifestement incorrecte
  (même si mon intuition se révèle fausse — les deux cas sont utiles)

□ Je n'utilise jamais l'IA pour des décisions hors de son périmètre
  (sécurité physique du réseau, décisions politiques tarifaires, etc.)
```

#### Dimension 3 — Supervision Humaine

```
□ Je maintiens mes compétences de prévision manuelle
  (je participe aux exercices "sans IA" semestriels)

□ Je suis en mesure de faire une prévision raisonnée sans l'outil
  en cas de panne de l'API (procédure dégradée)

□ Je ne délègue pas entièrement ma vigilance à l'outil :
  je reste attentif aux signaux du terrain

□ Si un comportement de l'IA me surprend à plusieurs reprises,
  je le remonte — ce n'est pas normal, c'est peut-être une dérive

□ Je participe aux réunions mensuelles de revue qualité IA
  (au moins une fois par trimestre)
```

#### Dimension 4 — Sécurité Informatique

```
□ Je n'envoie jamais de données sensibles ou confidentielles
  dans les requêtes à l'API /predict
  (noms de centrales, données de sécurité nationale, contrats, etc.)

□ Je n'essaie pas de contourner les mécanismes de sécurité de l'API
  (pas de tests de pénétration non autorisés)

□ Je signale immédiatement toute anomalie de sécurité perçue
  (réponses inattendues, lenteurs excessives, messages d'erreur inhabituels)
  au canal #securite-si

□ Je ne partage pas mes identifiants d'accès à l'API avec des tiers

□ Je ne cherche pas à inférer des informations sur l'architecture interne
  via les messages d'erreur de l'API
```

#### Dimension 5 — Conformité RGPD & Réglementaire

```
□ Je ne transmets aucune donnée à caractère personnel dans les requêtes
  (l'API /predict ne nécessite aucune donnée personnelle)

□ Je suis informé(e) que mes interactions avec l'outil peuvent être
  loggées à des fins de supervision et d'amélioration

□ Je comprends que l'IA Act européen classe cet outil en "risque limité"
  (système d'aide à la décision dans infrastructure critique)
  → obligation de transparence envers les utilisateurs ✅ (ce document)

□ Je sais à qui m'adresser pour toute question RGPD : le DPO de mon entité

□ Si des données de production réelles (consommation régionale, données
  contractuelles) devaient être utilisées pour améliorer le modèle,
  je vérifierai au préalable avec le DPO la licéité du traitement
```

#### Dimension 6 — Amélioration Continue

```
□ Je soumets au moins 1 fiche de feedback par mois
  (même positive : "la prédiction était excellente ce jour-là, voici pourquoi")

□ Je remplis le formulaire de feedback immédiatement après avoir observé
  une prédiction anormale (pas le lendemain — les détails s'oublient)

□ Je participe aux ateliers d'amélioration A3 quand je suis invité(e)

□ Je propose des idées d'amélioration de l'outil :
  nouvelles features, nouveaux cas d'usage, indicateurs manquants

□ Je partage mes bonnes pratiques avec mes collègues moins à l'aise
  avec l'outil (je joue le rôle de "pair IA" dans mon équipe)
```

---

## 4. Outils Lean & Amélioration Continue

### 4.1 Formulaire de Feedback Utilisateur

*Ce formulaire doit être rempli dès qu'un utilisateur observe une anomalie, une prédiction surprenante, ou souhaite partager une bonne pratique. Il est disponible en version papier (salle de supervision) et en version numérique (lien intranet / QR code).*

---

```
╔══════════════════════════════════════════════════════════════════════╗
║           FICHE DE FEEDBACK — IA PRÉDICTION CONSOMMATION           ║
║                      EDF / RTE — Version 1.0                        ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  DATE : ___/___/______    HEURE : ___h___    REF : FF-____          ║
║                                                                      ║
║  AUTEUR (optionnel) : _______________________  ÉQUIPE : __________  ║
║                                                                      ║
╠═══════════════════════ SECTION 1 — CONTEXTE ══════════════════════╣
║                                                                      ║
║  Type de retour :                                                    ║
║  □ Anomalie de prédiction    □ Bonne pratique à partager            ║
║  □ Problème technique API    □ Suggestion d'amélioration            ║
║  □ Question / Incompréhension                                        ║
║                                                                      ║
║  Datetime de la prédiction concernée :                               ║
║  _______________________________ (format : YYYY-MM-DDTHH:MM:SS)     ║
║                                                                      ║
║  Température fournie : _______ °C                                   ║
║                                                                      ╣
╠═══════════════════════ SECTION 2 — OBSERVATION ═══════════════════╣
║                                                                      ║
║  Valeur prédite par l'IA : ______________ MW                        ║
║                                                                      ║
║  Valeur réelle observée (si connue) : __________ MW                 ║
║                                                                      ║
║  Écart : __________ MW  (soit _______ %)                            ║
║                                                                      ║
║  Description de l'anomalie ou de l'observation :                    ║
║  __________________________________________________________________ ║
║  __________________________________________________________________ ║
║  __________________________________________________________________ ║
║                                                                      ║
╠══════════════════ SECTION 3 — CONTEXTE ÉVÉNEMENTIEL ══════════════╣
║                                                                      ║
║  Y avait-il un événement exceptionnel ? □ Oui  □ Non                ║
║  Si oui, lequel : _____________________________________________     ║
║                                                                      ║
║  Conditions météo inhabituelles ? □ Oui  □ Non                     ║
║  Si oui : _____________________________________________________     ║
║                                                                      ║
║  Alerte de dérive active dans Grafana ? □ Oui  □ Non  □ Non vérifié ║
║                                                                      ║
╠════════════════════ SECTION 4 — IMPACT & DÉCISION ════════════════╣
║                                                                      ║
║  Avez-vous utilisé la prédiction pour une décision ? □ Oui  □ Non  ║
║                                                                      ║
║  Si oui, quelle décision :                                          ║
║  __________________________________________________________________ ║
║                                                                      ║
║  Avez-vous corrigé la prédiction de l'IA ? □ Oui  □ Non            ║
║  Si oui, nouvelle valeur utilisée : ______________ MW               ║
║  Raison de la correction :                                          ║
║  __________________________________________________________________ ║
║                                                                      ║
║  Impact estimé de l'anomalie :                                      ║
║  □ Aucun  □ Faible (informatif)  □ Modéré  □ Élevé (décision altérée)║
║                                                                      ║
╠════════════════════ SECTION 5 — SUGGESTION (optionnel) ════════════╣
║                                                                      ║
║  Avez-vous une suggestion pour améliorer l'outil ?                  ║
║  __________________________________________________________________ ║
║  __________________________________________________________________ ║
║                                                                      ║
╠════════════════════ SECTION 6 — TRAITEMENT (Usage Resp. IA) ═══════╣
║                                                                      ║
║  Date de réception : ___/___/______   Traité par : _______________  ║
║  Priorité : □ P1 Critique  □ P2 Majeur  □ P3 Mineur  □ P4 Info     ║
║  Action décidée : ____________________________________________      ║
║  Ticket MLOps créé : □ Oui (ref: __________)  □ Non                ║
║  Clôture : ___/___/______                                           ║
╚══════════════════════════════════════════════════════════════════════╝
```

**Circuit de traitement du formulaire :**
```
Utilisateur remplit le formulaire (papier ou numérique)
    │
    ▼
Responsable Usage IA reçoit et trie (sous 24h ouvrées)
    │
    ├── Anomalie technique → Ticket MLOps (Jira) → Traitement technique
    ├── Suggestion → Backlog produit IA → Priorisé lors du Comité IA
    ├── Question → Réponse directe + ajout à la FAQ
    └── Bonne pratique → Partage dans la newsletter + MAJ du guide
```

---

### 4.2 Template A3 d'Amélioration Continue

*L'A3 est un outil Lean qui tient sur une feuille A3. Il structure le résolution de problèmes récurrents ou complexes détectés via les feedbacks. Un A3 est ouvert quand un problème se répète plus de 3 fois ou a un impact élevé.*

---

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    FICHE A3 — AMÉLIORATION CONTINUE IA                      ║
║                          EDF / RTE — Prédiction Conso.                       ║
╠══════════════════════════════════╦═══════════════════════════════════════════╣
║  TITRE DU PROBLÈME :             ║  DATE OUVERTURE : ___/___/______          ║
║  ___________________________     ║  PILOTE : _____________________________   ║
║  ___________________________ __  ║  ÉQUIPE : _____________________________   ║
║  REF A3 : A3-____                ║  DATE CIBLE RÉSOLUTION : ___/___/______   ║
╠══════════════════════════════════╩═══════════════════════════════════════════╣
║                                                                              ║
║  1. CONTEXTE & SITUATION ACTUELLE                                            ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║  Décrivez le problème constaté, sa fréquence, son périmètre.                ║
║  Appuyez-vous sur des données mesurées (MAPE, nb de feedbacks, dates).      ║
║                                                                              ║
║  ___________________________________________________________________________║
║  ___________________________________________________________________________║
║  ___________________________________________________________________________║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  2. OBJECTIF CIBLE (SMART)                                                   ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║  Quel est l'état cible attendu ? Mesurable, avec une échéance claire.        ║
║                                                                              ║
║  Ex : "Réduire le MAPE en période de canicule de 9% à < 5% avant M+3"       ║
║                                                                              ║
║  ___________________________________________________________________________║
║  ___________________________________________________________________________║
║                                                                              ║
╠═════════════════════════════╦════════════════════════════════════════════════╣
║  3. ANALYSE DES CAUSES      ║  4. SOLUTIONS IDENTIFIÉES                     ║
║     (5 Pourquoi / Ishikawa) ║                                                ║
║  ───────────────────────    ║  ─────────────────────────────────────────    ║
║  Pourquoi 1 :               ║  Solution A : ____________________________    ║
║  ___________________        ║  Responsable : ______  Délai : __________     ║
║                             ║                                                ║
║  Pourquoi 2 :               ║  Solution B : ____________________________    ║
║  ___________________        ║  Responsable : ______  Délai : __________     ║
║                             ║                                                ║
║  Pourquoi 3 :               ║  Solution C : ____________________________    ║
║  ___________________        ║  Responsable : ______  Délai : __________     ║
║                             ║                                                ║
║  Cause racine :             ║  Solution retenue : ______________________    ║
║  ___________________        ║  Pourquoi ? : ____________________________    ║
╠═════════════════════════════╩════════════════════════════════════════════════╣
║                                                                              ║
║  5. PLAN D'ACTION DÉTAILLÉ                                                   ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║  Action             │ Responsable │ Délai    │ Statut      │ Validation      ║
║  ──────────────────────────────────────────────────────────────────────    ║
║  __________________ │ ___________ │ ________ │ □ À faire   │ _____________  ║
║  __________________ │ ___________ │ ________ │ □ En cours  │ _____________  ║
║  __________________ │ ___________ │ ________ │ □ Terminé   │ _____________  ║
║  __________________ │ ___________ │ ________ │ □ À faire   │ _____________  ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  6. RÉSULTATS & VÉRIFICATION                                                 ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║  Avant : MAPE = _____%  │  Latence = ___ms  │  Feedbacks/mois = ____        ║
║  Après : MAPE = _____%  │  Latence = ___ms  │  Feedbacks/mois = ____        ║
║                                                                              ║
║  Problème résolu ? □ Oui  □ Partiellement  □ Non (→ Ouvrir A3 suivant)      ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  7. PÉRENNISATION & PARTAGE                                                  ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║  Comment s'assurer que le problème ne revient pas ?                         ║
║  □ MAJ du guide utilisateur   □ MAJ du Runbook   □ Nouvelle règle Airflow   ║
║  □ Formation complémentaire    □ Alerte Prometheus ajoutée                   ║
║                                                                              ║
║  Ce retour a-t-il été partagé lors du Comité IA ? □ Oui (date : ________) ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

**Exemples d'A3 types déjà identifiés :**

| Réf | Titre | Cause racine probable | Solution envisagée |
|:---|:---|:---|:---|
| A3-001 | MAPE > 8% en canicule (>35°C) | Données d'entraînement sans canicule extrême | Ajouter des données climatiques extrêmes synthétiques + variable humidité |
| A3-002 | Prédictions aberrantes le 1er janvier | Effet "Jour de l'An" non capturé | Vérifier le flag `is_holiday` pour le 1er janvier |
| A3-003 | Taux de feedback < 3/mois | Formulaire trop long, peu accessible | Version QR code 3 questions seulement |

---

### 4.3 Tableau Kanban des Retours d'Usage

*Ce tableau est affiché physiquement en salle de réunion MLOps et disponible en version numérique (Jira / Trello). Il est mis à jour hebdomadairement par le Responsable Usage IA.*

```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│   📥 REÇUS      │  🔍 EN ANALYSE  │  🔧 EN COURS    │  ✅ CLÔTURÉS    │
│   (Non traité)  │   (Priorisé)    │   (Assigné)     │   (Ce mois)     │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│                 │                 │                 │                 │
│  [FF-023]       │  [FF-019]       │  [FF-017]       │  [FF-015]       │
│  Prédiction basse│ MAPE élevé les │  Ajouter feature│  Latence API    │
│  un dimanche de │  jours de pont  │  "veille jour   │  corrigée       │
│  canicule       │                 │  férié"         │  (< 5ms)        │
│  P2 - Majeur    │  P1 - Critique  │  P3 - Mineur    │                 │
│  J. Martin      │  Data Science   │  MLOps          │  [FF-014]       │
│                 │                 │                 │  Feedback format │
│  [FF-022]       │  [FF-018]       │  [FF-016]       │  datetime corrigé│
│  Question sur   │  API lente      │  Ajout d'un     │                 │
│  l'intervalle   │  > 200ms        │  endpoint       │  [FF-013]       │
│  de confiance   │  pendant les    │  /predict/batch │  Guide mis à    │
│                 │  pics           │                 │  jour section 3 │
│  [FF-021]       │                 │                 │                 │
│  Suggestion :   │                 │                 │                 │
│  Afficher       │                 │                 │                 │
│  l'incertitude  │                 │                 │                 │
│  dans la réponse│                 │                 │                 │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ Total : 3       │ Total : 2       │ Total : 2       │ Total : 3 ce M  │
│                 │                 │                 │ Cumul : 15      │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘

Légende couleurs :
🔴 P1 Critique (< 24h)  |  🟠 P2 Majeur (< 1 sem)
🟡 P3 Mineur (< 1 mois) |  🟢 P4 Info (backlog)
```

**Cadence de revue du Kanban :**
- **Quotidien** (5 min) : Le Responsable Usage IA vérifie les nouveaux tickets P1
- **Hebdomadaire** (30 min) : Revue de tous les tickets avec l'équipe MLOps
- **Mensuel** (1h) : Comité IA — Présentation des clôtures et ouverture des A3 si besoin

---

### 4.4 Procédure de Traitement des Incidents d'Usage

Cette procédure standardise le traitement des feedbacks qui signalent un comportement anormal de l'IA.

```
RÉCEPTION D'UN FEEDBACK
        │
        ▼
┌───────────────────────────────────────────┐
│  TRIAGE (Responsable Usage IA — sous 24h) │
│                                           │
│  Évaluer : Impact × Fréquence             │
└───────────┬───────────────────────────────┘
            │
    ┌───────┼───────────┬──────────────────┐
    ▼       ▼           ▼                  ▼
  P1       P2          P3                P4
CRITIQUE  MAJEUR     MINEUR            INFO
  │         │           │                │
  ▼         ▼           ▼                ▼
Alerte   Ticket     Backlog          Archivé
MLOps    MLOps      produit          + FAQ
immédiate 24h      sprint+1
  │         │           │
  ▼         ▼           ▼
┌─────────────────────────────────────────┐
│  INVESTIGATION (MLOps + Data Science)   │
│                                         │
│  1. Reproduire le problème              │
│  2. Analyser les logs (kubectl logs)    │
│  3. Vérifier drift_report.json          │
│  4. Vérifier mlflow_logs.json           │
│  5. Simuler avec les données du feedback│
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│  DÉCISION                               │
│                                         │
│  □ Bug technique → PR + déploiement     │
│  □ Dérive modèle → DAG Airflow trigger  │
│  □ Feature manquante → Backlog sprint   │
│  □ Erreur d'usage → Formation complém.  │
│  □ Faux positif → Archiver + expliquer  │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│  CLÔTURE & FEEDBACK EN RETOUR           │
│                                         │
│  • Informer l'auteur du feedback        │
│  • Mettre à jour le guide si nécessaire │
│  • Partager lors du prochain Comité IA  │
│  • Mettre à jour le Kanban (→ Clôturé)  │
└─────────────────────────────────────────┘
```

---

## 5. Indicateurs de Maturité d'Adoption (KPIs Humains)

Ces indicateurs mesurent non pas la performance technique de l'IA, mais la **qualité de son adoption** par les équipes. Ils sont revus mensuellement lors du Comité IA.

### 5.1 Tableau de Bord d'Adoption

| KPI | Description | Méthode de mesure | Cible M+6 | Cible M+12 |
|:---|:---|:---:|:---:|:---:|
| **Taux d'utilisation** | % d'opérateurs ayant consulté l'API ≥ 1x dans la semaine | Logs API (User-Agent ou token) | ≥ 60% | ≥ 85% |
| **Taux de feedback** | Nombre de fiches feedback soumises / mois | Comptage formulaires | ≥ 5/mois | ≥ 15/mois |
| **Score NPS** | "Recommanderiez-vous cet outil à un collègue ?" (0–10) | Enquête trimestrielle | ≥ 30 | ≥ 50 |
| **Taux de correction** | % de prédictions utilisées sans correction / total | Formulaire décision | Mesure | ≤ 30% correction |
| **Temps de réponse incident** | Délai moyen entre soumission feedback P1 et résolution | Kanban (date ouv. / clôt.) | < 48h | < 24h |
| **Taux de formation** | % d'utilisateurs cibles ayant suivi les modules obligatoires | Suivi RH / plateforme | ≥ 80% | 100% |
| **Autonomie** | % capables d'expliquer "MAPE" et "dérive" sans aide | Quiz post-formation | ≥ 70% | ≥ 90% |
| **A3 clôturés** | Nombre d'A3 ouverts et clôturés dans le trimestre | Kanban A3 | ≥ 1 | ≥ 3 |

### 5.2 Radar de Maturité IA (Évaluation Semestrielle)

```
                        FIABILITÉ TECHNIQUE
                              ⬆
                         5 ●──────●
                       4 ● │        ● 4
AMÉLIORATION    ←  3 ──────┼──────── 3  → GOUVERNANCE
CONTINUE           2 ● │        ● 2       & CONFORMITÉ
                       1 ● │        ● 1
                         1──────●
                              ⬇
                         ADOPTION HUMAINE

Niveaux :
1 = Initiation (l'outil existe, peu utilisé)
2 = Développement (usage partiel, formation en cours)
3 = Maîtrise (usage régulier, feedback actif)
4 = Optimisation (amélioration continue active)
5 = Excellence (référence, outil institutionnalisé)

Objectif M+12 : Score ≥ 3 sur toutes les dimensions
```

### 5.3 Plan de Revue et de Gouvernance

| Instance | Participants | Fréquence | Ordre du jour |
|:---|:---|:---:|:---|
| **Stand-up IA** | MLOps + Resp. Usage IA | Quotidien (5 min) | Alertes, tickets P1 |
| **Revue Kanban** | MLOps + Resp. Usage IA + 1 opérateur | Hebdomadaire (30 min) | Tickets, priorisation |
| **Comité IA** | Tous stakeholders | Mensuel (1h) | KPIs, A3, backlog, dérive |
| **Revue de direction** | Management + Chef de projet | Trimestriel (30 min) | ROI, SLA, tendances |
| **Audit de conformité** | DPO + RSSI + Chef de projet | Semestriel (2h) | RGPD, IA Act, sécurité |

---

## 6. Références Croisées

Ce document s'inscrit dans un ensemble cohérent de trois livrables :

| Thème | Livrable 1 | Livrable 2 | Ce document (Livrable 3) |
|:---|:---:|:---:|:---:|
| Architecture technique | §1 | §1.1 | — |
| Performances du modèle | §1.2.B | §1.2 | §3.1 (interprétation utilisateur) |
| Limites et incertitude | §3.4 | §5.1 Note 1 | §3.1 🔴 "Quand ne pas faire confiance" |
| Dérive et ré-entraînement | §2.3, 2.4 | §3.3 Incident C | §3.3 Check-list Dim.1 + §4.4 |
| Rollback et incidents | §2.4 | §2.4, §3 | §3.2 "En cas d'anomalie" |
| Rôles et responsabilités | §2.6 RACI | — | §2.1, §2.3 |
| Conformité RGPD | §2.1.D | §5.1 Rec. 2 | §3.3 Dimension 5 |
| Métriques qualité | §2.2 | §1.4 Runbook | §3.1 "Interpréter les métriques" |
| Amélioration continue | §3.4.C | §5.1 Rec. 10 | §4 (tout) |

---

*Document rédigé le 03 juin 2026 — CDPIA MSPR TPRE932 & TPRE942*
*Livrable 3 : Plan d'Accompagnement du Changement & de Bonne Utilisation de l'IA*
*Projet EDF/RTE — Prédiction de Consommation Électrique Nationale*

---
> **Voir aussi :**
> - [Livrable 1 — Dossier de Déploiement & Maintenabilité](file:///C:/Users/USER/.gemini/antigravity/brain/1e5021d6-d49a-4fe7-9504-c69fb7af4a5a/dossier_deploiement_maintenabilite.md)
> - [Livrable 2 — Documentation Technique & Runbook](file:///C:/Users/USER/.gemini/antigravity/brain/1e5021d6-d49a-4fe7-9504-c69fb7af4a5a/documentation_technique_runbook.md)
