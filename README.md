# 🏗️ GCI-2011 — Poutre Composite Interactive

**Outil pédagogique** pour le cours GCI-2011 Conception des structures I  
Université Laval · Prof. Luca Sorelli · CSA S16:24 Ch.17

## 🚀 Lancer l'application

```bash
pip install -r requirements.txt
streamlit run composite_app.py
```

L'app s'ouvre dans le navigateur à http://localhost:8501

## 🌐 Déploiement Streamlit Cloud (GitHub)

1. Poussez ce dépôt sur GitHub
2. Allez sur https://share.streamlit.io
3. Connectez votre compte GitHub
4. Choisissez ce dépôt → `composite_app.py`
5. L'app est en ligne en 2 minutes ✅

## 📐 Fonctionnalités

- **46 sections T1** (HSC) + propriétés affichées en temps réel
- **3 types de coffrage** : dalle pleine, nervures ⊥, nervures ∥
- **ELU §17.9.3** : Cas A/B/C avec toutes les étapes détaillées
- **Goujons §17.7.2** : dalle pleine, nervures perp. (Ap pyramidal), nervures par.
- **ELS §17.3.1** : It, Ie, Its, Ies, ANE instantané + ANE fluage
- **Déflexions** : Δ_vive, Δ_morte, Δ_fluage, comparaison L/360
- **Formules éducatives** complètes avec références CSA
- **Exemples intégrés** : Ex. 7.1 (f'c=20 et f'c=35) et Ex. 7.2

## ⚠️ Avertissement

Outil pédagogique uniquement — aucune responsabilité assumée.  
Résultats validés sur Ex. 7.1 (2026) et Ex. 7.2 du cours GCI-2011.

## 📋 Conventions

| Paramètre | Valeur |
|-----------|--------|
| φ (acier) | 0.90 |
| φc (béton) | 0.65 |
| φsc (goujons) | 0.80 |
| Fu (goujons W59) | 415 MPa |
| α₁ | 0.85 − 0.0015·f'c ≥ 0.67 |
| Ec simplifié | 4500·√f'c MPa |
| Ec complet | (3300√f'c+6900)·(ρ/2300)^1.5 |
