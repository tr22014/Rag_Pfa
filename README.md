# Rag_Pfa — Plateforme de Gestion des Connaissances d'Entreprise (RAG)

> Plateforme intelligente de gestion des connaissances basée sur le **Retrieval-Augmented Generation (RAG)**, permettant à une organisation de centraliser ses documents internes et d'y répondre en langage naturel, avec citations des sources.

**Stage effectué chez :** OneClick — Agence digitale, Marrakech
**Type :** R&D / Ingénierie Full-stack + IA
**Encadrant :** Ali Ourtanane

---

## 1. Contexte

Les organisations génèrent un volume important d'informations non structurées réparties sur de nombreux formats et systèmes de stockage (contrats, rapports, procédures, factures, présentations, fichiers scannés, wikis internes). Retrouver une information précise dans cette masse est lent, manuel et source d'erreurs.

- La recherche par mots-clés classique échoue car elle associe des mots, pas du sens.
- Les chatbots IA génériques échouent car ils ne connaissent pas les documents internes de l'entreprise et ont tendance à inventer des réponses.

**Rag_Pfa** vise à construire une plateforme intelligente qui centralise les connaissances de l'entreprise, indexe automatiquement les documents, et répond aux questions en langage naturel — en s'appuyant **exclusivement** sur les documents de l'organisation, avec citation des sources.

Le socle technique est le **RAG** : récupérer d'abord les passages pertinents, puis laisser le LLM répondre en s'appuyant uniquement sur ces passages.

---

## 2. Objectifs

Concevoir, développer et déployer une plateforme web fonctionnelle permettant à une entreprise de :

1. Uploader et organiser ses documents internes.
2. Traiter, indexer et vectoriser automatiquement ces documents.
3. Effectuer une recherche sémantique, en langage naturel, multilingue.
4. Interroger un assistant IA qui répond avec ses sources, jamais de manière inventée.
5. Administrer les utilisateurs, collections et modèles via un dashboard.
6. Mesurer l'usage et la couverture des connaissances via des analytics.

---

## 3. Périmètre fonctionnel

### 3.1 Gestion documentaire
- Upload, organisation et versioning des documents :
  - PDF, Word (DOCX), Excel (XLSX), PowerPoint (PPTX)
  - Texte brut / Markdown
  - Images (via OCR)
  - Pages web (ingestion par URL)
- Regroupement en **collections de connaissances** (ex. RH, Juridique, Technique).

### 3.2 Pipeline de traitement des données
Pipeline automatisé et asynchrone qui :
- Extrait le contenu brut de chaque format (OCR inclus pour les scans)
- Nettoie et normalise le texte
- Découpe les documents en chunks sémantiques (stratégie de chevauchement)
- Génère les embeddings pour chaque chunk
- Stocke les vecteurs + métadonnées (fichier source, page, section, collection, permissions)

### 3.3 Moteur de recherche IA
- Recherche sémantique (vectorielle)
- Recherche hybride (vectorielle + mots-clés) — bonus
- Compréhension de requêtes en langage naturel
- Récupération de contexte et re-ranking
- Citation des sources sur chaque résultat
- Requêtes multilingues (FR / EN / AR minimum)

### 3.4 Assistant conversationnel
Assistant sécurisé répondant uniquement à partir de la base de connaissances interne :
- Historique de conversation
- Prise en compte du contexte sur plusieurs tours
- Questions de suivi
- Références aux sources (document + page)
- Indicateur de confiance
- Réponse explicite **« Je ne sais pas »** quand la base ne contient pas la réponse (comportement obligatoire)

### 3.5 Dashboard d'administration
- Gestion des utilisateurs
- Gestion des rôles et permissions (accès par collection)
- Gestion des collections de connaissances
- Gestion des documents (ré-indexation, suppression, statut du pipeline)
- Configuration du modèle IA (modèle, température, taille des chunks, top-k)
- Analytics de recherche

### 3.6 Analytics
- Documents les plus consultés
- Questions les plus fréquentes
- Questions sans réponse (métrique la plus précieuse : révèle les lacunes de connaissances)
- Couverture de connaissances par collection
- Statistiques de réponse IA (latence, tokens, confiance)

---

## 4. Architecture cible

```
Documents
   │
PDF DOCX XLSX PPTX IMG URL
   │
   ▼
Extraction & OCR
   │
   ▼
Traitement du texte
   │
   ▼
Génération de chunks
   │
   ▼
Génération des embeddings
   │
   ▼
Base de données vectorielle
   │
   ├────────────┬────────────┐
   │            │            │
Recherche    Métadonnées
sémantique      (DB)
   │            │
   └────────────┴────────────┘
   │
   ▼
   LLM
   │
   ▼
API de réponse IA
   │
   ▼
Frontend Next.js
```

---

## 5. Stack technique

| Couche               | Technologie                                  |
|----------------------|-----------------------------------------------|
| Frontend             | Next.js, React, TypeScript, Tailwind CSS      |
| Backend              | Python, FastAPI                               |
| Orchestration IA     | LangChain / LlamaIndex                        |
| LLM                  | OpenAI, Claude, ou modèles open-source         |
| Embeddings           | Sentence Transformers                          |
| Base de données      | PostgreSQL                                     |
| Vector store         | pgvector ou Qdrant                             |
| Stockage fichiers    | Cloudflare R2 ou Amazon S3                      |
| Authentification     | JWT ou Clerk                                    |
| Déploiement          | Docker, Nginx                                   |

> La stack ci-dessus est indicative. Toute déviation doit être justifiée techniquement.

---

## 6. Structure du dépôt

```
Rag_Pfa/
├── backend/          # API FastAPI, pipeline d'ingestion, logique RAG
├── frontend/         # Application Next.js (upload, chat, dashboard)
├── qdrant_storage/    # Stockage local de la base vectorielle Qdrant
├── docker-compose.yml # Orchestration des services (backend, frontend, DB, Qdrant)
└── README.md
```

---

## 7. Phasage du projet

| Phase | Objectif | Résultat attendu |
|-------|----------|-------------------|
| 1 | État de l'art & spécification | Compréhension du RAG, comparaison des vector DBs et stratégies de chunking, spec fonctionnelle |
| 2 | Pipeline d'ingestion | Documents → texte → chunks → embeddings → vector DB, fonctionnel de bout en bout sur PDF |
| 3 | Recherche & API RAG | Recherche sémantique + réponse LLM avec citations, exposée via FastAPI |
| 4 | Frontend | UI d'upload, UI de chat avec sources, gestion des collections |
| 5 | Admin & analytics | Rôles, permissions, dashboards |
| 6 | Déploiement & documentation | Déploiement Dockerisé, documentation, démo finale |

> Objectif : livrer tôt une **tranche verticale fonctionnelle** (PDF → question → réponse citée) avant d'élargir aux autres formats.

---

## 8. Livrables attendus

- Plateforme web fonctionnelle (code source, dépôt Git, historique de commits propre)
- Documentation de l'API REST
- Conception du schéma de base de données et du schéma vectoriel
- Documentation technique (architecture, choix de chunking/retrieval et justifications)
- Guide de déploiement (Docker)
- Manuel utilisateur
- Démonstration en direct sur un jeu de documents d'entreprise

---

## 9. Critères d'évaluation

- **Qualité des réponses** : correctes, ancrées dans les sources, correctement citées
- **Honnêteté du système** : dit « je ne sais pas » plutôt que d'halluciner
- **Robustesse du pipeline** : résiste à un PDF scanné de 200 pages mal formaté
- **Qualité du code** : structure, lisibilité, tests sur le chemin critique
- **Autonomie** : capacité à chercher, décider, justifier, avancer
- **Documentation & démo** : un tiers peut exécuter et comprendre le projet

---

## 10. Perspective industrielle

Une fois fonctionnelle, la plateforme peut être proposée en SaaS à des organisations à forte documentation interne : cabinets d'avocats, cabinets comptables, hôpitaux, universités, hôtels, assurances, industriels, administrations publiques, PME.

Des extensions futures (Microsoft 365, Google Drive, SharePoint, Slack, Teams, email) en feraient un assistant complet de connaissance d'entreprise.

---

## 11. Installation & lancement (à compléter au fil du projet)

```bash
# Cloner le dépôt
git clone https://github.com/tr22014/Rag_Pfa.git
cd Rag_Pfa

# Lancer les services via Docker
docker-compose up --build
```

- Backend : `http://localhost:8000`
- Frontend : `http://localhost:3000`
- Qdrant : `http://localhost:6333`

> ⚠️ Section à mettre à jour avec les variables d'environnement, les prérequis exacts, et les instructions de configuration au fur et à mesure de l'avancement.

---

## 12. Avancement actuel

- [ ] Phase 1 — État de l'art & spécification
- [ ] Phase 2 — Pipeline d'ingestion (PDF → chunks → embeddings → Qdrant)
- [ ] Phase 3 — Recherche & API RAG (FastAPI)
- [ ] Phase 4 — Frontend (upload, chat, collections)
- [ ] Phase 5 — Admin & analytics
- [ ] Phase 6 — Déploiement & documentation

---

## 13. Auteur

Projet réalisé dans le cadre d'un stage (PFA/PFE) chez **OneClick**, sous la supervision de **Ali Ourtanane**.