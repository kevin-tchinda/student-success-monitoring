# Journal de Projet - API de Prédiction pour `Suivi de Réussite Étudiante`

## Déroulement du Projet

**Phase initiale** : Nous avons commencé par l'entraînement et l'optimisation des modèles de *machine learning*. Les modèles de **classification** et **régression** ont été optimisés via des recherches d'hyperparamètres utilisant `RandomizedSearchCV` et `GridSearchCV`, puis enregistrés sur **MLflow** avec **DagsHub** comme backend.

**Développement de l'API** : Ensuite, nous avons développé l'API **FastAPI** en créant une structure modulaire organisée autour de plusieurs composants :
- `main.py` pour les endpoints
- `schemas.py` pour la validation avec **Pydantic**
- `model_loader.py` pour le client MLflow
- `config.py` pour la gestion de configuration

**Intégration MLflow** : Puis nous avons intégré **MLflow** pour charger les modèles et preprocesseurs. Cette étape a inclus la configuration de l'authentification via tokens DagsHub et le chargement dynamique des modèles au démarrage de l'application.

**Tests de l'API et validation** : Enfin, nous avons testé l'API en local et à travers les fonctionnalités exposé via l'interface **Swagger UI**-like de `FastAPI` pour la documentation visuelle et claire disponible sur `/docs`, tout en veillant au bon fonctionnement des endpoints `/health` et `/predict`.

## Défis Techniques Rencontrés

**Problèmes d'import** : Nous avons d'abord rencontré des difficultés avec l'import des modules Python, résolues en restructurant l'architecture des dossiers et en créant un point d'entrée unique dans `api/main.py`.

**Incompatibilité des formats** : L'incompatibilité des formats de données avec MLflow a nécessité la création de **DataFrames** avec des noms de colonnes spécifiques correspondant exactement à ceux attendus par les modèles entraînés.

**Gestion du préprocessing** : Le préprocessing a posé difficulté car les modèles attendaient des données normalisées. Nous avons résolu ceci en sauvegardant et chargeant les *preprocesseurs* (`StandardScaler`, `MinMaxScaler`) depuis **MLflow** comme artefacts complémentaires.

**Validation des schémas** : La validation des schémas de réponse a requis plusieurs ajustements pour assurer la cohérence entre les données retournées par l'API et les schémas **Pydantic** définis, notamment pour le champ `features_used` devenu optionnel.

## Architecture et Bonnes Pratiques

**Séparation des responsabilités** : L'API suit une architecture en couches avec une séparation claire entre la logique métier, l'accès aux modèles et la validation des données.

**Gestion de configuration** : La configuration utilise des variables d'environnement via un fichier `.env` pour une meilleure sécurité et flexibilité, notamment pour les credentials DagsHub.

**Versioning des modèles** : Le *versioning* est géré via **MLflow Model Registry**, permettant des déploiements progressifs et des *rollbacks* si nécessaire.

**Performance** : Le chargement des modèles au démarrage (*startup event*) optimise les temps de réponse des prédictions.
