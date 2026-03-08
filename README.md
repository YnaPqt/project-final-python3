# Anime  Database App

## Description
Ce projet est une application Python en ligne de commande permettant de gérer une base de données de dessins animés.

L'application utilise Peewee pour interagir avec une base de données SQLite et permet d'effectuer les opérations CRUD (Create, Read, Update, Delete).

Un utilisateur peut:
- ajouter un animé
- afficher la liste des animés
- modifier un animé existant
- supprimer un animé

Les informations enregistrées pour chaque animé comprennent:
- le titre
- le studio
- l'année de sortie
- une description
- les personnages
- les genres

  ## Technologies utilisées
  - Python
  - Peewe
  - SQLite
  - Pandas
  - Pytest

  ## Structure
  Project-final-python3 /
  - models.py
  - anime_modules.py
  - app.py
  - anime.db
  - test_app.py
  - requirements.txt
  - README.md
 
- models.py: Défintion des modèles Peewee et structure de la base de données
- anime_modules.py: Logique de l'application et les fonctions en CRUD
- app.py: Interface en ligne de commade dont le menu interactif
- test_app.py: Tests automatisés avec pytest
- anime.db: Base de données SQLite
- requirements.txt: Dépendances du projet

## Modèles de données
La base de données contient les tables suivantes:

**Studio**

Contient les studios de production

**Anime**

Contient les informations principales sur les animés.

**Character**

Contient les personnages associés à un animé.

**Genre**

Contient les genres d'animés.


