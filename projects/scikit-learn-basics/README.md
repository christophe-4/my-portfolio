# scikit-learn-basics

# Projet 1 – Classification avec scikit-learn : Spaceship Titanic (Kaggle)

## 🎯 Objectif du projet

Ce projet a pour but de construire un **modèle de classification supervisée** avec **scikit-learn** pour la compétition Kaggle **“Spaceship Titanic”**.

La tâche consiste à prédire si un passager a été **transporté dans une dimension parallèle** lors d’un accident du vaisseau (`Transported` = True/False), à partir de ses caractéristiques personnelles, de sa cabine et de ses dépenses à bord. :contentReference[oaicite:0]{index=0}  

Ce projet me sert à :

- mettre en pratique un **pipeline complet de machine learning** (prétraitement → entraînement → évaluation → soumission Kaggle) ;
- valider mon travail via un **score réel et un classement sur le leaderboard Kaggle** ;
- disposer d’un projet clair à présenter dans mon **portfolio GitHub**.

---

## 🗂️ Données

Compétition : [Spaceship Titanic – Kaggle](https://www.kaggle.com/competitions/spaceship-titanic) :contentReference[oaicite:1]{index=1}  

Les fichiers fournis sont :

- `train.csv` : données d’entraînement avec la variable cible `Transported` ;
- `test.csv` : données de test sans la cible ;
- `sample_submission.csv` : format attendu pour la soumission Kaggle. :contentReference[oaicite:2]{index=2}  

### Variables principales (exemples)

- **Caractéristiques des passagers** :  
  `HomePlanet`, `Destination`, `Age`, `VIP`, `CryoSleep`… :contentReference[oaicite:3]{index=3}  
- **Informations cabine** :  
  `Cabin` (qui encode le pont, le numéro et le côté du vaisseau).  
- **Dépenses à bord** :  
  `RoomService`, `FoodCourt`, `ShoppingMall`, `Spa`, `VRDeck`. :contentReference[oaicite:4]{index=4}  
- **Cible** :  
  `Transported` (booléen indiquant si le passager a été transporté ou non).

Ces données permettent de travailler sur un cas typique de **classification client / événement binaire**, transposable à d’autres domaines comme la supply chain ou la relation client.

---

## 🧠 Approche / Méthodologie

### 1. Exploration et nettoyage

- Inspection des valeurs manquantes et des distributions.
- Suppression ou transformation de colonnes peu informatives (ex. identifiants purs).
- Analyse des corrélations et de l’importance métier des variables (âge, dépenses, cryosleep, etc.).

### 2. Prétraitement des données

Mise en place d’un **pipeline scikit-learn** comprenant :

- **Imputation des valeurs manquantes** :
  - numérique : moyenne / médiane (ou autre stratégie) ;
  - catégoriel : modalité la plus fréquente.
- **Encodage des variables catégorielles** :
  - encodage one-hot (ou équivalent).
- **Mise à l’échelle** des variables numériques si nécessaire.

### 3. Modélisation

Tests de plusieurs modèles de classification :

- Régression logistique
- Random Forest
- Gradient Boosting / XGBoost / autres modèles d’arbres (selon les essais)
- Comparaison via **validation croisée** (ex. `StratifiedKFold`) et métrique **accuracy**.

Sélection du modèle final en fonction :

- de la performance moyenne en cross-validation,
- de la stabilité des résultats,
- de la simplicité d’interprétation.

### 4. Génération de la soumission Kaggle

- Entraînement du modèle retenu sur l’ensemble des données `train`.
- Prédiction de `Transported` sur `test`.
- Création du fichier `submission.csv` au format demandé (`PassengerId`, `Transported`).
- Soumission sur Kaggle et récupération :
  - du **score sur la leaderboard (accuracy)**,
  - du **rang** parmi les participants.

---

## 📈 Résultats (à compléter après soumission)

- **Score Kaggle (accuracy)** : `...`  
- **Classement** : `...` (exemple : *top 30 % des participants*).

Commentaires possibles :

- Quel modèle fonctionne le mieux (ex. RandomForest vs GradientBoosting).
- Impact de certains choix de prétraitement (encodage, imputation, features cabine, etc.).
- Lien entre caractéristiques (ex. `CryoSleep`, dépenses, cabine) et probabilité d’être transporté. :contentReference[oaicite:5]{index=5}  

---

## 🛠️ Stack technique

- **Langage** : Python
- **Librairies principales** :
  - `pandas`, `numpy`
  - `scikit-learn`
  - éventuellement : `matplotlib` / `seaborn` pour les graphiques
- **Environnement** : Jupyter Notebook / VS Code

---

## 🚀 Reproduire le projet

### 1. Cloner le dépôt

```bash
git clone https://github.com/<ton-pseudo-github>/my-portfolio.git
cd my-portfolio/projects/spaceship-titanic-scikit-learn

