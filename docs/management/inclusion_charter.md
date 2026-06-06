# Charte de Collaboration Internationale & d'Inclusion Numérique

Ce document définit les règles de gouvernance interculturelle pour la R&D d'EDF (répartie sur 9 centres mondiaux) et les aménagements ergonomiques pour garantir l'accessibilité à tous les profils de handicap.

---

## 1. Gouvernance Interculturelle et Collaboration Asynchrone

Le projet réunit des ingénieurs situés en France, en Chine, aux États-Unis, en Allemagne et au Royaume-Uni. Pour surmonter les décalages horaires et optimiser l'inclusion de chacun :

### A. Fenêtre de Communication Universelle ("Core Hours")
*   Les réunions synchrone en visio (Daily Scrum hebdomadaires élargis, revues de sprint) se tiennent exclusivement sur la plage horaire commune : **14h00 - 16h00 (Heure de Paris / CET)**.
    *   *Paris :* 14h - 16h
    *   *Pékin :* 20h - 22h (limité aux points essentiels)
    *   *New York :* 08h - 10h
*   Aucun point d'équipe critique n'est planifié en dehors de cette plage.

### B. Prémisse de la Communication "Asynchrone d'Abord"
*   Toute décision technique, modification d'architecture ou arbitrage de modélisation doit être documentée sur la base de connaissances commune (Git / Confluence) en **anglais technique simple**.
*   Les canaux de messagerie instantanée (Slack/Teams) disposent de canaux dédiés par lots techniques (`#data-pipeline`, `#model-rbfn`, `#mlops-k8s`).
*   Toute discussion synchrone se conclut par la rédaction d'un résumé écrit succinct partagé sur le canal approprié.

---

## 2. Plan d'Inclusion et d'Accessibilité Numérique

Pour garantir que les outils opérationnels (FastAPI docs, Dashboards de monitoring Grafana, rapports techniques) soient utilisables par tous :

### A. Handicap Visuel et Daltonisme (Deutéranopie, Protanopie, Tritanopie)
*   **Charte Graphique Accessible :** Les tableaux de bord Grafana et les graphiques d'explicabilité (SHAP) proscrivent l'association binaire rouge/vert pour indiquer des états de santé système ou des dérives (drift).
*   **Norme appliquée :** Les palettes de couleurs reposent sur le standard *ColorBrewer* (combinaison bleu/orange contrastée ou nuances de gris complétées de symboles typographiques explicites : `✔` pour nominal, `⚠` pour alerte, `✖` pour arrêt critique).
*   Les textes des interfaces web doivent respecter un contraste minimal de **4.5:1** conforme aux normes WCAG 2.1 niveau AA.

### B. Neuroatypies (TDAH, Troubles Dys, Autisme)
*   **Décomposition Cognitive :** L'organisation des tâches s'appuie sur le principe de Goblin.tools : division systématique des epics et des tâches en sous-étapes extrêmement granulaires (durée < 4h) sans surcharge de métaphores.
*   **Documentation "Sans Distraction" :** Les documentations techniques évitent les blocs de texte denses. L'usage de listes à puces claires, de schémas Mermaid épurés et de synthèses visuelles en début de document est généralisé.
*   **Réduction du bruit cognitif :** Lors des réunions, les partages d'écrans sont limités au document ou code concerné, évitant les transitions visuelles rapides.

### C. Handicap Auditif
*   **Sous-titrage en temps réel :** Activation systématique du sous-titrage automatique (Teams Live Captions) et de la transcription écrite pour tous les appels oraux.
*   **Enregistrements disponibles :** Toutes les réunions et démos de sprint font l'objet d'un enregistrement vidéo hébergé en interne, permettant aux collaborateurs malentendants ou n'ayant pas l'anglais/français comme langue maternelle de réécouter à leur rythme avec retranscription.
