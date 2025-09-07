<h1 align="center">Christophe — Consultant Supply Chain & AI/Analytics | Manager Supply Chain</h1>
<p align="center">
Prévision & risque (ML) • RAG d’entreprise on-prem • Agents “Control Tower” • KPI OTIF/CO₂ • Focus Lille / Hauts-de-France
</p>

<p align="center">
  <!-- Badges simples via shields.io -->
  <a href="https://github.com/christophe-4"><img alt="Followers" src="https://img.shields.io/github/followers/christophe-4?style=flat"></a>
  <a href="https://github.com/christophe-4?tab=repositories"><img alt="Public Repos" src="https://img.shields.io/badge/repos-public-blue"></a>
  <a href="#"><img alt="License" src="https://img.shields.io/badge/license-MIT-green"></a>
</p>

## 🧭 Positionnement
Je conçois des **solutions data/IA orientées supply chain** : prévision (demande/lead time), **maintenance prédictive**, **RAG d’entreprise** (on-prem, confidentialité), et **agents “control-tower”** pour accélérer les décisions (service, coûts, CO₂).

## 🔥 Projets phares
- **SCANIA Component X — Maintenance prédictive (ML)**  
  Risque de panne imminente (classes 0–4) + **métrique de coût** (challenge IDA). Baselines + **LightGBM** ; courbes ROC/PR, importances.  
  ↳ Code : [`projects/scania-ml`](./projects/scania-ml)
- **RAG Supply Chain — Knowledge Base Lille (on-prem)**  
  Ingestion PDF/DOCX (SOP, contrats transport, fiches produit) → **spaCy** (SKU/PO/carrier) → (option) **Presidio** PII → **Elasticsearch/OpenSearch** (BM25 + kNN/ELSER) → **LangChain** (retriever hybride) → UI Streamlit. **Évaluation** : Ragas (faithfulness/relevancy) + **Kibana** (latences, % réponses citées).
- **Forecasting Demande & Stock (DL)**  
  Séries temporelles (TFT/N-Beats/LSTM) avec features calendrier/promo, comparaison aux baselines statistiques. Livrables orientés **OTIF** et **stock** (service, MAPE, stock de sécurité).
- **Agent IA “Control-Tower”**  
  Orchestration **LangGraph/CrewAI** : interroge le RAG, croise KPI (ETA, backlog, aléas), applique des règles, génère un **plan d’action** (alerte, ticket, replanification). Observabilité via **Langfuse**.

## 🧰 Stack (principale)
**Data/ML** : Python, scikit-learn, LightGBM, XGBoost, PyTorch, MLflow  
**RAG & LLM** : LangChain, (LangGraph/CrewAI), vLLM ou Ollama, Unstructured, **Chroma** ou **Elasticsearch/OpenSearch** (BM25 + kNN/ELSER)  
**NLP & conformité** : **spaCy** (NER supply), **Microsoft Presidio** (PII)  
**Observabilité** : Kibana (logs/latences), **Langfuse** (traces LLM)  
**Ops on-prem** : FastAPI, Podman/Compose, (Kafka/NiFi/Camel/Flowable/Temporal pour intégration si besoin)

## 📌 Comment je travaille
- **Reproductibilité** : `requirements.txt`, seed, scripts de run, README détaillés.  
- **Lisibilité des graphes** : palettes **qualitatives** pour classes, **séquentielles** pour intensités ; mêmes couleurs = mêmes catégories.  
- **Impact métier** : chaque repo documente **hypothèses**, **métriques métier** (OTIF, coût, CO₂) et **limites**.

## 📫 Contact
- LinkedIn : https://www.linkedin.com/in/christophe-troel
