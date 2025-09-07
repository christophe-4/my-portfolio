# SCANIA Component X — Maintenance prédictive (ML)

> ⚑ Objectif : pipeline **simple mais complet** pour prédire une **panne imminente** du composant moteur « Component X » sur une flotte de camions SCANIA (tâche du challenge IDA 2024).  
> ⚙️ Tech : Python, scikit-learn, LightGBM, notebooks Jupyter.

---

## 1. Problème & données

- **Tâche** : classifier le **dernier readout** de chaque véhicule en 5 classes de risque (0 = pas imminent ; 1 → 4 = fenêtres de plus en plus proches de la panne).  
- **Jeu de données** (réel, multivarié) :  
  - `*_operational_readouts.csv` : observations tabulaires (comptages/buckets, valeurs agrégées).  
  - `*_specifications.csv` : métadonnées véhicule (catégorielles).  
  - `train_tte.csv`, `*_labels.csv` : temps avant panne / classes (train/validation/test).  
- **Évaluation principale** : **coût de mauvaise classification** (fortement pénalisant si la panne est proche).  
- **Évaluation secondaire** : F1 macro, ROC-AUC (one-vs-rest).

> 🔎 Les CSV sont conséquents : ne pas versionner `data/` (voir `.gitignore`). Ce dépôt fournit des scripts/notebooks reproductibles et laisse l’utilisateur télécharger les données depuis la source officielle.

---

## 2. Approche « simple mais solide »

1) **Baselines**  
   - `DummyClassifier` (majoritaire) — point de départ.  
   - `LogisticRegression` dans un `Pipeline` (imputation médiane + standardisation + one-hot sur `specifications`).

2) **Modèle recommandé**  
   - **LightGBM (classification 5 classes)** : très efficace sur données tabulaires hétérogènes et rapides à entraîner.  
   - Gestion du déséquilibre : `class_weight='balanced'` ou pondération personnalisée par la matrice de coûts.  
   - Petits grids de hyperparamètres : `num_leaves`, `max_depth`, `learning_rate`, `min_data_in_leaf`.

3) **Split & fuite de données**  
   - Utiliser les splits fournis (`train_*`, `validation_*`, `test_*`).  
   - Entraîner sur train, sélectionner sur validation, **ne pas** regarder test avant le reporting final.

4) **Métriques & reporting**  
   - **Total_cost** (matrice de coûts officielle) + **F1 macro**.  
   - Matrice de confusion, courbes ROC/PR, importances de variables (gain LightGBM).  
   - Option : SHAP pour interprétabilité.

---

## 3. Arborescence du projet
projects/scania-ml/
├─ data/ # (non versionné) placez les CSV ici
├─ notebooks/
│ ├─ 01_eda.ipynb
│ ├─ 02_train_baseline.ipynb
│ └─ 03_train_lightgbm.ipynb
├─ scripts/
│ ├─ make_cost_metric.py
│ └─ train_lightgbm.py
├─ models/ # artefacts (pkl, booster.txt)
├─ charts/ # figures exportées (png/svg)
├─ requirements.txt
└─ README.md
## 4. Installation (Windows CMD)

```cmd
cd projects\scania-ml
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
